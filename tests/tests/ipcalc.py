import logging
import unittest

import pyipcalc

log = logging.getLogger(__name__)


class IPCalc(unittest.TestCase):
    def test_ipv4_network(self):
        net = pyipcalc.IPNetwork('192.168.0.0/25')
        self.assertEqual('192.168.0.0/25', net.prefix())
        self.assertEqual('192.168.0.0', net.network())
        self.assertEqual('192.168.0.1', net.first())
        self.assertEqual('192.168.0.126', net.last())
        self.assertEqual('192.168.0.127', net.broadcast())
        self.assertEqual('255.255.255.128', net.subnet())
        self.assertEqual(3232235520, pyipcalc.ip2dec('192.168.0.0', 4))
        self.assertEqual('192.168.0.0', pyipcalc.dec2ip(3232235520, 4))
        self.assertEqual('255.255.255.128', net.subnet())

    def test_ipv6_network(self):
        net = pyipcalc.IPNetwork('fff0::/64')
        self.assertEqual('fff0:0000:0000:0000:0000:0000:0000:0000/64', net.prefix())
        self.assertEqual('fff0:0000:0000:0000:0000:0000:0000:0000', net.network())
        self.assertEqual('fff0:0000:0000:0000:0000:0000:0000:0000', net.first())
        self.assertEqual('fff0:0000:0000:0000:ffff:ffff:ffff:ffff', net.last())
        self.assertEqual(340199290171201906239764863564210241535L,
                         pyipcalc.ip2dec('fff0:0000:0000:0000:ffff:ffff:ffff:ffff',
                                        6))
        self.assertEqual('fff0:0000:0000:0000:ffff:ffff:ffff:ffff',
                         pyipcalc.dec2ip(340199290171201906239764863564210241535L,
                                        6))

