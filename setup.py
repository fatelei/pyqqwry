# -*- coding: utf8 -*-
"""
    pyqqwry
    ~~~~~~~

    Python Parse QQwry.dat.
"""

from setuptools import setup

from pyqqwry import __version__

setup(
    name="pyqqwry",
    version=__version__,
    author="fatelei",
    author_email="fatelei@gmail.com",
    description="Lookup location via ip using cz ip",
    install_requires=["pylru"],
    packages=["pyqqwry"],
    zip_safe=False,
    url="https://github.com/fatelei/pyqqwry",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries",
    ],
    license="BSD License"
)
