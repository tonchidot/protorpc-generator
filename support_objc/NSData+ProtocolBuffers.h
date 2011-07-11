// Copyright 2011 Tonchidot Corporation. All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
//    1. Redistributions of source code must retain the above copyright notice,
//       this list of conditions and the following disclaimer.
//
//    2. Redistributions in binary form must reproduce the above copyright
//       notice, this list of conditions and the following disclaimer in the
//       documentation and/or other materials provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS "AS IS" AND ANY EXPRESS
// OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
// OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN
// NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY
// DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
// ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
// THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
// The views and conclusions contained in the software and documentation are
// those of the authors and should not be interpreted as representing official
// policies, either expressed or implied, of the copyright holders.
//
// @author: Julien Cayzac https://github.com/jcayzac

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
