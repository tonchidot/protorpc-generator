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

enum ProtoRPCErrorCode {
    PROTORPC_NO_ERROR = 0,
    PROTORPC_FAILED_TO_PARSE_PROTOCOL_BUFFER,
};

@interface ProtoRPCService : NSObject {
    NSObject<ProtoRPCConnection>* connection;
    NSURL* baseUrl;
    NSString* name;
}
@property(nonatomic, retain) NSObject<ProtoRPCConnection>* connection;
@property(nonatomic, retain) NSURL* baseUrl;
@property(nonatomic, retain) NSString* name;

- (void) initWithConnection:(NSObject<ProtoRPCConnection> *)connection
             baseUrl:(NSURL *)baseUrl
                name:(NSString *)name;
- (NSURL *) urlForMethod:(NSString *)method;
@end

