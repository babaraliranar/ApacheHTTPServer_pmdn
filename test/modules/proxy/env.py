import inspect
import logging
import os

from pyhttpd.certs import CertificateSpec
from pyhttpd.env import HttpdTestEnv, HttpdTestSetup

log = logging.getLogger(__name__)


class ProxyTestSetup(HttpdTestSetup):

    def __init__(self, env: 'HttpdTestEnv'):
        super().__init__(env=env)
        self.add_source_dir(os.path.dirname(inspect.getfile(ProxyTestSetup)))
        self.add_modules(["proxy", "proxy_http", "proxy_wstunnel"])
        self.add_optional_modules(["lua"])


class ProxyTestEnv(HttpdTestEnv):

    def __init__(self, pytestconfig=None):
        super().__init__(pytestconfig=pytestconfig)
        self.add_httpd_conf([
                         ])
        self._d_reverse = f"reverse.{self.http_tld}"
        self._d_forward = f"forward.{self.http_tld}"
        self._d_mixed = f"mixed.{self.http_tld}"

        self.add_httpd_log_modules(["proxy", "proxy_http", "proxy_wstunnel", "core",
                                    "http", "http1", "lua"])
        self.add_cert_specs([
            CertificateSpec(domains=[
                self._d_forward, self._d_reverse, self._d_mixed
            ]),
            CertificateSpec(domains=[f"noh2.{self.http_tld}"], key_type='rsa2048'),
        ])

    def setup_httpd(self, setup: HttpdTestSetup = None):
        super().setup_httpd(setup=ProxyTestSetup(env=self))

    @property
    def d_forward(self):
        return self._d_forward

    @property
    def d_reverse(self):
        return self._d_reverse

    @property
    def d_mixed(self):
        return self._d_mixed
