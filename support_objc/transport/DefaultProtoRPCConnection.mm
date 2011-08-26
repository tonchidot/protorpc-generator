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

#import "DefaultProtoRPCConnection.h"
#import "ASIHTTPRequest.h"

@implementation DefaultProtoRPCConnection
- (void)          invoke:(NSURL *)end_point
serializedProtocolBuffer:(NSData *)payload
                 success:(protorpc_success_handler_t)success
                   error:(protorpc_error_handler_t)error {
    NSLog(@"Invoking method at [%@]", [end_point absoluteString]);
    __block ASIHTTPRequest *request = [ASIHTTPRequest requestWithURL:end_point];
    [request addRequestHeader:@"Content-Type" value:@"application/x-google-protobuf"];
    [request setRequestMethod:@"POST"];
    [request appendPostData:payload];
//    [request shouldWaitToInflateCompressedResponses:NO];
    [request setShouldContinueWhenAppEntersBackground:YES];
    [request setNumberOfTimesToRetryOnTimeout:2];
    [request setCompletionBlock:^{
        if ([request responseStatusCode] == 200)
            success([request responseData]);
        else
            // For some reason, a HTTP error is not
            // a "failure"...
            error(
                [NSError errorWithDomain:@"HTTP"
                                    code:[request responseStatusCode]
                                userInfo:[request responseHeaders]]
            );
    }];
    [request setFailedBlock:^{
        error([request error]);
    }];
    [request startAsynchronous];
}
@end
