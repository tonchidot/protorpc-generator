//
//  ProtoRPCService.m
//  RPCStub
//
//  Created by Julien Cayzac on 6/27/11.
//  Copyright 2011 -. All rights reserved.
//

#import "ProtoRPCService.h"

@implementation ProtoRPCService
@synthesize connection, baseUrl, name;

- (void) initWithConnection:(NSObject<ProtoRPCConnection> *)connection_
                    baseUrl:(NSURL *)baseUrl_
                       name:(NSString *)name_ {
    if (self = [super init]) {
        self.connection = connection_;
        self.baseUrl    = baseUrl_;
        self.name       = name_;
    }
    return self;
}

- (NSURL *) urlForMethod:(NSString *)method {
	/// This conforms to ProtoRPC way of doing things.
    return [NSURL URLWithString:[NSString stringWithFormat:@"/%@.%@", self.name, method]
                  relativeToURL:self.baseUrl];
}

@end
