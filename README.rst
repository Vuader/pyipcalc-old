PyIPCalc
========
Project Status: Development

Quick Links
-----------

* `Website <http://pyipcalc.fwiw.co.za>`__.
* `GITHUB Code <https://github.com/vision1983/pyipcalc>`__.
* `Issues <https://github.com/vision1983/pyipcalc/issues>`__.

Installation
------------

PyIPCalc currently fully supports `CPython <https://www.python.org/downloads/>`__ 2.7.

A package is availible on PyPI.
Installing it is as simple as:

.. code:: bash

    $ pip install pyipcalc

Source Code
-----------

Code is hosted on `GitHub <https://github.com/vision1983/pyipcalc>`_. Making the code easy to browse, download, fork, etc. Pull requests are always welcome!

Clone the project like this:

.. code:: bash

    $ git clone https://github.com/vision1983/pyipcalc.git

Once you have cloned the repo or downloaded a tarball from GitHub, you
can install pyipcalc like this:

.. code:: bash

    $ cd pyipcalc
    $ pip install .

Or, if you want to edit the code, first fork the main repo, clone the fork
to your desktop, and then run the following to install it using symbolic
linking, so that when you change your code, the changes will be automagically
available to your app without having to reinstall the package:

.. code:: bash

    $ cd pyipcalc
    $ pip install -e .

You can manually test changes to pyipcalc by switching to the
directory of the cloned repo:

.. code:: bash

    $ cd pyipcalc/tests
    $ python test.py

Using PyIPCalc
--------------

.. code:: bash

	$ ipcalc.py 192.168.0.0/24
	PyIPCalc 0.0.0

		Network Prefix: 192.168.0.0/24
		Network Address: 192.168.0.0
		First IP Address: 192.168.0.1
		Last IP Address: 192.168.0.254
		Broadcast Address: 192.168.0.255
		Netmask: 255.255.255.0

IPV6
----
IPV6 is supported, you can simply just provide an IPV6 prefix.

Development Module
------------------
.. code:: python

	$ python
	>>> import pyipcalc
	>>> net = pyipcalc.IPNetwork('192.168.0.0/24')
	>>> print net.prefix()
	192.168.0.0/24
	>>> print net.network()
	192.168.0.0
	>>> print net.first()
	192.168.0.1
	>>> print net.last()
	192.168.0.254
	>>> print net.broadcast()
	192.168.0.255
	>>> print net.subnet()
	255.255.255.0

	>>> for ip in net:
	...     print ip
	... 
	192.168.0.0/32
	192.168.0.2/32
	........
	........
	192.168.0.254/32
	192.168.0.255/32
	>>>  

	>>> test = pyipcalc.IPIter('10.10.10.0/24',26)
	>>> for net in test:
	...     print net
	... 
	10.10.10.0/26
	10.10.10.64/26
	10.10.10.128/26
	10.10.10.192/26
	>>> 

	>>> test = pyipcalc.IPIter('10.10.10.0/24',26)
	>>> for net in test:
	...     print net.first()
	...     print net.last()
	... 
	10.10.10.1
	10.10.10.62
	10.10.10.65
	10.10.10.126
	10.10.10.129
	10.10.10.190
	10.10.10.193
	10.10.10.254
	>>> 

Converting IPv4 to 32bit Decimal to store in database.

.. code:: python

	>>> print pyipcalc.ip2dec('192.168.0.0',4)
	3232235520
	>>> print pyipcalc.dec2ip(3232235520,4)
	192.168.0.0
	>>> 

Converting IPv6 to 128bit Decimal to store in database.

.. code:: python

	>>> print pyipcalc.ip2dec('ffff:0000:0000:0000:0000:0000:0000:0000',6)
	340277174624079928635746076935438991360
	>>> print pyipcalc.dec2ip(340277174624079928635746076935438991360,6)
	ffff:0000:0000:0000:0000:0000:0000:0000

Typically you will need two 64bit columns in a database to store 128bit IPv6 address.

.. code:: python

	>>> print pyipcalc.dec128to64(340277174624079928635746076935438991360)
	[18446462598732840960L, 0L]
	>>> print pyipcalc.dec64to128(18446462598732840960L,0L)
	340277174624079928635746076935438991360

