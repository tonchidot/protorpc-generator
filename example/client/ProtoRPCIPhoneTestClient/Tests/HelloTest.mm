//
//  HelloTest.m
//  ProtoRPCIPhoneTestClient
//
//  Created by Cayzac Julien on 7/1/11.
//  Copyright 2011 -. All rights reserved.
//

#import "HelloTest.h"
#import "hello.rpc.h"
#import "DefaultProtoRPCConnection.h"

@implementation HelloTest
- (void) testHelloMethod {
    [self prepare];
    DefaultProtoRPCConnection* transport = [[DefaultProtoRPCConnection alloc] init];
    HelloService* service = [[HelloService alloc]
                             initWithConnection:transport
                             baseUrl:[NSURL URLWithString:@"http://172.16.1.147:8081/rpc"]
                             ];
    ::hello::HelloRequest request;
    request.set_my_name("Julien");
    [service hello:&request
        success:^(const ::hello::HelloResponse* response) {
            GHAssertNotNULL(response, @"Got a NULL response");
            GHTestLog(@"Got response with .hello=[%s]", response->hello().c_str());
            [self notify:kGHUnitWaitStatusSuccess forSelector:@selector(testHelloMethod)];
        }
        error:^(NSError* error) {
            GHTestLog(@"Error :[%@]", error);
            [self notify:kGHUnitWaitStatusFailure forSelector:@selector(testHelloMethod)];
        }
    ];
    [self waitForStatus:kGHUnitWaitStatusSuccess timeout:60.0];
}
@end
