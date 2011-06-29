#/usr/env/bin python
from google.protobuf.descriptor import FieldDescriptor
import re

class ObjCClientGenerator(object):
	def __init__(self):
		self.created_files = {}
	def generate(self, request, response):
		# Generate C++ header files list
		headers=[]
		for i in range(0, len(request.proto_file)):
			headers+=['#include "%s"'%request.proto_file[i].name.replace('.proto', '.pb.h')]
		# Generate ObjC header files
		for i in range(0, len(request.proto_file)):
			x=request.proto_file[i]
			gen_header=response.file.add()
			gen_source=response.file.add()
			gen_header.name='gen_rpc_client_objc/%s.rpc.h'%x.package
			gen_source.name='gen_rpc_client_objc/%s.rpc.mm'%x.package
			header_lines=[
				'// Generated from %s' % x.name,
			]
			source_lines=[
				'// Generated from %s' % x.name,
			]
			if not gen_header.name in self.created_files:
				header_lines+=[
					'#import "ProtoRPCService.h"'
				] + headers
			if not gen_source.name in self.created_files:
				source_lines+=[
					'#import "%s.rpc.h"'%x.package
				]
			for service in x.service:
				# The service is an ObjC class, as such we don't support
				# namespaces
				service_class=service.name.split('.')[-1]
				header_lines+=[
					"""
@interface %s : ProtoRPCService
- (void) initWithConnection:(NSObject<ProtoRPCConnection> *)connection
                    baseUrl:(NSURL *)baseUrl;
"""%service_class
				]
				source_lines+=[
					"""
@implementation %s
- (void) initWithConnection:(NSObject<ProtoRPCConnection> *)connection_
                    baseUrl:(NSURL *)baseUrl_ {
	self = [super initWithConnection:connection_ baseUrl:baseUrl_ name:@%s];
	return self;
}
"""%(service_class,service_class)
				]
				for method in service.method:
					input_t = method.input_type.replace('.', '::')
					output_t = method.output_type.replace('.', '::')
					header_lines+=[
						"""- (void) %s:(const %s *)request
	success:(void (^)(const %s *))success
	error:(void (^)(NSError *))failure;"""%(method.name, input_t, output_t)
					]
					source_lines+=[
						"""- (void) %(method)s:(const %(in)s *)request
	success:(void (^)(const %(out)s *))success
	error:(void (^)(NSError *))failure {
	[self.connection invoke:[self urlForMethod:@%(method)s]
		serializedProtocolBuffer:[NSData dataWithProtocolBuffer:request]
		success:^(NSData* data) {
			%(out)s response;
			if ([data parseProtocolBuffer:&response])
				success(&response);
			else
				failure([NSError errorWithDomain:@"ProtoRPC" code: PROTORPC_FAILED_TO_PARSE_PROTOCOL_BUFFER userInfo:nil]);
		}
		error:^(NSError* error) {
			failure(error);
		}
	];
}"""%{'method':method.name, 'in':input_t, 'out':output_t}
					]
				header_lines+=[ "@end" ]
				source_lines+=[ "@end" ]
			if gen_header.name in self.created_files:
				gen_header.insertion_point = "END"
			else:
				header_lines+=["// @@protoc_insertion_point(END)"]
				self.created_files[gen_header.name]=True
			if gen_source.name in self.created_files:
				gen_source.insertion_point = "END"
			else:
				source_lines+=["// @@protoc_insertion_point(END)"]
				self.created_files[gen_source.name]=True
			gen_header.content='\n'.join(header_lines)
			gen_source.content='\n'.join(source_lines)
