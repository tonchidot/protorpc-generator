#/usr/env/bin python
from google.protobuf.compiler.plugin_pb2 import CodeGeneratorRequest, CodeGeneratorResponse
from protorpc_service_generator import ProtoRPCServiceGenerator
from objc_client_generator import ObjCClientGenerator

GENERATORS={
	'py':ProtoRPCServiceGenerator(),
	'objc':ObjCClientGenerator()
}

def generate(pb):
	request = CodeGeneratorRequest()
	request.ParseFromString(pb)
	response = CodeGeneratorResponse()
	
	keys=request.parameter and request.parameter.split(',') or GENERATORS.keys()
	for g in keys:
		try:
			GENERATORS[g].generate(request, response)
		except KeyError,e:
			raise KeyError("Unknown generator: '%s'. Possible values are: [%s]"%(g, ','.join(GENERATORS.keys())))
	return response.SerializeToString()
