#!/usr/bin/env python
# coding=UTF-8
#
# Copyright 2011 Tonchidot Corporation. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS "AS IS" AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN
# NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of the copyright holders.
#
# author: Julien Cayzac https://github.com/jcayzac
from google.protobuf.compiler.plugin_pb2 import CodeGeneratorRequest
from google.protobuf.compiler.plugin_pb2 import CodeGeneratorResponse
from protorpc_service_generator import ProtoRPCServiceGenerator
from objc_client_generator import ObjCClientGenerator

GENERATORS = {
    'py': ProtoRPCServiceGenerator(),
    'objc': ObjCClientGenerator()
}


def generate(pb):
    request = CodeGeneratorRequest()
    request.ParseFromString(pb)
    response = CodeGeneratorResponse()

    keys = request.parameter \
        and request.parameter.split(',') \
        or GENERATORS.keys()

    for g in keys:
        try:
            GENERATORS[g].generate(request, response)
        except KeyError, e:
            raise KeyError(
                "Unknown generator: '%s'. Possible values are: [%s]" % \
                (g, ','.join(GENERATORS.keys()))
            )

    return response.SerializeToString()

# vim: set fileencodings=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
