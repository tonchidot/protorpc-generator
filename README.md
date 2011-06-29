# ProtoRPC generators
## Requirements
Well, of course, [libprotobuf](http://code.google.com/p/protobuf/).
If you install through [MacPorts](http://www.macports.org/), then this should be enough:

    $ sudo port install protobuf-cpp protobuf-pythonVERSION # protobuf-python25, protobuf-python26 or protobuf-python27

## How to generate the example service
Running the following:

    $ ./proto2rpc hello.proto

...will create these source files:

    gen_rpc_client_cpp:
        hello.pb.cc  hello.pb.h
    
    gen_rpc_client_objc:
        hello.rpc.h  hello.rpc.mm
    
    gen_rpc_services:
        __init__.py  hello.py

