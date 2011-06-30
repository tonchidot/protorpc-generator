#!/usr/bin/env python
# coding=UTF-8
from google.protobuf.descriptor import FieldDescriptor
import re

class ObjCClientGenerator(object):
	def __init__(self):
		self.created_files = {}
	def generate(self, request, response):
		# Generate C++ header files list
		headers=['// Includes']
		for i in range(0, len(request.proto_file)):
			headers+=['#include "%s"'%request.proto_file[i].name.replace('.proto', '.pb.h')]
		# Generate ObjC header files
		for i in range(0, len(request.proto_file)):
			x=request.proto_file[i]
			gen_header=response.file.add()
			gen_source=response.file.add()
			gen_header.name='gen_rpc_client_objc/%s.rpc.h'%x.package
			gen_source.name='gen_rpc_client_objc/%s.rpc.mm'%x.package
			header_lines=[]
			source_lines=[]
			if not gen_header.name in self.created_files:
				header_lines+=[
					'// THIS FILE IS AUTO-GENERATED! DO NOT MODIFY IT!\n',
					'#import "ProtoRPCService.h"\n'
				] + headers + ['']
			if not gen_source.name in self.created_files:
				source_lines+=[
					'// THIS FILE IS AUTO-GENERATED! DO NOT MODIFY IT!\n',
					'#import "%s.rpc.h"\n'%x.package
				]
			header_lines+=[
				'// Interfaces generated from %s\n' % x.name,
			]
			source_lines+=[
				'// Source code generated from %s\n' % x.name,
			]
			for service in x.service:
				# The service is an ObjC class, as such we don't support
				# namespaces
				service_class=service.name.split('.')[-1]
				header_lines+=[
					"""\
/// %(service)s provides an interface for asynchronously invoking
/// methods on a remote server.
@interface %(service)s : ProtoRPCService

/// @brief Initialize a new %(service)s object.
/// @param connection An object that implements the {ProtoRPCConnection} protocol
/// @param baseUrl    Base URL for accessing remotes services (e.g. "https://around.me:8080/rpc")
- (void) initWithConnection:(NSObject<ProtoRPCConnection> *)connection
                    baseUrl:(NSURL *)baseUrl;
"""%{'service':service_class}
				]
				source_lines+=[
					"""\
@implementation %s
- (void) initWithConnection:(NSObject<ProtoRPCConnection> *)connection_
                    baseUrl:(NSURL *)baseUrl_ {
	// Initialize parent
	self = [super initWithConnection:connection_ baseUrl:baseUrl_ name:@"%s"];
	return self;
}
"""%(service_class,service_class)
				]
				for method in service.method:
					input_t = method.input_type.replace('.', '::')
					output_t = method.output_type.replace('.', '::')
					header_lines+=[
						"""\
/// @brief Asynchronnously invoke the %(service)s.%(name)s remote method.
/// @param request Request object, filled by the caller
/// @param success A block that will be called upon success with a response object.
/// @param failure A block that will be called in case of failure.
- (void) %(name)s:(const %(in)s *)request
	success:(void (^)(const %(out)s *))success
	error:(void (^)(NSError *))failure;
"""%{
	'service':service.name,
	'name':method.name,
	'in':input_t,
	'out':output_t
}
					]
					source_lines+=[
						"""\
- (void) %(method)s:(const %(in)s *)request
	success:(void (^)(const %(out)s *))success
	error:(void (^)(NSError *))failure {
	// Retrieve the full URL for the %(service)s.%(method)s remote method,
	// serialize the request as a protocol buffer,
	// transmit it asynchronously and have 'success'
	// and 'failure' blocks called upon success or failure.
	[self.connection invoke:[self urlForMethod:@"%(method)s"]
		serializedProtocolBuffer:[NSData dataWithProtocolBuffer:request]
		success:^(NSData* data) {
			%(out)s response;
			if ([data parseProtocolBuffer:&response])
				success(&response);
			else
				failure([NSError errorWithDomain:@"ProtoRPC" code:PROTORPC_FAILED_TO_PARSE_PROTOCOL_BUFFER userInfo:nil]);
		}
		error:^(NSError* error) {
			failure(error);
		}
	];
}
"""%{
	'service':service.name,
	'method':method.name,
	'in':input_t,
	'out':output_t
}
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
