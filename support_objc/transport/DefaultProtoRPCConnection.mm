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
    __block protorpc_success_handler_t success_copy = [success copy];
    __block protorpc_error_handler_t error_copy     = [error copy];
    [request setCompletionBlock:^{
        success_copy([request responseData]);
    }];
    [request setFailedBlock:^{
        error_copy([request error]);
    }];
    [request startAsynchronous];
}
@end
