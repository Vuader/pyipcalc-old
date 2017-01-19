# Neutrino Framework
#
# Copyright (c) 2016, Christiaan Frans Rademan
# All rights reserved.
#
# LICENSE: (BSD3-Clause)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENTSHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
import logging
import unittest

import pyipcalc

log = logging.getLogger(__name__)


class IPCalc(unittest.TestCase):
    def test_ipv4_network(self):
        net = pyipcalc.IPNetwork('192.168.0.0/25')
        net2 = pyipcalc.IPNetwork('192.168.0.1/30')
        net3 = pyipcalc.IPNetwork('192.168.0.128/25')
        self.assertEqual('192.168.0.0/25', net.prefix())
        self.assertEqual('192.168.0.0', net.network())
        self.assertEqual('192.168.0.1', net.first())
        self.assertEqual('192.168.0.126', net.last())
        self.assertEqual('192.168.0.127', net.broadcast())
        self.assertEqual('255.255.255.128', net.subnet())
        self.assertEqual(3232235520, pyipcalc.ip2dec('192.168.0.0', 4))
        self.assertEqual('192.168.0.0', pyipcalc.dec2ip(3232235520, 4))
        self.assertEqual('255.255.255.128', net.subnet())
        self.assertEqual(True, net.contains(net2))
        self.assertEqual(False, net.contains(net3))
        self.assertEqual('192.168.0.0/24', pyipcalc.supernet(net,
                         net3).prefix())

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
