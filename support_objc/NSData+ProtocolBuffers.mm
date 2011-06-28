//
//  ProtocolBuffers.m
//  RPCStub
//
//  Created by Julien Cayzac on 6/27/11.
//  Copyright 2011 -. All rights reserved.
//

#import "NSData+ProtocolBuffers.h"

@implementation NSData (ProtocolBuffers)
+ (id) dataWithProtocolBuffer:(const ::google::protobuf::MessageLite *)message {
    if (message) {
        NSMutableData* data = [NSMutableData dataWithCapacity:message->ByteSize()];
        data.length = message->GetCachedSize();
        if (message->SerializeToArray(data.mutableBytes, data.length))
            return data;
    }
	return nil;
}
- (bool) parseProtocolBuffer:(::google::protobuf::MessageLite *)message {
    if (message)
        return message->ParseFromArray(self.bytes, self.length);
    else
        return false;
}
@end
