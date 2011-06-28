//
//  ProtocolBuffers.h
//  RPCStub
//
//  Created by Julien Cayzac on 6/27/11.
//  Copyright 2011 -. All rights reserved.
//

#import <Foundation/Foundation.h>
#include <google/protobuf/message_lite.h>

@interface NSData (ProtocolBuffers)
+ (id) dataWithProtocolBuffer:(const ::google::protobuf::MessageLite *)message;
- (bool) parseProtocolBuffer:(::google::protobuf::MessageLite *)message;
@end
