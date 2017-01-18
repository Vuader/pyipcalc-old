# PyIPCalc
#
# Copyright (c) 2017, Christiaan Frans Rademan.
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
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from .exceptions import IPPrefixError

log = logging.getLogger(__name__)


def block_size(cidr, version):
    size = None
    if version == 4:
        size = 32
    if version == 6:
        size = 128
    if size is not None:
        bits = size - cidr
        ips = pow(2, bits)
        return ips


def subnet(cidr):
    subnet_mask = 0xFFFFFFFF << (32 - cidr)
    mask_quads = []
    mask_quads.append(str(subnet_mask >> 24 & 0xFF))
    mask_quads.append(str(subnet_mask >> 16 & 0xFF))
    mask_quads.append(str(subnet_mask >> 8 & 0xFF))
    mask_quads.append(str(subnet_mask >> 0 & 0xFF))
    return ".".join(mask_quads)


def ip2dec(ip, version):
    if version == 4:
        ip = ip.split('.')
        num = 0
        for (i, value) in enumerate(ip):
            part = 8 * (i+1)
            value = int(value) * block_size(part, 4)
            num = value + num
        return num

    elif version == 6:
        ip = ip.split(':')
        num = 0
        for (i, value) in enumerate(ip):
            part = ((16) * (i+1))
            if value == '':
                value = 0
            value = int(str(value), 16)
            value = value * block_size(part, 6)
            num = value + num
        return num


def dec2ip(ip, version):
    if version == 4:
        ip1 = ip // pow(256, 3)
        ip2 = (ip % pow(256, 3)) // pow(256, 2)
        ip3 = (ip % pow(256, 3) % pow(256, 2)) // pow(256, 1)
        ip4 = (ip % pow(256, 3) % pow(256, 2) % pow(256, 1)) // pow(256, 0)
        ip = "%s.%s.%s.%s" % (ip1, ip2, ip3, ip4)
        return ip
    if version == 6:
        ip1 = str(hex(ip // pow(65536, 7))[2:]).rstrip('L').zfill(4)
        ip2 = str(hex((ip % pow(65536, 7)) //
                      pow(65536, 6))[2:]).rstrip('L').zfill(4)
        ip3 = str(hex((ip % pow(65536, 7) % pow(65536, 6)) //
                      pow(65536, 5))[2:]).rstrip('L').zfill(4)
        ip4 = str(hex((ip % pow(65536, 7) % pow(65536, 6) % pow(65536, 5)) //
                      pow(65536, 4))[2:]).rstrip('L').zfill(4)
        ip5 = str(hex((ip % pow(65536, 7) % pow(65536, 6) % pow(65536, 5) %
                      pow(65536, 4)) //
                      pow(65536, 3))[2:]).rstrip('L').zfill(4)
        ip6 = str(hex((ip % pow(65536, 7) % pow(65536, 6) %
                      pow(65536, 5) % pow(65536, 4) % pow(65536, 3)) //
                      pow(65536, 2))[2:]).rstrip('L').zfill(4)
        ip7 = str(hex((ip % pow(65536, 7) % pow(65536, 6) % pow(65536, 5) %
                      pow(65536, 4) % pow(65536, 3) % pow(65536, 2)) //
                      pow(65536, 1))[2:]).rstrip('L').zfill(4)
        ip8 = str(hex((ip % pow(65536, 7) % pow(65536, 6) % pow(65536, 5) %
                       pow(65536, 4) % pow(65536, 3) % pow(65536, 2) %
                       pow(65536, 1)) //
                      pow(65536, 0))[2:]).rstrip('L').zfill(4)
        ip = "%s:%s:%s:%s:%s:%s:%s:%s" % (ip1,
                                          ip2,
                                          ip3,
                                          ip4,
                                          ip5,
                                          ip6,
                                          ip7,
                                          ip8)
        return ip


def dec128to64(dec):
    dec1 = dec // pow(2, 64)
    dec2 = dec1 * pow(2, 64)
    dec2 = dec - dec2
    return [dec1, dec2]


def dec64to128(dec1, dec2):
    value = (dec1 * (pow(2, 64) + 1)) + dec2
    bitto64 = pow(2, 64)
    multiply = dec1 * bitto64
    value = multiply + dec2
    return value


def cidr2bin4(cidr):
    return str(bin(cidr))[2:].zfill(32)


def cidr2bin6(cidr):
    return str(bin(cidr))[2:].zfill(128)


def bin_nm2wm4(binary):
    binary = str(binary).rstrip('0')
    if '1' in binary:
        binary = str(binary).replace('1', '0')
        if len(binary) < 32:
            diff = 32 - len(binary)
            pad = diff * '1'
            binary = "%s%s" % (pad, binary)
        return binary
    else:
        return "1010101010101010101010101010101010101010"


def bin_nm2wm6(binary):
    binary = str(binary).rstrip('0')
    if '1' in binary:
        binary = str(binary).replace('1', '0')
        if len(binary) < 128:
            diff = 128 - len(binary)
            pad = diff * '1'
            binary = "%s%s" % (pad, binary)
        return binary
    else:
        return "1010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010"


def ip2bin4(ip):
    binary = bin(ip2dec(ip, 4))[2:]
    if len(binary) < 32:
        diff = 32 - len(binary)
        pad = diff * '0'
        binary = "%s%s" % (pad, binary)
    return binary


def bin2ip4(binary):
    dec = int(binary, 2)
    return dec2ip(dec, 4)


def bin2ip6(binary):
    dec = int(binary, 2)
    return dec2ip(dec, 6)


def ip2bin6(ip):
    binary = bin(ip2dec(ip, 6))[2:]
    if len(binary) < 128:
        diff = 128 - len(binary)
        pad = diff * '0'
        binary = "%s%s" % (pad, binary)
    return binary


def detect_version(prefix):
    if ":" in prefix:
        return 6
    elif "." in prefix:
        return 4
    else:
        raise IPPrefixError(prefix)


def validate_ip4(prefix):
    validate_prefix = prefix.split('/')
    if len(validate_prefix) != 2:
        raise IPPrefixError(prefix)
    else:
        mask = validate_prefix[1]
        if int(mask) < 0 or int(mask) > 32:
            raise IPPrefixError(prefix)
        validate_prefix = validate_prefix[0]
    validate_prefix = validate_prefix.split('.')

    if len(validate_prefix) == 4:
        for value in validate_prefix:
            value = int(value)
            if value > 255 or value < 0:
                raise IPPrefixError(prefix)
    else:
        raise IPPrefixError(prefix)

    return prefix


def validate_ip6(prefix):
    validate_prefix = prefix.split('/')
    if len(validate_prefix) != 2:
        raise IPPrefixError(prefix)
    else:
        mask = validate_prefix[1]
        if int(mask) < 0 or int(mask) > 128:
            raise IPPrefixError(prefix)
        validate_prefix = validate_prefix[0]

    if '::' in prefix:
        ip_values = len(validate_prefix[0])
        b,e = validate_prefix.split('::')
        ip_values = len(b.split(':')) + len(e.split(':'))
        diff = 8 - ip_values
        add = '0000:' * diff
        prefix = "%s:%s%s/%s" % (b,add,e,mask)
        validate_prefix = prefix.split('/')[0]
        validate_prefix = validate_prefix.split(':')
    else:
        validate_prefix = validate_prefix.split(':')

    if len(validate_prefix) != 8:
        raise IPPrefixError(prefix)

    for value in validate_prefix:
        if len(value) > 4:
            raise IPPrefixError(prefix)

    return prefix

def isPow2(n):
    return n and not (n & (n-1))

def supernet(ipn1,ipn2,min_cidr=None):
    for ip in (ipn1,ipn2):
        if not type(ip) is IPNetwork:
            raise IPPrefixError(ip)
    if ipn1.contains(ipn2):
	return ipn1
    elif ipn2.contains(ipn1):
	return ipn2
    else:
	if ipn1._version == 4:
		bitlength = 32
		min_cidr=min_cidr if isinstance(min_cidr,int) else 8
	elif ipn1._version == 6:
		bitlength = 128
		min_cidr=min_cidr if isinstance(min_cidr,int) else 16
	mask = (1 << ipn1._cidr) - 1
	mask <<= bitlength - ipn1._cidr
	pl = (1 << bitlength) - 1
        d1 = ip2dec(ipn1.ip_network,ipn1._version)
        d2 = ip2dec(ipn2.ip_network,ipn2._version)
	min_cidr = ipn1._cidr - min_cidr
	i = 0
	d1net = d1 & mask
	while d1net != d2 & mask and i < min_cidr:
		i +=1
		mask <<= 1
		mask &= pl
		d1net = d1 & mask
	if d1net == d2 & mask:
		cidr = ipn1._cidr - i
		return IPNetwork(dec2ip(d1net,ipn1._version)+"/"+str(cidr))
	else: #we did not find a common supernet within the search limits
		return None

class IPIter(object):
    def __init__(self, prefix, blocks=32):
        self._version = detect_version(prefix)
        if self._version == 4:
            self._prefix = validate_ip4(prefix)
        else:
            self._prefix = validate_ip6(prefix)
        self._ip, self._cidr = self._prefix.split('/')
        self._cidr = int(self._cidr)

        self._blocks = block_size(blocks, self._version)
        self._blocks_bits = blocks
        self._size = block_size(self._cidr, self._version)
        self._dec = ip2dec(self._ip, self._version)
        self._decend = self._dec + self._size - 1

    def __iter__(self):
        return self

    def next(self):
        if self._dec > self._decend:
            raise StopIteration
        else:
            ip = dec2ip(self._dec, self._version)
            self._dec += self._blocks
            net = "%s/%s" % (ip, self._blocks_bits)
            net = IPNetwork(net)
            return net


class IPNetwork(object):
    def __init__(self, prefix):
        version = detect_version(prefix)
        if version == 4:
            self._version = 4
            self._prefix = validate_ip4(prefix)
        else:
            self._version = 6
            self._prefix = validate_ip6(prefix)

        ip, self._cidr = self._prefix.split('/')
        self._cidr = int(self._cidr)

        if version == 4:
            bin_nmask = cidr2bin4(self._cidr)
            bin_wmask = bin_nm2wm4(bin_nmask)
            bin_host = ip2bin4(ip)

            self.bin_net = str(bin_host)[0:self._cidr]
            if len(self.bin_net) < 32:
                diff = 32 - len(self.bin_net)
                pad = diff * '0'
                self.bin_net = "%s%s" % (self.bin_net, pad)

            if self._cidr > 30:
                self.bin_bcast = None
            else:
                self.bin_bcast = str(bin_host)[0:self._cidr]
                if len(self.bin_bcast) < 32:
                    diff = 32 - len(self.bin_bcast)
                    pad = diff * '1'
                    self.bin_bcast = "%s%s" % (self.bin_bcast, pad)

            if self._cidr == 32:
                self.bin_first = self.bin_net
            elif self._cidr == 31:
                self.bin_first = self.bin_net
            else:
                self.bin_first = str(self.bin_net)[0:31]
                if len(self.bin_first) < 32:
                    diff = 32 - len(self.bin_first)
                    pad = diff * '1'
                    self.bin_first = "%s%s" % (self.bin_first, pad)

            if self._cidr == 32:
                self.bin_last = self.bin_net
            elif self._cidr == 31:
                self.bin_last = str(bin_host)[0:self._cidr]
                if len(self.bin_last) < 32:
                    diff = 32 - len(self.bin_last)
                    pad = diff * '1'
                    self.bin_last = "%s%s" % (self.bin_last, pad)
            else:
                self.bin_last = str(self.bin_bcast)[0:31]
                if len(self.bin_last) < 32:
                    diff = 32 - len(self.bin_last)
                    pad = diff * '0'
                    self.bin_last = "%s%s" % (self.bin_last, pad)

            if self.bin_bcast is not None:
                self.ip_broadcast = bin2ip4(self.bin_bcast)
            else:
                self.ip_broadcast = None

            self.ip_network = bin2ip4(self.bin_net)
            self.ip_first = bin2ip4(self.bin_first)
            self.ip_last = bin2ip4(self.bin_last)
        else:
            bin_nmask = cidr2bin6(self._cidr)
            bin_host = ip2bin6(ip)

            self.bin_net = str(bin_host)[0:self._cidr]
            if len(self.bin_net) < 128:
                diff = 128 - len(self.bin_net)
                pad = diff * '0'
                self.bin_net = "%s%s" % (self.bin_net, pad)

            self.bin_first = self.bin_net

            self.bin_last = str(bin_host)[0:self._cidr]
            if len(self.bin_last) < 128:
                diff = 128 - len(self.bin_last)
                pad = diff * '1'
                self.bin_last = "%s%s" % (self.bin_last, pad)

            self.ip_broadcast = None
            self.ip_network = bin2ip6(self.bin_net)
            self.ip_first = bin2ip6(self.bin_first)
            self.ip_last = bin2ip6(self.bin_last)

    def __iter__(self):
        return IPIter(self.prefix())

    def __string__(self):
        return str(self.prefix())

    def __repr__(self):
        return str(self.prefix())

    def prefix(self):
        prefix = "%s/%s" % (self.ip_network, self._cidr)
        return prefix

    def network(self):
        return self.ip_network

    def broadcast(self):
        return self.ip_broadcast

    def first(self):
        return self.ip_first

    def last(self):
        return self.ip_last

    def version(self):
        return self._version

    def subnet(self):
        if self._version == 4:
            return subnet(self._cidr)
        else:
            return None

    def contains(self,ip):
        if not type(ip) is IPNetwork:
            raise IPPrefixError(ip)
	else:
	    dec_ip = ip2dec(ip.ip_network,ip._version)
	if self._cidr == 32 or self._cidr == 128:
	  if ip._cidr == 32 or ip._cidr == 128:
	    if self.ip_network == ip.ip_network:
		return True
	    else:
		return False
	elif self._cidr == 31 or self._cidr == 127:
	  if ip._cidr == 31 or ip._cidr == 127:
	    if int(self.bin_last,2) - 1 == dec_ip:
		return True
	    else:
		return False
	else:
	    if dec_ip >= int(self.bin_net,2) and dec_ip <= int(self.bin_bcast,2):
		return True
	    else:
		return False
