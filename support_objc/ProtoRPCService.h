//
//  ProtoRPCService.h
//  RPCStub
//
//  Created by Julien Cayzac on 6/27/11.
//  Copyright 2011 -. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "ProtoRPCConnection.h"
#import "NSData+ProtocolBuffers.h"

// Error codes used in NSError objects produced by the framework
enum ProtoRPCErrorCode {
    PROTORPC_NO_ERROR = 0,
    PROTORPC_FAILED_TO_PARSE_PROTOCOL_BUFFER,
};

/// Base class for all RPC services, from which generated service
/// classes will derive.
/// It provides common properties used by all services and a
/// method to map remote method names to URLs.
@interface ProtoRPCService : NSObject {
	/// Object responsible for implementing the transport layer.
    NSObject<ProtoRPCConnection>* connection;
	/// Base URL for accessing remotes services (e.g. "https://around.me:8080/rpc")
    NSURL* baseUrl;
	/// Name of the service. Currently it is the same as the service's class name.
    NSString* name;
}
@property(nonatomic, retain) NSObject<ProtoRPCConnection>* connection;
@property(nonatomic, retain) NSURL* baseUrl;
@property(nonatomic, retain) NSString* name;

/// @brief Initialize a new service object.
/// @param connection An object that implements the {ProtoRPCConnection} protocol.
/// @param baseUrl    Base URL for accessing remotes services (e.g. "https://around.me:8080/rpc")
/// @param name       Name of the service. Currently it is the same as the service's class name.
- (id) initWithConnection:(NSObject<ProtoRPCConnection> *)connection
                  baseUrl:(NSURL *)baseUrl
                     name:(NSString *)name;

/// @brief Returns an URL for the specified remote method of the service.
/// @param method Remote method name.
/// @return Full URL for accessing said method.
- (NSURL *) urlForMethod:(NSString *)method;
@end
