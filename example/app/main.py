#!/usr/bin/env python
# coding=UTF-8
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from protorpc.webapp import service_handlers
import sys

# Implement HelloService

from gen_rpc_services import hello


class HelloServiceImpl(object):
    def __init__(self, template):
        self.template = template

    def hello(self, request, state):
        return hello.HelloResponse(
            hello=self.template % request.my_name
        )

# End of HelloService implementation


# Normal webapp handler
class TestHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("Foo!\n")


def main():
    util.run_wsgi_app(webapp.WSGIApplication(
        # RPC services go here
        service_handlers.service_mapping([
            hello.HelloService.mapping(
                root='/rpc',
                implementation=HelloServiceImpl("Hey, hello %s!")
            ),
        ])
        +
        # Normal webapp handlers go here
        [
            ('/Test', TestHandler),
        ]
    ))

if __name__ == '__main__':
    main()
