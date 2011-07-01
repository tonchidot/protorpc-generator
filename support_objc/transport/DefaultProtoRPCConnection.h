#import "ProtoRPCConnection.h"

@interface DefaultProtoRPCConnection: NSObject<ProtoRPCConnection>
- (void)          invoke:(NSURL *)end_point
serializedProtocolBuffer:(NSData *)payload
                 success:(protorpc_success_handler_t)success
                   error:(protorpc_error_handler_t)error;
@end
