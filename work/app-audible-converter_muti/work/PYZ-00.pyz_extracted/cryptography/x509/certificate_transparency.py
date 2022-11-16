# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\x509\certificate_transparency.py
import abc, datetime
from cryptography import utils
from cryptography.hazmat.bindings._rust import x509 as rust_x509

class LogEntryType(utils.Enum):
    X509_CERTIFICATE = 0
    PRE_CERTIFICATE = 1


class Version(utils.Enum):
    v1 = 0


class SignedCertificateTimestamp(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def version(self) -> Version:
        """
        Returns the SCT version.
        """
        pass

    @abc.abstractproperty
    def log_id(self) -> bytes:
        """
        Returns an identifier indicating which log this SCT is for.
        """
        pass

    @abc.abstractproperty
    def timestamp(self) -> datetime.datetime:
        """
        Returns the timestamp for this SCT.
        """
        pass

    @abc.abstractproperty
    def entry_type(self) -> LogEntryType:
        """
        Returns whether this is an SCT for a certificate or pre-certificate.
        """
        pass


SignedCertificateTimestamp.register(rust_x509.Sct)