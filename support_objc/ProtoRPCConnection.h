//
//  ProtoRPCConnection.h
//  RPCStub
//
//  Created by Julien Cayzac on 6/27/11.
//  Copyright 2011 -. All rights reserved.
//

#import <Foundation/Foundation.h>

typedef void (^protorpc_success_handler_t)(NSData *);
typedef void (^protorpc_error_handler_t)(NSError *);

/// Protocol for implementing the RPC transport layer (HTTP[S], ...)
@protocol ProtoRPCConnection
@required
/// Implements RPC transport layer
/// @param end_point Remote method end point (e.g. http://around.me:8080/rpc/HelloService.myMethod)
/// @param payload   Request object, serialized as a protocol buffer.
/// @param success   Block that will be called with a NSData containing a response protocol buffer.
/// @param error     Block that will be called with a NSError if the connection or remote call fail.
- (void)          invoke:(NSURL *)end_point
serializedProtocolBuffer:(NSData *)payload
                 success:(protorpc_success_handler_t)success
                   error:(protorpc_error_handler_t)error;
@end
