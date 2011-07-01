//
//  ProtocolBuffers.h
//  RPCStub
//
//  Created by Julien Cayzac on 6/27/11.
//  Copyright 2011 -. All rights reserved.
//

#import <Foundation/Foundation.h>
#include <google/protobuf/message_lite.h>

/// @brief Augment NSData with protocol buffers capabilities.
@interface NSData (ProtocolBuffers)

/// @brief Create a new NSData object holding the binary representation of a message.
/// @param message Protocol buffer message to serialize.
/// @return New NSData object holding the binary representation of the specified message.
+ (id) dataWithProtocolBuffer:(const ::google::protobuf::MessageLite *)message;

/// @brief Parse a protocol buffer message from the binary payload of this NSData object.
/// @param message Protocol buffer message to be filled.
/// @return <code>true</code> upon success, <code>false</code> upon failure.
- (bool) parseProtocolBuffer:(::google::protobuf::MessageLite *)message;
@end
