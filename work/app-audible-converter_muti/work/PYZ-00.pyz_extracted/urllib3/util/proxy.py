# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: urllib3\util\proxy.py
from .ssl_ import create_urllib3_context, resolve_cert_reqs, resolve_ssl_version

def connection_requires_http_tunnel(proxy_url=None, proxy_config=None, destination_scheme=None):
    """
    Returns True if the connection requires an HTTP CONNECT through the proxy.

    :param URL proxy_url:
        URL of the proxy.
    :param ProxyConfig proxy_config:
        Proxy configuration from poolmanager.py
    :param str destination_scheme:
        The scheme of the destination. (i.e https, http, etc)
    """
    if proxy_url is None:
        return False
    else:
        if destination_scheme == 'http':
            return False
        if proxy_url.scheme == 'https':
            if proxy_config:
                if proxy_config.use_forwarding_for_https:
                    return False
        return True


def create_proxy_ssl_context(ssl_version, cert_reqs, ca_certs=None, ca_cert_dir=None, ca_cert_data=None):
    """
    Generates a default proxy ssl context if one hasn't been provided by the
    user.
    """
    ssl_context = create_urllib3_context(ssl_version=(resolve_ssl_version(ssl_version)),
      cert_reqs=(resolve_cert_reqs(cert_reqs)))
    if not ca_certs:
        if not ca_cert_dir:
            if not ca_cert_data:
                if hasattr(ssl_context, 'load_default_certs'):
                    ssl_context.load_default_certs()
    return ssl_context