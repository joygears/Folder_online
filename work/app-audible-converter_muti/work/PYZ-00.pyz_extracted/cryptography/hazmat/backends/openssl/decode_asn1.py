# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\backends\openssl\decode_asn1.py
from cryptography import x509
_DISTPOINT_TYPE_FULLNAME = 0
_DISTPOINT_TYPE_RELATIVENAME = 1
_CRL_ENTRY_REASON_ENUM_TO_CODE = {x509.ReasonFlags.unspecified: 0, 
 x509.ReasonFlags.key_compromise: 1, 
 x509.ReasonFlags.ca_compromise: 2, 
 x509.ReasonFlags.affiliation_changed: 3, 
 x509.ReasonFlags.superseded: 4, 
 x509.ReasonFlags.cessation_of_operation: 5, 
 x509.ReasonFlags.certificate_hold: 6, 
 x509.ReasonFlags.remove_from_crl: 8, 
 x509.ReasonFlags.privilege_withdrawn: 9, 
 x509.ReasonFlags.aa_compromise: 10}