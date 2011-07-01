//
//  HelloTest.h
//  ProtoRPCIPhoneTestClient
//
//  Created by Cayzac Julien on 7/1/11.
//  Copyright 2011 -. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <GHUnitIOS/GHUnit.h>
#import "DefaultProtoRPCConnection.h"
#import "hello.rpc.h"

@interface HelloTest : GHAsyncTestCase<UITextFieldDelegate, UIAlertViewDelegate> {
    DefaultProtoRPCConnection* transport;
    UITextField* baseURL;
    HelloService* service;
}
@property(nonatomic,retain) DefaultProtoRPCConnection* transport;
@property(nonatomic,retain) UITextField* baseURL;
@property(nonatomic,retain) HelloService* service;
@end
