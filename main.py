from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from protorpc.webapp import service_handlers
import sys

# Provides an implementation for hello.HelloService
from gen_rpc_services import hello

class HelloServiceImpl(object):
	def __init__(self, template):
		self.template = template
	def hello(self, request):
		return hello.HelloResponse(hello=self.template%request.my_name)

# Map the RPC services
rpc_service_handlers = service_handlers.service_mapping([
	('/HelloService', hello.HelloService.new_factory(implementation=HelloServiceImpl("Hey, hello %s!"))),
])

# Apply the service mappings to Webapp
application = webapp.WSGIApplication(rpc_service_handlers)

def main():
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()
