#!/usr/bin/env python
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

import argparse

import pyipcalc

app = "\033[1;32;40mPyIPCalc %s\033[0m" % (pyipcalc.version,)

def main():
    parser = argparse.ArgumentParser(description=app)
    parser.add_argument('prefix', help='IPv4 / IPv6 in CIDR Notation')
    args = parser.parse_args()
    if args is not None:
        print("%s\n" % app)
        ipn = pyipcalc.IPNetwork(args.prefix)
        print("\t\033[1mNetwork Prefix: \033[0;33;40m%s\033[0m" % (ipn.prefix(),))
        print("\t\033[1mNetwork Address: \033[0;33;40m%s\033[0m" % (ipn.network(),))
        print("\t\033[1mFirst IP Address: \033[0;33;40m%s\033[0m" % (ipn.first(),))
        print("\t\033[1mLast IP Address: \033[0;33;40m%s\033[0m" % (ipn.last(),))
        print("\t\033[1mBroadcast Address: \033[0;33;40m%s\033[0m" % (ipn.broadcast(),))
        print("\t\033[1mNetmask: \033[0;33;40m%s\033[0m" % (ipn.subnet(),))
        print("")

if __name__ == "__main__":
    main()
