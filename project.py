from setuptools import find_packages

config = {
        "name": "pyipcalc",
        "author": "Christiaan Frans Rademan",
        "author_email": "christiaan.rademan@gmail.com",
        "description": "Python IP Calculator Module",
        "license": "BSD 3-Clause",
        "include_package_data": True,
        "keywords": "ip calculator",
        "url": "http://pyipcalc.fwiw.co.za",
        "packages": find_packages(),
        "scripts": [
            'ipcalc.py'
            ],
        "classifiers": [
            "Topic :: Software Development :: Libraries",
            "Environment :: Other Environment",
            "Intended Audience :: Information Technology",
            "Intended Audience :: System Administrators",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7"
            "Programming Language :: Python :: 3"
            ]
        }
