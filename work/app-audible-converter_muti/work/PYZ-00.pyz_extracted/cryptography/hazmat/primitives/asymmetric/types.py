# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\primitives\asymmetric\types.py
import typing
from cryptography.hazmat.primitives.asymmetric import dsa, ec, ed25519, ed448, rsa
PUBLIC_KEY_TYPES = typing.Union[(
 dsa.DSAPublicKey,
 rsa.RSAPublicKey,
 ec.EllipticCurvePublicKey,
 ed25519.Ed25519PublicKey,
 ed448.Ed448PublicKey)]
PRIVATE_KEY_TYPES = typing.Union[(
 ed25519.Ed25519PrivateKey,
 ed448.Ed448PrivateKey,
 rsa.RSAPrivateKey,
 dsa.DSAPrivateKey,
 ec.EllipticCurvePrivateKey)]