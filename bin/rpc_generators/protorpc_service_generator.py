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
from google.protobuf.descriptor import FieldDescriptor
from sys import stderr
import re


class ProtoRPCServiceGenerator(object):
    """
    This generator produces a new Python module for each
    package, containing the ProtoRPC definitions.
    """

    # Maps fields types from google.protobuf to protorpc
    FIELD_TYPE_MAP = {
        FieldDescriptor.TYPE_DOUBLE: u'IntegerField',
        FieldDescriptor.TYPE_FLOAT: u'FloatField',
        FieldDescriptor.TYPE_INT64: u'IntegerField',
        FieldDescriptor.TYPE_UINT64: u'IntegerField',
        FieldDescriptor.TYPE_INT32: u'IntegerField',
        FieldDescriptor.TYPE_FIXED64: u'IntegerField',
        FieldDescriptor.TYPE_FIXED32: u'IntegerField',
        FieldDescriptor.TYPE_BOOL: u'BooleanField',
        FieldDescriptor.TYPE_STRING: u'StringField',
        FieldDescriptor.TYPE_MESSAGE: u'MessageField',
        FieldDescriptor.TYPE_BYTES: u'BytesField',
        FieldDescriptor.TYPE_UINT32: u'IntegerField',
        FieldDescriptor.TYPE_ENUM: u'EnumField',
        FieldDescriptor.TYPE_SFIXED32: u'IntegerField',
        FieldDescriptor.TYPE_SFIXED64: u'IntegerField',
        FieldDescriptor.TYPE_SINT32: u'IntegerField',
        FieldDescriptor.TYPE_SINT64: u'IntegerField',
    }

    def __init__(self):
        # We keep track of the files we created so far,
        # so we know when to use insertion points.
        self.created_files = {}

    def genEnum(self, x, t=0):
        """
        Generate a new class for an enum type
        """
        lines = \
            [u"%sclass %s(messages.Enum):" % ("    " * t, x.name)] + \
            [u"%s%s = %i" % (
                "    " * (t + 1),
                e.name,
                e.number
            ) for e in x.value] + \
            [u""]
        return lines

    def genExtension(self, x, t=0):
        """
        Generate an extension.
        Note: Not implemented.
        """
        raise NotImplementedError("Extensions not supported")

    def genExtensionRange(self, x, t=0):
        """
        Generate an extension range.
        Note: Not implemented.
        """
        raise NotImplementedError("Extensions not supported")

    def genField(self, x, t=0):
        """
        Generate a new field on a class.
        """
        if x.extendee:
            raise NotImplementedError("Extendees not supported")
        if x.options.ctype:
            raise NotImplementedError("'ctype' not supported")
        # Creates a list of parameters for the field
        kwargs = []
        if x.label == FieldDescriptor.LABEL_REQUIRED:
            kwargs += [u'required=True']
        if x.label == FieldDescriptor.LABEL_REPEATED:
            kwargs += [u'repeated=True']
        if x.default_value:
            value_type = ProtoRPCServiceGenerator.FIELD_TYPE_MAP[x.type]
            if value_type == 'BooleanField':
                v = x.default_value.lower()
                # I don't think '1' or 'yes' are allowed,
                # but better be safe than sorry
                if v == u'true' or v == u'1' or v == u'yes':
                    kwargs += [u'default=True']
            elif value_type == 'EnumField':
                kwargs += [u"default='%s'" % x.default_value]
            elif value_type == 'StringField':
                kwargs += [u"default=%s" % repr(x.default_value)]
            elif value_type == 'FloatField':
                kwargs += [u'default=float(%s)' % x.default_value]
            else:
                kwargs += [u'default=%s' % x.default_value]
        return [u"%s%s = messages.%s(%s%i%s)%s" % (
            "    " * t,
            x.name,
            ProtoRPCServiceGenerator.FIELD_TYPE_MAP[x.type],
            (x.type == FieldDescriptor.TYPE_MESSAGE or \
             x.type == FieldDescriptor.TYPE_ENUM) \
                and u"'%s'," % x.type_name[1:] \
                or u'',
            x.number,
            len(kwargs) \
                and u', %s' % ', '.join(kwargs) \
                or u'',
            x.options.deprecated \
                and u' # deprecated!' \
                or u''
        )]

    def genMessage(self, x, t=0):
        """
        Generate a new Python class corresponding to the specified message
        """
        lines = [
            u"%sclass %s(messages.Message):" % ("    " * t, x.name)
        ]
        for xx in x.enum_type:
            lines += self.genEnum(xx, t + 1)
        for xx in x.extension:
            lines += self.genExtension(xx, t + 1)
        for xx in x.extension_range:
            lines += self.genExtensionRange(xx, t + 1)
        for xx in x.nested_type:
            lines += self.genMessage(xx, t + 1)
        for xx in x.field:
            lines += self.genField(xx, t + 1)
        if not (x.enum_type or x.nested_type or x.field):
            lines += [u"%spass" % ("    " * (t + 1))]
        return lines + [u""]

    def genMethod(self, x, t=0):
        return [u"""\
%(tabs)s@remote.method('%(in)s', '%(out)s')
%(tabs)sdef %(name)s(self, request):
%(tabs)s    return self.implementation.%(name)s(request, self.state)
""" % {
    'tabs':"    " * t,
    'name':x.name,
    'in':x.input_type[1:],
    'out':x.output_type[1:]
}]

    def genService(self, x, package, t=0):
        lines = [u"""\
%(tabs)sclass %(class)s(remote.Service):
%(tabs)s    \"\"\"
%(tabs)s    Usage:
%(tabs)s        from google.appengine.ext import webapp
%(tabs)s        from google.appengine.ext.webapp import util
%(tabs)s        from protorpc.webapp import service_handlers
%(tabs)s
%(tabs)s        from gen_rpc_services import %(package)s
%(tabs)s        class %(class)sImpl(object):
%(tabs)s            # The constructor can accept any parameter you want.
%(tabs)s            # Here we pass a 'template' string used to
%(tabs)s            # build our responses.
%(tabs)s            def __init__(self, template):
%(tabs)s                self.template = template
%(tabs)s
%(tabs)s            # Assuming %(class)s defines the following method:
%(tabs)s            # rpc hello(HelloRequest) returns (HelloResponse);
%(tabs)s            def hello(self, request, state):
%(tabs)s                '''
%(tabs)s                "request" is a '%(package)s.HelloRequest' object.
%(tabs)s                "state" is a 'HttpRequestState' object.
%(tabs)s                '''
%(tabs)s                if state.headers['X-Boom']:
%(tabs)s                    raise RuntimeError('Boom!')
%(tabs)s                return %(package)s.HelloResponse(
%(tabs)s                    hello=self.template%%request.my_name
%(tabs)s                )
%(tabs)s
%(tabs)s        rpc_service_handlers = service_handlers.service_mapping([
%(tabs)s            # Service endpoint is /rpc/%(class)s
%(tabs)s            # If 'root' weren't specified,
%(tabs)s            # it would simply be /%(class)s
%(tabs)s            %(package)s.%(class)s.mapping(
%(tabs)s                root='/rpc',
%(tabs)s                implementation=%(class)sImpl("Hey, hello %%s!")
%(tabs)s            ),
%(tabs)s        ])
%(tabs)s
%(tabs)s        application = webapp.WSGIApplication(rpc_service_handlers)
%(tabs)s
%(tabs)s        def main():
%(tabs)s            util.run_wsgi_app(application)
%(tabs)s
%(tabs)s        if __name__ == '__main__':
%(tabs)s            main()
%(tabs)s    \"\"\"
%(tabs)s    def __init__(self, implementation):
%(tabs)s        self.implementation = implementation
%(tabs)s        self.state          = None
%(tabs)s
%(tabs)s    @classmethod
%(tabs)s    def mapping(cls, implementation, root=''):
%(tabs)s        if not implementation: # pragma: no cover
%(tabs)s            raise RuntimeError(
%(tabs)s            "No implementation provided for RPC service '%(class)s'"
%(tabs)s            )
%(tabs)s        if type==type(implementation): #pragma: no cover
%(tabs)s            # got a type, get an instance
%(tabs)s            implementation=implementation()
%(tabs)s        return (
%(tabs)s            '%%s/%(class)s'%%root,
%(tabs)s            cls.new_factory(implementation=implementation)
%(tabs)s        )
%(tabs)s
%(tabs)s    def initialize_request_state(self, state):
%(tabs)s        self.state = state
""" % {
    'tabs':"    " * t,
    'class':x.name,
    'package':package,
}]
        for xx in x.method:
            lines += self.genMethod(xx, t + 1)
        return lines

    def genFile(self, x, response):
        lines = []
        if not x.package in self.created_files:
            lines += [
                u"#!/usr/bin/env python",
                u"# coding=UTF-8\n",
                u"##################################################",
                u"# THIS FILE IS AUTO-GENERATED! DO NOT MODIFY IT! #",
                u"##################################################\n",
                u"from protorpc import messages, remote",
                u"package='%s'\n" % x.package,
            ]
        lines += [u"# Generated from %s" % x.name, ""]
        for xx in x.enum_type:
            lines += self.genEnum(xx)
        for xx in x.extension:
            lines += self.genExtension(xx)
        for xx in x.message_type:
            lines += self.genMessage(xx)
        for xx in x.service:
            lines += self.genService(xx, x.package)
        service_py = response.file.add()
        service_py.name = 'gen_rpc_services/%s.py' % x.package
        if x.package in self.created_files:
            service_py.insertion_point = "END"
        else:
            lines += [u"# @@protoc_insertion_point(END)"]
            self.created_files[x.package] = True
        service_py.content = u'\n'.join(
            lines + ["""
# vim: set fileencodings=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
"""]
        )

    def generate(self, request, response):
        m = response.file.add()
        m.name = 'gen_rpc_services/__init__.py'
        m.content = ''
        for i in range(0, len(request.proto_file)):
            self.genFile(request.proto_file[i], response)

# vim: set fileencodings=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
