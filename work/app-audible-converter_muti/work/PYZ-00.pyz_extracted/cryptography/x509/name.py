# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\x509\name.py
import typing
from cryptography import utils
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.backends.interfaces import Backend
from cryptography.x509.oid import NameOID, ObjectIdentifier

class _ASN1Type(utils.Enum):
    UTF8String = 12
    NumericString = 18
    PrintableString = 19
    T61String = 20
    IA5String = 22
    UTCTime = 23
    GeneralizedTime = 24
    VisibleString = 26
    UniversalString = 28
    BMPString = 30


_ASN1_TYPE_TO_ENUM = {i.value:i for i in _ASN1Type}
_SENTINEL = object()
_NAMEOID_DEFAULT_TYPE = {NameOID.COUNTRY_NAME: _ASN1Type.PrintableString, 
 NameOID.JURISDICTION_COUNTRY_NAME: _ASN1Type.PrintableString, 
 NameOID.SERIAL_NUMBER: _ASN1Type.PrintableString, 
 NameOID.DN_QUALIFIER: _ASN1Type.PrintableString, 
 NameOID.EMAIL_ADDRESS: _ASN1Type.IA5String, 
 NameOID.DOMAIN_COMPONENT: _ASN1Type.IA5String}
_NAMEOID_TO_NAME = {NameOID.COMMON_NAME: 'CN', 
 NameOID.LOCALITY_NAME: 'L', 
 NameOID.STATE_OR_PROVINCE_NAME: 'ST', 
 NameOID.ORGANIZATION_NAME: 'O', 
 NameOID.ORGANIZATIONAL_UNIT_NAME: 'OU', 
 NameOID.COUNTRY_NAME: 'C', 
 NameOID.STREET_ADDRESS: 'STREET', 
 NameOID.DOMAIN_COMPONENT: 'DC', 
 NameOID.USER_ID: 'UID', 
 NameOID.EMAIL_ADDRESS: 'E'}

def _escape_dn_value(val: str) -> str:
    """Escape special characters in RFC4514 Distinguished Name value."""
    if not val:
        return ''
    else:
        val = val.replace('\\', '\\\\')
        val = val.replace('"', '\\"')
        val = val.replace('+', '\\+')
        val = val.replace(',', '\\,')
        val = val.replace(';', '\\;')
        val = val.replace('<', '\\<')
        val = val.replace('>', '\\>')
        val = val.replace('\x00', '\\00')
        if val[0] in ('#', ' '):
            val = '\\' + val
        if val[(-1)] == ' ':
            val = val[:-1] + '\\ '
        return val


class NameAttribute(object):

    def __init__(self, oid: ObjectIdentifier, value: str, _type=_SENTINEL) -> None:
        if not isinstance(oid, ObjectIdentifier):
            raise TypeError('oid argument must be an ObjectIdentifier instance.')
        else:
            if not isinstance(value, str):
                raise TypeError('value argument must be a str.')
            else:
                if oid == NameOID.COUNTRY_NAME or oid == NameOID.JURISDICTION_COUNTRY_NAME:
                    if len(value.encode('utf8')) != 2:
                        raise ValueError('Country name must be a 2 character country code')
                if _type == _SENTINEL:
                    _type = _NAMEOID_DEFAULT_TYPE.get(oid, _ASN1Type.UTF8String)
            raise isinstance(_type, _ASN1Type) or TypeError('_type must be from the _ASN1Type enum')
        self._oid = oid
        self._value = value
        self._type = _type

    @property
    def oid(self) -> ObjectIdentifier:
        return self._oid

    @property
    def value(self) -> str:
        return self._value

    @property
    def rfc4514_attribute_name(self) -> str:
        """
        The short attribute name (for example "CN") if available,
        otherwise the OID dotted string.
        """
        return _NAMEOID_TO_NAME.get(self.oid, self.oid.dotted_string)

    def rfc4514_string(self) -> str:
        """
        Format as RFC4514 Distinguished Name string.

        Use short attribute name if available, otherwise fall back to OID
        dotted string.
        """
        return '%s=%s' % (
         self.rfc4514_attribute_name,
         _escape_dn_value(self.value))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NameAttribute):
            return NotImplemented
        else:
            return self.oid == other.oid and self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash((self.oid, self.value))

    def __repr__(self) -> str:
        return '<NameAttribute(oid={0.oid}, value={0.value!r})>'.format(self)


class RelativeDistinguishedName(object):

    def __init__(self, attributes: typing.Iterable[NameAttribute]):
        attributes = list(attributes)
        if not attributes:
            raise ValueError('a relative distinguished name cannot be empty')
        if not all(isinstance(x, NameAttribute) for x in attributes):
            raise TypeError('attributes must be an iterable of NameAttribute')
        self._attributes = attributes
        self._attribute_set = frozenset(attributes)
        if len(self._attribute_set) != len(attributes):
            raise ValueError('duplicate attributes are not allowed')

    def get_attributes_for_oid(self, oid: ObjectIdentifier) -> typing.List[NameAttribute]:
        return [i for i in self if i.oid == oid]

    def rfc4514_string(self) -> str:
        """
        Format as RFC4514 Distinguished Name string.

        Within each RDN, attributes are joined by '+', although that is rarely
        used in certificates.
        """
        return '+'.join(attr.rfc4514_string() for attr in self._attributes)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RelativeDistinguishedName):
            return NotImplemented
        else:
            return self._attribute_set == other._attribute_set

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self._attribute_set)

    def __iter__(self) -> typing.Iterator[NameAttribute]:
        return iter(self._attributes)

    def __len__(self) -> int:
        return len(self._attributes)

    def __repr__(self) -> str:
        return '<RelativeDistinguishedName({})>'.format(self.rfc4514_string())


class Name(object):

    @typing.overload
    def __init__(self, attributes: typing.Iterable[NameAttribute]) -> None:
        pass

    @typing.overload
    def __init__(self, attributes: typing.Iterable[RelativeDistinguishedName]) -> None:
        pass

    def __init__(self, attributes: typing.Iterable[typing.Union[(NameAttribute, RelativeDistinguishedName)]]) -> None:
        attributes = list(attributes)
        if all(isinstance(x, NameAttribute) for x in attributes):
            self._attributes = [RelativeDistinguishedName([typing.cast(NameAttribute, x)]) for x in attributes]
        else:
            if all(isinstance(x, RelativeDistinguishedName) for x in attributes):
                self._attributes = typing.cast(typing.List[RelativeDistinguishedName], attributes)
            else:
                raise TypeError('attributes must be a list of NameAttribute or a list RelativeDistinguishedName')

    def rfc4514_string(self) -> str:
        """
        Format as RFC4514 Distinguished Name string.
        For example 'CN=foobar.com,O=Foo Corp,C=US'

        An X.509 name is a two-level structure: a list of sets of attributes.
        Each list element is separated by ',' and within each list element, set
        elements are separated by '+'. The latter is almost never used in
        real world certificates. According to RFC4514 section 2.1 the
        RDNSequence must be reversed when converting to string representation.
        """
        return ','.join(attr.rfc4514_string() for attr in reversed(self._attributes))

    def get_attributes_for_oid(self, oid: ObjectIdentifier) -> typing.List[NameAttribute]:
        return [i for i in self if i.oid == oid]

    @property
    def rdns(self) -> typing.List[RelativeDistinguishedName]:
        return self._attributes

    def public_bytes(self, backend: typing.Optional[Backend]=None) -> bytes:
        backend = _get_backend(backend)
        return backend.x509_name_bytes(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Name):
            return NotImplemented
        else:
            return self._attributes == other._attributes

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(tuple(self._attributes))

    def __iter__(self) -> typing.Iterator[NameAttribute]:
        for rdn in self._attributes:
            for ava in rdn:
                yield ava

    def __len__(self) -> int:
        return sum(len(rdn) for rdn in self._attributes)

    def __repr__(self) -> str:
        rdns = ','.join(attr.rfc4514_string() for attr in self._attributes)
        return '<Name({})>'.format(rdns)