#!/usr/bin/env python

from distutils.core import setup


setup(name='protorpc-generator',
    version='1.0',
    description='ProtoRPC generator',
    package_dir = {'': 'bin'},
    packages=['rpc_generators'],
    scripts=['bin/protoc-gen-rpc', 'bin/proto2rpc'],
    install_requires=[
        'protobuf>=2.4.1',
    ],
    )
