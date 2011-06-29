# ProtoRPC generators
## How to generate the example service
Assuming you have installed *libprotobuf* on your machine, running the following:

    $ ./proto2rpc hello.proto

...will create these source files:

    gen_rpc_client_cpp:
        hello.pb.cc  hello.pb.h
    
    gen_rpc_client_objc:
        hello.rpc.h  hello.rpc.mm
    
    gen_rpc_services:
        __init__.py  hello.py

