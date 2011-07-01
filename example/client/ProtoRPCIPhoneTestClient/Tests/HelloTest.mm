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
                             baseUrl:[NSURL URLWithString:@"http://julien.local:8081/rpc"]
                             ];
    ::hello::HelloRequest request;
    NSString* name=[[UIDevice currentDevice] name];
    __block NSString* expected = [NSString stringWithFormat:@"Hey, hello %@!", name];
    request.set_my_name([name UTF8String]);
    [service hello:&request
        success:^(const ::hello::HelloResponse* response) {
            GHAssertNotNULL(response, @"Got a NULL response");
            NSString* heyHello = [NSString stringWithUTF8String:response->hello().c_str()];
            GHTestLog(@"Got response with .hello=[%@]", heyHello);
            if ([heyHello isEqual:expected]) {
                [self notify:kGHUnitWaitStatusSuccess forSelector:@selector(testHelloMethod)];
            }
            else {
                [self notify:kGHUnitWaitStatusFailure forSelector:@selector(testHelloMethod)];
            }
            UIAlertView *alert = [[UIAlertView alloc]
                                       initWithTitle: nil
                                       message: heyHello
                                       delegate:nil
                                       cancelButtonTitle:@"OK"
                                       otherButtonTitles:nil];
            [alert show];
            [alert release];
        }
        error:^(NSError* error) {
            GHTestLog(@"Error :[%@]", error);
            [self notify:kGHUnitWaitStatusFailure forSelector:@selector(testHelloMethod)];
        }
    ];
    [self waitForStatus:kGHUnitWaitStatusSuccess timeout:60.0];
}
@end
