# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\primitives\serialization\ssh.py
import binascii, os, re, struct, typing
from base64 import encodebytes as _base64_encode
from cryptography import utils
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.backends.interfaces import Backend
from cryptography.hazmat.primitives.asymmetric import dsa, ec, ed25519, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat, PublicFormat
try:
    from bcrypt import kdf as _bcrypt_kdf
    _bcrypt_supported = True
except ImportError:
    _bcrypt_supported = False

    def _bcrypt_kdf(password: bytes, salt: bytes, desired_key_bytes: int, rounds: int, ignore_few_rounds: bool=False) -> bytes:
        raise UnsupportedAlgorithm('Need bcrypt module')


_SSH_ED25519 = b'ssh-ed25519'
_SSH_RSA = b'ssh-rsa'
_SSH_DSA = b'ssh-dss'
_ECDSA_NISTP256 = b'ecdsa-sha2-nistp256'
_ECDSA_NISTP384 = b'ecdsa-sha2-nistp384'
_ECDSA_NISTP521 = b'ecdsa-sha2-nistp521'
_CERT_SUFFIX = b'-cert-v01@openssh.com'
_SSH_PUBKEY_RC = re.compile(b'\\A(\\S+)[ \\t]+(\\S+)')
_SK_MAGIC = b'openssh-key-v1\x00'
_SK_START = b'-----BEGIN OPENSSH PRIVATE KEY-----'
_SK_END = b'-----END OPENSSH PRIVATE KEY-----'
_BCRYPT = b'bcrypt'
_NONE = b'none'
_DEFAULT_CIPHER = b'aes256-ctr'
_DEFAULT_ROUNDS = 16
_MAX_PASSWORD = 72
_PEM_RC = re.compile(_SK_START + b'(.*?)' + _SK_END, re.DOTALL)
_PADDING = memoryview(bytearray(range(1, 17)))
_SSH_CIPHERS = {b'aes256-ctr':(
  algorithms.AES, 32, modes.CTR, 16), 
 b'aes256-cbc':(
  algorithms.AES, 32, modes.CBC, 16)}
_ECDSA_KEY_TYPE = {'secp256r1':_ECDSA_NISTP256, 
 'secp384r1':_ECDSA_NISTP384, 
 'secp521r1':_ECDSA_NISTP521}
_U32 = struct.Struct(b'>I')
_U64 = struct.Struct(b'>Q')

def _ecdsa_key_type(public_key):
    """Return SSH key_type and curve_name for private key."""
    curve = public_key.curve
    if curve.name not in _ECDSA_KEY_TYPE:
        raise ValueError('Unsupported curve for ssh private key: %r' % curve.name)
    return _ECDSA_KEY_TYPE[curve.name]


def _ssh_pem_encode(data, prefix=_SK_START + b'\n', suffix=_SK_END + b'\n'):
    return (b'').join([prefix, _base64_encode(data), suffix])


def _check_block_size(data, block_len):
    """Require data to be full blocks"""
    if not data or len(data) % block_len != 0:
        raise ValueError('Corrupt data: missing padding')


def _check_empty(data):
    """All data should have been parsed."""
    if data:
        raise ValueError('Corrupt data: unparsed data')


def _init_cipher(ciphername, password, salt, rounds, backend):
    """Generate key + iv and return cipher."""
    if not password:
        raise ValueError('Key is password-protected.')
    algo, key_len, mode, iv_len = _SSH_CIPHERS[ciphername]
    seed = _bcrypt_kdf(password, salt, key_len + iv_len, rounds, True)
    return Cipher(algo(seed[:key_len]), mode(seed[key_len:]), backend)


def _get_u32(data):
    """Uint32"""
    if len(data) < 4:
        raise ValueError('Invalid data')
    return (
     _U32.unpack(data[:4])[0], data[4:])


def _get_u64(data):
    """Uint64"""
    if len(data) < 8:
        raise ValueError('Invalid data')
    return (
     _U64.unpack(data[:8])[0], data[8:])


def _get_sshstr(data):
    """Bytes with u32 length prefix"""
    n, data = _get_u32(data)
    if n > len(data):
        raise ValueError('Invalid data')
    return (
     data[:n], data[n:])


def _get_mpint(data):
    """Big integer."""
    val, data = _get_sshstr(data)
    if val:
        if val[0] > 127:
            raise ValueError('Invalid data')
    return (
     int.from_bytes(val, 'big'), data)


def _to_mpint(val):
    """Storage format for signed bigint."""
    if val < 0:
        raise ValueError('negative mpint not allowed')
    if not val:
        return b''
    else:
        nbytes = (val.bit_length() + 8) // 8
        return utils.int_to_bytes(val, nbytes)


class _FragList(object):
    __doc__ = 'Build recursive structure without data copy.'

    def __init__(self, init=None):
        self.flist = []
        if init:
            self.flist.extend(init)

    def put_raw(self, val):
        """Add plain bytes"""
        self.flist.append(val)

    def put_u32(self, val):
        """Big-endian uint32"""
        self.flist.append(_U32.pack(val))

    def put_sshstr(self, val):
        """Bytes prefixed with u32 length"""
        if isinstance(val, (bytes, memoryview, bytearray)):
            self.put_u32(len(val))
            self.flist.append(val)
        else:
            self.put_u32(val.size())
            self.flist.extend(val.flist)

    def put_mpint(self, val):
        """Big-endian bigint prefixed with u32 length"""
        self.put_sshstr(_to_mpint(val))

    def size(self):
        """Current number of bytes"""
        return sum(map(len, self.flist))

    def render(self, dstbuf, pos=0):
        """Write into bytearray"""
        for frag in self.flist:
            flen = len(frag)
            start, pos = pos, pos + flen
            dstbuf[start:pos] = frag

        return pos

    def tobytes(self):
        """Return as bytes"""
        buf = memoryview(bytearray(self.size()))
        self.render(buf)
        return buf.tobytes()


class _SSHFormatRSA(object):
    __doc__ = 'Format for RSA keys.\n\n    Public:\n        mpint e, n\n    Private:\n        mpint n, e, d, iqmp, p, q\n    '

    def get_public(self, data):
        """RSA public fields"""
        e, data = _get_mpint(data)
        n, data = _get_mpint(data)
        return ((e, n), data)

    def load_public(self, key_type, data, backend):
        """Make RSA public key from data."""
        (e, n), data = self.get_public(data)
        public_numbers = rsa.RSAPublicNumbers(e, n)
        public_key = public_numbers.public_key(backend)
        return (public_key, data)

    def load_private(self, data, pubfields, backend):
        """Make RSA private key from data."""
        n, data = _get_mpint(data)
        e, data = _get_mpint(data)
        d, data = _get_mpint(data)
        iqmp, data = _get_mpint(data)
        p, data = _get_mpint(data)
        q, data = _get_mpint(data)
        if (
         e, n) != pubfields:
            raise ValueError('Corrupt data: rsa field mismatch')
        dmp1 = rsa.rsa_crt_dmp1(d, p)
        dmq1 = rsa.rsa_crt_dmq1(d, q)
        public_numbers = rsa.RSAPublicNumbers(e, n)
        private_numbers = rsa.RSAPrivateNumbers(p, q, d, dmp1, dmq1, iqmp, public_numbers)
        private_key = private_numbers.private_key(backend)
        return (private_key, data)

    def encode_public(self, public_key, f_pub):
        """Write RSA public key"""
        pubn = public_key.public_numbers()
        f_pub.put_mpint(pubn.e)
        f_pub.put_mpint(pubn.n)

    def encode_private(self, private_key, f_priv):
        """Write RSA private key"""
        private_numbers = private_key.private_numbers()
        public_numbers = private_numbers.public_numbers
        f_priv.put_mpint(public_numbers.n)
        f_priv.put_mpint(public_numbers.e)
        f_priv.put_mpint(private_numbers.d)
        f_priv.put_mpint(private_numbers.iqmp)
        f_priv.put_mpint(private_numbers.p)
        f_priv.put_mpint(private_numbers.q)


class _SSHFormatDSA(object):
    __doc__ = 'Format for DSA keys.\n\n    Public:\n        mpint p, q, g, y\n    Private:\n        mpint p, q, g, y, x\n    '

    def get_public(self, data):
        """DSA public fields"""
        p, data = _get_mpint(data)
        q, data = _get_mpint(data)
        g, data = _get_mpint(data)
        y, data = _get_mpint(data)
        return ((p, q, g, y), data)

    def load_public(self, key_type, data, backend):
        """Make DSA public key from data."""
        (p, q, g, y), data = self.get_public(data)
        parameter_numbers = dsa.DSAParameterNumbers(p, q, g)
        public_numbers = dsa.DSAPublicNumbers(y, parameter_numbers)
        self._validate(public_numbers)
        public_key = public_numbers.public_key(backend)
        return (public_key, data)

    def load_private(self, data, pubfields, backend):
        """Make DSA private key from data."""
        (p, q, g, y), data = self.get_public(data)
        x, data = _get_mpint(data)
        if (
         p, q, g, y) != pubfields:
            raise ValueError('Corrupt data: dsa field mismatch')
        parameter_numbers = dsa.DSAParameterNumbers(p, q, g)
        public_numbers = dsa.DSAPublicNumbers(y, parameter_numbers)
        self._validate(public_numbers)
        private_numbers = dsa.DSAPrivateNumbers(x, public_numbers)
        private_key = private_numbers.private_key(backend)
        return (private_key, data)

    def encode_public(self, public_key, f_pub):
        """Write DSA public key"""
        public_numbers = public_key.public_numbers()
        parameter_numbers = public_numbers.parameter_numbers
        self._validate(public_numbers)
        f_pub.put_mpint(parameter_numbers.p)
        f_pub.put_mpint(parameter_numbers.q)
        f_pub.put_mpint(parameter_numbers.g)
        f_pub.put_mpint(public_numbers.y)

    def encode_private(self, private_key, f_priv):
        """Write DSA private key"""
        self.encode_public(private_key.public_key(), f_priv)
        f_priv.put_mpint(private_key.private_numbers().x)

    def _validate(self, public_numbers):
        parameter_numbers = public_numbers.parameter_numbers
        if parameter_numbers.p.bit_length() != 1024:
            raise ValueError('SSH supports only 1024 bit DSA keys')


class _SSHFormatECDSA(object):
    __doc__ = 'Format for ECDSA keys.\n\n    Public:\n        str curve\n        bytes point\n    Private:\n        str curve\n        bytes point\n        mpint secret\n    '

    def __init__(self, ssh_curve_name, curve):
        self.ssh_curve_name = ssh_curve_name
        self.curve = curve

    def get_public(self, data):
        """ECDSA public fields"""
        curve, data = _get_sshstr(data)
        point, data = _get_sshstr(data)
        if curve != self.ssh_curve_name:
            raise ValueError('Curve name mismatch')
        if point[0] != 4:
            raise NotImplementedError('Need uncompressed point')
        return (
         (
          curve, point), data)

    def load_public(self, key_type, data, backend):
        """Make ECDSA public key from data."""
        (curve_name, point), data = self.get_public(data)
        public_key = ec.EllipticCurvePublicKey.from_encoded_point(self.curve, point.tobytes())
        return (
         public_key, data)

    def load_private(self, data, pubfields, backend):
        """Make ECDSA private key from data."""
        (curve_name, point), data = self.get_public(data)
        secret, data = _get_mpint(data)
        if (
         curve_name, point) != pubfields:
            raise ValueError('Corrupt data: ecdsa field mismatch')
        private_key = ec.derive_private_key(secret, self.curve, backend)
        return (private_key, data)

    def encode_public(self, public_key, f_pub):
        """Write ECDSA public key"""
        point = public_key.public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)
        f_pub.put_sshstr(self.ssh_curve_name)
        f_pub.put_sshstr(point)

    def encode_private(self, private_key, f_priv):
        """Write ECDSA private key"""
        public_key = private_key.public_key()
        private_numbers = private_key.private_numbers()
        self.encode_public(public_key, f_priv)
        f_priv.put_mpint(private_numbers.private_value)


class _SSHFormatEd25519(object):
    __doc__ = 'Format for Ed25519 keys.\n\n    Public:\n        bytes point\n    Private:\n        bytes point\n        bytes secret_and_point\n    '

    def get_public(self, data):
        """Ed25519 public fields"""
        point, data = _get_sshstr(data)
        return ((point,), data)

    def load_public(self, key_type, data, backend):
        """Make Ed25519 public key from data."""
        (point,), data = self.get_public(data)
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(point.tobytes())
        return (
         public_key, data)

    def load_private(self, data, pubfields, backend):
        """Make Ed25519 private key from data."""
        (point,), data = self.get_public(data)
        keypair, data = _get_sshstr(data)
        secret = keypair[:32]
        point2 = keypair[32:]
        if point != point2 or (point,) != pubfields:
            raise ValueError('Corrupt data: ed25519 field mismatch')
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret)
        return (private_key, data)

    def encode_public(self, public_key, f_pub):
        """Write Ed25519 public key"""
        raw_public_key = public_key.public_bytes(Encoding.Raw, PublicFormat.Raw)
        f_pub.put_sshstr(raw_public_key)

    def encode_private(self, private_key, f_priv):
        """Write Ed25519 private key"""
        public_key = private_key.public_key()
        raw_private_key = private_key.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
        raw_public_key = public_key.public_bytes(Encoding.Raw, PublicFormat.Raw)
        f_keypair = _FragList([raw_private_key, raw_public_key])
        self.encode_public(public_key, f_priv)
        f_priv.put_sshstr(f_keypair)


_KEY_FORMATS = {_SSH_RSA: _SSHFormatRSA(), 
 _SSH_DSA: _SSHFormatDSA(), 
 _SSH_ED25519: _SSHFormatEd25519(), 
 _ECDSA_NISTP256: _SSHFormatECDSA(b'nistp256', ec.SECP256R1()), 
 _ECDSA_NISTP384: _SSHFormatECDSA(b'nistp384', ec.SECP384R1()), 
 _ECDSA_NISTP521: _SSHFormatECDSA(b'nistp521', ec.SECP521R1())}

def _lookup_kformat(key_type):
    """Return valid format or throw error"""
    if not isinstance(key_type, bytes):
        key_type = memoryview(key_type).tobytes()
    if key_type in _KEY_FORMATS:
        return _KEY_FORMATS[key_type]
    raise UnsupportedAlgorithm('Unsupported key type: %r' % key_type)


_SSH_PRIVATE_KEY_TYPES = typing.Union[(
 ec.EllipticCurvePrivateKey,
 rsa.RSAPrivateKey,
 dsa.DSAPrivateKey,
 ed25519.Ed25519PrivateKey)]

def load_ssh_private_key(data: bytes, password: typing.Optional[bytes], backend: typing.Optional[Backend]=None) -> _SSH_PRIVATE_KEY_TYPES:
    """Load private key from OpenSSH custom encoding."""
    utils._check_byteslike('data', data)
    backend = _get_backend(backend)
    if password is not None:
        utils._check_bytes('password', password)
    m = _PEM_RC.search(data)
    if not m:
        raise ValueError('Not OpenSSH private key format')
    p1 = m.start(1)
    p2 = m.end(1)
    data = binascii.a2b_base64(memoryview(data)[p1:p2])
    if not data.startswith(_SK_MAGIC):
        raise ValueError('Not OpenSSH private key format')
    else:
        data = memoryview(data)[len(_SK_MAGIC):]
        ciphername, data = _get_sshstr(data)
        kdfname, data = _get_sshstr(data)
        kdfoptions, data = _get_sshstr(data)
        nkeys, data = _get_u32(data)
        if nkeys != 1:
            raise ValueError('Only one key supported')
        pubdata, data = _get_sshstr(data)
        pub_key_type, pubdata = _get_sshstr(pubdata)
        kformat = _lookup_kformat(pub_key_type)
        pubfields, pubdata = kformat.get_public(pubdata)
        _check_empty(pubdata)
        edata, data = _get_sshstr(data)
        _check_empty(data)
        if (
         ciphername, kdfname) != (_NONE, _NONE):
            ciphername = ciphername.tobytes()
            if ciphername not in _SSH_CIPHERS:
                raise UnsupportedAlgorithm('Unsupported cipher: %r' % ciphername)
            if kdfname != _BCRYPT:
                raise UnsupportedAlgorithm('Unsupported KDF: %r' % kdfname)
            blklen = _SSH_CIPHERS[ciphername][3]
            _check_block_size(edata, blklen)
            salt, kbuf = _get_sshstr(kdfoptions)
            rounds, kbuf = _get_u32(kbuf)
            _check_empty(kbuf)
            ciph = _init_cipher(ciphername, password, salt.tobytes(), rounds, backend)
            edata = memoryview(ciph.decryptor().update(edata))
        else:
            blklen = 8
            _check_block_size(edata, blklen)
    ck1, edata = _get_u32(edata)
    ck2, edata = _get_u32(edata)
    if ck1 != ck2:
        raise ValueError('Corrupt data: broken checksum')
    key_type, edata = _get_sshstr(edata)
    if key_type != pub_key_type:
        raise ValueError('Corrupt data: key type mismatch')
    private_key, edata = kformat.load_private(edata, pubfields, backend)
    comment, edata = _get_sshstr(edata)
    if edata != _PADDING[:len(edata)]:
        raise ValueError('Corrupt data: invalid padding')
    return private_key


def serialize_ssh_private_key(private_key: _SSH_PRIVATE_KEY_TYPES, password: typing.Optional[bytes]=None) -> bytes:
    """Serialize private key with OpenSSH custom encoding."""
    if password is not None:
        utils._check_bytes('password', password)
    else:
        if password:
            if len(password) > _MAX_PASSWORD:
                raise ValueError('Passwords longer than 72 bytes are not supported by OpenSSH private key format')
        if isinstance(private_key, ec.EllipticCurvePrivateKey):
            key_type = _ecdsa_key_type(private_key.public_key())
        else:
            if isinstance(private_key, rsa.RSAPrivateKey):
                key_type = _SSH_RSA
            else:
                if isinstance(private_key, dsa.DSAPrivateKey):
                    key_type = _SSH_DSA
                else:
                    if isinstance(private_key, ed25519.Ed25519PrivateKey):
                        key_type = _SSH_ED25519
                    else:
                        raise ValueError('Unsupported key type')
            kformat = _lookup_kformat(key_type)
            f_kdfoptions = _FragList()
            if password:
                ciphername = _DEFAULT_CIPHER
                blklen = _SSH_CIPHERS[ciphername][3]
                kdfname = _BCRYPT
                rounds = _DEFAULT_ROUNDS
                salt = os.urandom(16)
                f_kdfoptions.put_sshstr(salt)
                f_kdfoptions.put_u32(rounds)
                backend = _get_backend(None)
                ciph = _init_cipher(ciphername, password, salt, rounds, backend)
            else:
                ciphername = kdfname = _NONE
                blklen = 8
                ciph = None
        nkeys = 1
        checkval = os.urandom(4)
        comment = b''
        f_public_key = _FragList()
        f_public_key.put_sshstr(key_type)
        kformat.encode_public(private_key.public_key(), f_public_key)
        f_secrets = _FragList([checkval, checkval])
        f_secrets.put_sshstr(key_type)
        kformat.encode_private(private_key, f_secrets)
        f_secrets.put_sshstr(comment)
        f_secrets.put_raw(_PADDING[:blklen - f_secrets.size() % blklen])
        f_main = _FragList()
        f_main.put_raw(_SK_MAGIC)
        f_main.put_sshstr(ciphername)
        f_main.put_sshstr(kdfname)
        f_main.put_sshstr(f_kdfoptions)
        f_main.put_u32(nkeys)
        f_main.put_sshstr(f_public_key)
        f_main.put_sshstr(f_secrets)
        slen = f_secrets.size()
        mlen = f_main.size()
        buf = memoryview(bytearray(mlen + blklen))
        f_main.render(buf)
        ofs = mlen - slen
        if ciph is not None:
            ciph.encryptor().update_into(buf[ofs:mlen], buf[ofs:])
    txt = _ssh_pem_encode(buf[:mlen])
    buf[ofs:mlen] = bytearray(slen)
    return txt


_SSH_PUBLIC_KEY_TYPES = typing.Union[(
 ec.EllipticCurvePublicKey,
 rsa.RSAPublicKey,
 dsa.DSAPublicKey,
 ed25519.Ed25519PublicKey)]

def load_ssh_public_key(data: bytes, backend: typing.Optional[Backend]=None) -> _SSH_PUBLIC_KEY_TYPES:
    """Load public key from OpenSSH one-line format."""
    backend = _get_backend(backend)
    utils._check_byteslike('data', data)
    m = _SSH_PUBKEY_RC.match(data)
    if not m:
        raise ValueError('Invalid line format')
    key_type = orig_key_type = m.group(1)
    key_body = m.group(2)
    with_cert = False
    if _CERT_SUFFIX == key_type[-len(_CERT_SUFFIX):]:
        with_cert = True
        key_type = key_type[:-len(_CERT_SUFFIX)]
    kformat = _lookup_kformat(key_type)
    try:
        data = memoryview(binascii.a2b_base64(key_body))
    except (TypeError, binascii.Error):
        raise ValueError('Invalid key format')

    inner_key_type, data = _get_sshstr(data)
    if inner_key_type != orig_key_type:
        raise ValueError('Invalid key format')
    if with_cert:
        nonce, data = _get_sshstr(data)
    public_key, data = kformat.load_public(key_type, data, backend)
    if with_cert:
        serial, data = _get_u64(data)
        cctype, data = _get_u32(data)
        key_id, data = _get_sshstr(data)
        principals, data = _get_sshstr(data)
        valid_after, data = _get_u64(data)
        valid_before, data = _get_u64(data)
        crit_options, data = _get_sshstr(data)
        extensions, data = _get_sshstr(data)
        reserved, data = _get_sshstr(data)
        sig_key, data = _get_sshstr(data)
        signature, data = _get_sshstr(data)
    _check_empty(data)
    return public_key


def serialize_ssh_public_key(public_key: _SSH_PUBLIC_KEY_TYPES) -> bytes:
    """One-line public key format for OpenSSH"""
    if isinstance(public_key, ec.EllipticCurvePublicKey):
        key_type = _ecdsa_key_type(public_key)
    else:
        if isinstance(public_key, rsa.RSAPublicKey):
            key_type = _SSH_RSA
        else:
            if isinstance(public_key, dsa.DSAPublicKey):
                key_type = _SSH_DSA
            else:
                if isinstance(public_key, ed25519.Ed25519PublicKey):
                    key_type = _SSH_ED25519
                else:
                    raise ValueError('Unsupported key type')
    kformat = _lookup_kformat(key_type)
    f_pub = _FragList()
    f_pub.put_sshstr(key_type)
    kformat.encode_public(public_key, f_pub)
    pub = binascii.b2a_base64(f_pub.tobytes()).strip()
    return (b'').join([key_type, b' ', pub])