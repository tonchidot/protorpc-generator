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

typedef void (^protorpc_success_handler_t)(NSData *);
typedef void (^protorpc_error_handler_t)(NSError *);

/// Protocol for implementing the RPC transport layer (HTTP[S], ...)
@protocol ProtoRPCConnection
@required
/// Implements RPC transport layer
/// @param end_point Remote method end point (e.g. http://around.me:8080/rpc/HelloService.myMethod)
/// @param payload   Request object, serialized as a protocol buffer.
/// @param success   Block that will be called with a NSData containing a response protocol buffer.
/// @param error     Block that will be called with a NSError if the connection or remote call fail.
- (void)          invoke:(NSURL *)end_point
serializedProtocolBuffer:(NSData *)payload
                 success:(protorpc_success_handler_t)success
                   error:(protorpc_error_handler_t)error;
@end
