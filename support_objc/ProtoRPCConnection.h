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

@protocol ProtoRPCConnection
- (void)          invoke:(NSURL *)end_point
serializedProtocolBuffer:(NSData *)payload
                 success:(protorpc_success_handler_t)success
                   error:(protorpc_error_handler_t)error;
@end
