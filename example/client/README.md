# Creating clients

## iOS clients

## Generate client code for the service

You can do it like this:

```bash
$ mkdir -p gen_rpc_client_cpp
$ protoc --plugin=path/to/protorpc-generator/bin/protoc-gen-rpc --rpc_out=objc:. --cpp_out=gen_rpc_client_cpp hello.proto
```

This will generate the client-side C++ and Objective-C++ code, but not the server-side Python code.

Then simply add the generated files to your project.

## Adding ObjC support code to your project

* Add the following source files from `support_objc` to your project:

```
NSData+ProtocolBuffers.h
NSData+ProtocolBuffers.mm
ProtoRPCConnection.h
ProtoRPCService.h
ProtoRPCService.mm
```

* Optional: if you don't want to implement the transport layer yourself, you can use the provided `DefaultProtoRPCConnection` by adding the two following files to your project. Otherwise you'll have to provide your own implementation of the `ProtoRPCConnection` protocol.

```
transport/DefaultProtoRPCConnection.h
transport/DefaultProtoRPCConnection.mm
```

## Adding libprotobuf-lite to your project

* Download [libprotobuf](http://code.google.com/p/protobuf/downloads/list) and uncompress the archive in your project directory. It will create a `protobuf-VERSION` directory, which I will call `protobuf-current` thereafter.
* Add `$(SRCROOT)/protobuf-current/src` to your project's header search paths.
* Add the following source files from protobuf-current/src (works for protobuf-2.4.1, YMMV):

```
extension_set.cc
generated_message_util.cc
message_lite.cc
repeated_field.cc
wire_format_lite.cc
io/coded_stream.cc
io/zero_copy_stream.cc
io/zero_copy_stream_impl_lite.cc
stubs/common.cc
stubs/once.cc
```

* Add `-I "$(SRCROOT)/protobuf-config"` to the CFLAGS of each of the files above (not on your whole project).

## Adding asi-http-request library to your project

If you don't plan to use the provided `DefaultProtoRPCConnection` transport layer, you don't need this.

* Get [asi-http-request](http://github.com/pokeb/asi-http-request/tree) and put it in your project directory.
* Add the following frameworks:

```
CFNetwork
SystemConfiguration
MobileCoreServices
CoreGraphics
libz.dylib
```

* Add the following source files from asi-http-request:

```
Classes/ASIAuthenticationDialog.h
Classes/ASIAuthenticationDialog.m
Classes/ASICacheDelegate.h
Classes/ASIDataCompressor.h
Classes/ASIDataCompressor.m
Classes/ASIDataDecompressor.h
Classes/ASIDataDecompressor.m
Classes/ASIDownloadCache.h
Classes/ASIDownloadCache.m
Classes/ASIFormDataRequest.h
Classes/ASIFormDataRequest.m
Classes/ASIHTTPRequest.h
Classes/ASIHTTPRequest.m
Classes/ASIHTTPRequestConfig.h
Classes/ASIHTTPRequestDelegate.h
Classes/ASIInputStream.h
Classes/ASIInputStream.m
Classes/ASINetworkQueue.h
Classes/ASINetworkQueue.m
Classes/ASIProgressDelegate.h
External/Reachability/Reachability.h
External/Reachability/Reachability.m
```

