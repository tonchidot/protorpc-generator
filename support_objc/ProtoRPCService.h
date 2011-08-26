// Copyright 2011 Tonchidot Corporation. All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
//    1. Redistributions of source code must retain the above copyright notice,
//       this list of conditions and the following disclaimer.
//
//    2. Redistributions in binary form must reproduce the above copyright
//       notice, this list of conditions and the following disclaimer in the
//       documentation and/or other materials provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS "AS IS" AND ANY EXPRESS
// OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
// OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN
// NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY
// DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
// ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
// THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
// The views and conclusions contained in the software and documentation are
// those of the authors and should not be interpreted as representing official
// policies, either expressed or implied, of the copyright holders.
//
// @author: Julien Cayzac https://github.com/jcayzac

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
