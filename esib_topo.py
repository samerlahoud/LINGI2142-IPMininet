from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, ebgp_session, AF_INET6

class ESIBTopo(IPTopo):

    def build(self, *args, **kwargs):

        # Routers AS4
        as4r1 = self.bgp('as4r1')
        as4r2 = self.bgp('as4r2')
        as4r3 = self.bgp('as4r3')
        as4r4 = self.bgp('as4r4')
        as4r5 = self.addRouter('as4r5')
        as4r5.addDaemon(BGP, address_families=(AF_INET6(networks=('dead:beef::/32',)),))
        h1 = self.addHost('h1')

        # Routers AS3
        as3r1 = self.bgp('as3r1')
        as3r2 = self.bgp('as3r2')
        as3r3 = self.bgp('as3r3')

        # Routers AS2
        as2r1 = self.bgp('as2r1')
        as2r2 = self.bgp('as2r2')
        as2r3 = self.bgp('as2r3')

        # Routers AS1
        as1r1 = self.addRouter('as1r1')
        as1r1.addDaemon(BGP, address_families=(AF_INET6(networks=('cafe:deca::/32',)),))
        h2 = self.addHost('h2')
        as1r2 = self.bgp('as1r2')
        as1r3 = self.bgp('as1r3')

        # Links AS4
        self.addLink(as4r1, as4r5, igp_metric=5)
        self.addLink(as4r2, as4r5, igp_metric=5)
        self.addLink(as4r3, as4r5, igp_metric=1)
        self.addLink(as4r4, as4r5, igp_metric=5)
        self.addLink(as4r5, h1, params1={"ip": "dead:beef::/48"}, params2={"ip": "dead:beef::1/48"})

        # Links AS3
        self.addLink(as3r1, as3r2, igp_metric=5)
        self.addLink(as3r1, as3r3, igp_metric=5)
        self.addLink(as3r2, as3r3, igp_metric=5)

        # Links AS2
        self.addLink(as2r1, as2r2, igp_metric=15)
        self.addLink(as2r1, as2r3, igp_metric=5)

        # Links AS1
        self.addLink(as1r1, as1r3, igp_metric=20)
        self.addLink(as1r1, as1r2, igp_metric=5)
        self.addLink(as1r1, h2, params1={"ip": "cafe:deca::/48"}, params2={"ip": "cafe:deca::1/48"})

        # Inter-AS Links
        self.addLink(as4r4, as2r1)
        self.addLink(as4r3, as2r3)
        self.addLink(as4r2, as3r2)
        self.addLink(as4r1, as3r1)
        self.addLink(as3r3, as1r3)
        self.addLink(as2r2, as1r2)
        self.addLink(as2r3, as1r3)

        # Set AS-ownerships
        self.addAS(1, (as1r1, as1r2, as1r3))
        self.addAS(2, (as2r1, as2r2, as2r3))
        self.addAS(3, (as3r1, as3r2, as3r3))
        self.addAS(4, (as4r1, as4r2, as4r3, as4r4, as4r5))

        # Add iBGP full mesh
        self.addiBGPFullMesh(1, routers=[as1r1, as1r2, as1r3])
        self.addiBGPFullMesh(2, routers=[as2r1, as2r2, as2r3])
        self.addiBGPFullMesh(3, routers=[as3r1, as3r2, as3r3])
        self.addiBGPFullMesh(4, routers=[as4r1, as4r2, as4r3, as4r4, as4r5])

        # Add eBGP session
        ebgp_session(self, as4r4, as2r1)
        ebgp_session(self, as4r3, as2r3)
        ebgp_session(self, as4r2, as3r2)
        ebgp_session(self, as4r1, as3r1)
        ebgp_session(self, as3r3, as1r3)
        ebgp_session(self, as2r2, as1r2)
        ebgp_session(self, as2r3, as1r3)

        super(ESIBTopo, self).build(*args, **kwargs)

    def bgp(self, name):
        r = self.addRouter(name)
        r.addDaemon(BGP, address_families=(
            AF_INET6(redistribute=('connected',)),))
        return r
