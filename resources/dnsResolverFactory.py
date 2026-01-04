import dns.resolver

class ResolverFactory:
    def __init__(self, timeout=2.0, lifetime=2.0):
        self.timeout = timeout
        self.lifetime = lifetime

    def create(self, nameservers):
        r_obj = dns.resolver.Resolver(configure=False)
        r_obj.nameservers = list(nameservers)
        r_obj.timeout = self.timeout
        r_obj.lifetime = self.lifetime
        r_obj.cache = None # no cache for client
        return r_obj