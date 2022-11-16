# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\backends\openssl\x509.py
import datetime, warnings
from cryptography import utils, x509

def _Certificate(backend, x509) -> x509.Certificate:
    warnings.warn('This version of cryptography contains a temporary pyOpenSSL fallback path. Upgrade pyOpenSSL now.', utils.DeprecatedIn35)
    return backend._ossl2cert(x509)


def _CertificateSigningRequest(backend, x509_req) -> x509.CertificateSigningRequest:
    warnings.warn('This version of cryptography contains a temporary pyOpenSSL fallback path. Upgrade pyOpenSSL now.', utils.DeprecatedIn35)
    return backend._ossl2csr(x509_req)


def _CertificateRevocationList(backend, x509_crl) -> x509.CertificateRevocationList:
    warnings.warn('This version of cryptography contains a temporary pyOpenSSL fallback path. Upgrade pyOpenSSL now.', utils.DeprecatedIn35)
    return backend._ossl2crl(x509_crl)


class _RawRevokedCertificate(x509.RevokedCertificate):

    def __init__(self, serial_number: int, revocation_date: datetime.datetime, extensions: x509.Extensions):
        self._serial_number = serial_number
        self._revocation_date = revocation_date
        self._extensions = extensions

    @property
    def serial_number(self) -> int:
        return self._serial_number

    @property
    def revocation_date(self) -> datetime.datetime:
        return self._revocation_date

    @property
    def extensions(self) -> x509.Extensions:
        return self._extensions