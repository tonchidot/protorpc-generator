//
//  HelloTest.m
//  ProtoRPCIPhoneTestClient
//
//  Created by Cayzac Julien on 7/1/11.
//  Copyright 2011 -. All rights reserved.
//

#import "HelloTest.h"

@implementation HelloTest
@synthesize transport, baseURL, service;

- (id) init {
    if (self=[super init]) {
        self.transport = [[DefaultProtoRPCConnection alloc] init];

        UIAlertView *serverInputAlert = [[UIAlertView alloc] initWithTitle:@"RPC Server base URL"
                                                                message:@"\n\n\n"
                                                               delegate:self
                                                      cancelButtonTitle:nil
                                                      otherButtonTitles:@"OK", nil];
        serverInputAlert.autoresizesSubviews=YES;
        baseURL = [[UITextField alloc] initWithFrame:CGRectMake(16,83,252,25)];
        baseURL.font = [UIFont systemFontOfSize:18];
        baseURL.backgroundColor = [UIColor whiteColor];
        baseURL.keyboardAppearance = UIKeyboardAppearanceAlert;
        baseURL.delegate = self;
        baseURL.text = @"http://julien.local:8081/rpc";
        //baseURL.autoresizingMask=-1;
        [baseURL becomeFirstResponder];
        [serverInputAlert addSubview:baseURL];
        [serverInputAlert show];
        [serverInputAlert release];
        
    }
    return self;
}

- (void)alertView:(UIAlertView *)alertView didDismissWithButtonIndex:(NSInteger)buttonIndex {
    
    self.service = [[HelloService alloc]
                    initWithConnection:transport
                    baseUrl:[NSURL URLWithString:self.baseURL.text]
                    ];
}


- (void) testHelloMethod {
    [self prepare];
    
    ::hello::HelloRequest request;
    NSString* name=[[UIDevice currentDevice] name];
    __block NSString* expected = [NSString stringWithFormat:@"Hey, hello %@!", name];
    request.set_my_name([name UTF8String]);
    [service hello:&request
        success:^(const ::hello::HelloResponse* response) {
            GHAssertNotNULL(response, @"Got a NULL response");
            NSString* heyHello = [NSString stringWithUTF8String:response->hello().c_str()];
            GHTestLog(@"Got response with .hello=[%@]", heyHello);
            GHAssertEqualStrings(heyHello, expected, @"Got a response, but not the one we expected:\n\tExpected: [%@]\n\tGot: [%@]", expected, heyHello);
            [self notify:kGHUnitWaitStatusSuccess forSelector:@selector(testHelloMethod)];
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
