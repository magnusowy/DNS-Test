import pytest
from resources.global_helpers import qname
from resources.dnsResolverFactory import ResolverFactory
@pytest.fixture(scope="session")
def NO_REPEATS():
    return 100

@pytest.fixture(scope="session")
def QNAME():
    return qname()

@pytest.fixture(scope="session")
def resolver_factory(tout=2.0, ltime=2.0):
    return ResolverFactory(timeout=tout, lifetime=ltime)

