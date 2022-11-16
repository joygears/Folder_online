# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: netbios.py
import sys, win32wnet, struct
NCBNAMSZ = 16
MAX_LANA = 254
NAME_FLAGS_MASK = 135
GROUP_NAME = 128
UNIQUE_NAME = 0
REGISTERING = 0
REGISTERED = 4
DEREGISTERED = 5
DUPLICATE = 6
DUPLICATE_DEREG = 7
LISTEN_OUTSTANDING = 1
CALL_PENDING = 2
SESSION_ESTABLISHED = 3
HANGUP_PENDING = 4
HANGUP_COMPLETE = 5
SESSION_ABORTED = 6
ALL_TRANSPORTS = 'M\x00\x00\x00'
MS_NBF = 'MNBF'
NCBCALL = 16
NCBLISTEN = 17
NCBHANGUP = 18
NCBSEND = 20
NCBRECV = 21
NCBRECVANY = 22
NCBCHAINSEND = 23
NCBDGSEND = 32
NCBDGRECV = 33
NCBDGSENDBC = 34
NCBDGRECVBC = 35
NCBADDNAME = 48
NCBDELNAME = 49
NCBRESET = 50
NCBASTAT = 51
NCBSSTAT = 52
NCBCANCEL = 53
NCBADDGRNAME = 54
NCBENUM = 55
NCBUNLINK = 112
NCBSENDNA = 113
NCBCHAINSENDNA = 114
NCBLANSTALERT = 115
NCBACTION = 119
NCBFINDNAME = 120
NCBTRACE = 121
ASYNCH = 128
NRC_GOODRET = 0
NRC_BUFLEN = 1
NRC_ILLCMD = 3
NRC_CMDTMO = 5
NRC_INCOMP = 6
NRC_BADDR = 7
NRC_SNUMOUT = 8
NRC_NORES = 9
NRC_SCLOSED = 10
NRC_CMDCAN = 11
NRC_DUPNAME = 13
NRC_NAMTFUL = 14
NRC_ACTSES = 15
NRC_LOCTFUL = 17
NRC_REMTFUL = 18
NRC_ILLNN = 19
NRC_NOCALL = 20
NRC_NOWILD = 21
NRC_INUSE = 22
NRC_NAMERR = 23
NRC_SABORT = 24
NRC_NAMCONF = 25
NRC_IFBUSY = 33
NRC_TOOMANY = 34
NRC_BRIDGE = 35
NRC_CANOCCR = 36
NRC_CANCEL = 38
NRC_DUPENV = 48
NRC_ENVNOTDEF = 52
NRC_OSRESNOTAV = 53
NRC_MAXAPPS = 54
NRC_NOSAPS = 55
NRC_NORESOURCES = 56
NRC_INVADDRESS = 57
NRC_INVDDID = 59
NRC_LOCKFAIL = 60
NRC_OPENERR = 63
NRC_SYSTEM = 64
NRC_PENDING = 255
UCHAR = 'B'
WORD = 'H'
DWORD = 'I'
USHORT = 'H'
ULONG = 'I'
ADAPTER_STATUS_ITEMS = [
 ('6s', 'adapter_address'),
 (
  UCHAR, 'rev_major'),
 (
  UCHAR, 'reserved0'),
 (
  UCHAR, 'adapter_type'),
 (
  UCHAR, 'rev_minor'),
 (
  WORD, 'duration'),
 (
  WORD, 'frmr_recv'),
 (
  WORD, 'frmr_xmit'),
 (
  WORD, 'iframe_recv_err'),
 (
  WORD, 'xmit_aborts'),
 (
  DWORD, 'xmit_success'),
 (
  DWORD, 'recv_success'),
 (
  WORD, 'iframe_xmit_err'),
 (
  WORD, 'recv_buff_unavail'),
 (
  WORD, 't1_timeouts'),
 (
  WORD, 'ti_timeouts'),
 (
  DWORD, 'reserved1'),
 (
  WORD, 'free_ncbs'),
 (
  WORD, 'max_cfg_ncbs'),
 (
  WORD, 'max_ncbs'),
 (
  WORD, 'xmit_buf_unavail'),
 (
  WORD, 'max_dgram_size'),
 (
  WORD, 'pending_sess'),
 (
  WORD, 'max_cfg_sess'),
 (
  WORD, 'max_sess'),
 (
  WORD, 'max_sess_pkt_size'),
 (
  WORD, 'name_count')]
NAME_BUFFER_ITEMS = [
 (
  str(NCBNAMSZ) + 's', 'name'),
 (
  UCHAR, 'name_num'),
 (
  UCHAR, 'name_flags')]
SESSION_HEADER_ITEMS = [
 (
  UCHAR, 'sess_name'),
 (
  UCHAR, 'num_sess'),
 (
  UCHAR, 'rcv_dg_outstanding'),
 (
  UCHAR, 'rcv_any_outstanding')]
SESSION_BUFFER_ITEMS = [
 (
  UCHAR, 'lsn'),
 (
  UCHAR, 'state'),
 (
  str(NCBNAMSZ) + 's', 'local_name'),
 (
  str(NCBNAMSZ) + 's', 'remote_name'),
 (
  UCHAR, 'rcvs_outstanding'),
 (
  UCHAR, 'sends_outstanding')]
LANA_ENUM_ITEMS = [
 ('B', 'length'),
 (
  str(MAX_LANA + 1) + 's', 'lana')]
FIND_NAME_HEADER_ITEMS = [
 (
  WORD, 'node_count'),
 (
  UCHAR, 'reserved'),
 (
  UCHAR, 'unique_group')]
FIND_NAME_BUFFER_ITEMS = [
 (
  UCHAR, 'length'),
 (
  UCHAR, 'access_control'),
 (
  UCHAR, 'frame_control'),
 ('6s', 'destination_addr'),
 ('6s', 'source_addr'),
 ('18s', 'routing_info')]
ACTION_HEADER_ITEMS = [
 (
  ULONG, 'transport_id'),
 (
  USHORT, 'action_code'),
 (
  USHORT, 'reserved')]
del UCHAR
del WORD
del DWORD
del USHORT
del ULONG
NCB = win32wnet.NCB

def Netbios(ncb):
    ob = ncb.Buffer
    is_ours = hasattr(ob, '_pack')
    if is_ours:
        ob._pack()
    try:
        return win32wnet.Netbios(ncb)
    finally:
        if is_ours:
            ob._unpack()


class NCBStruct:

    def __init__(self, items):
        self._format = ''.join([item[0] for item in items])
        self._items = items
        self._buffer_ = win32wnet.NCBBuffer(struct.calcsize(self._format))
        for format, name in self._items:
            if len(format) == 1:
                if format == 'c':
                    val = '\x00'
                else:
                    val = 0
            else:
                l = int(format[:-1])
                val = '\x00' * l
            self.__dict__[name] = val

    def _pack(self):
        vals = []
        for format, name in self._items:
            try:
                vals.append(self.__dict__[name])
            except KeyError:
                vals.append(None)

        self._buffer_[:] = (struct.pack)(*(self._format,) + tuple(vals))

    def _unpack(self):
        items = struct.unpack(self._format, self._buffer_)
        assert len(items) == len(self._items), 'unexpected number of items to unpack!'
        for (format, name), val in zip(self._items, items):
            self.__dict__[name] = val

    def __setattr__(self, attr, val):
        if attr not in self.__dict__:
            if attr[0] != '_':
                for format, attr_name in self._items:
                    if attr == attr_name:
                        break
                else:
                    raise AttributeError(attr)

        self.__dict__[attr] = val


def ADAPTER_STATUS():
    return NCBStruct(ADAPTER_STATUS_ITEMS)


def NAME_BUFFER():
    return NCBStruct(NAME_BUFFER_ITEMS)


def SESSION_HEADER():
    return NCBStruct(SESSION_HEADER_ITEMS)


def SESSION_BUFFER():
    return NCBStruct(SESSION_BUFFER_ITEMS)


def LANA_ENUM():
    return NCBStruct(LANA_ENUM_ITEMS)


def FIND_NAME_HEADER():
    return NCBStruct(FIND_NAME_HEADER_ITEMS)


def FIND_NAME_BUFFER():
    return NCBStruct(FIND_NAME_BUFFER_ITEMS)


def ACTION_HEADER():
    return NCBStruct(ACTION_HEADER_ITEMS)


def byte_to_int(b):
    """Given an element in a binary buffer, return its integer value"""
    if sys.version_info >= (3, 0):
        return b
    else:
        return ord(b)


if __name__ == '__main__':
    ncb = NCB()
    ncb.Command = NCBENUM
    la_enum = LANA_ENUM()
    ncb.Buffer = la_enum
    rc = Netbios(ncb)
    if rc != 0:
        raise RuntimeError('Unexpected result %d' % (rc,))
    for i in range(la_enum.length):
        ncb.Reset()
        ncb.Command = NCBRESET
        ncb.Lana_num = byte_to_int(la_enum.lana[i])
        rc = Netbios(ncb)
        if rc != 0:
            raise RuntimeError('Unexpected result %d' % (rc,))
        ncb.Reset()
        ncb.Command = NCBASTAT
        ncb.Lana_num = byte_to_int(la_enum.lana[i])
        ncb.Callname = '*               '.encode('ascii')
        adapter = ADAPTER_STATUS()
        ncb.Buffer = adapter
        Netbios(ncb)
        print('Adapter address:', end=' ')
        for ch in adapter.adapter_address:
            print(('%02x' % (byte_to_int(ch),)), end=' ')

        print()