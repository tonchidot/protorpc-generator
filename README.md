# ProtoRPC generators
## Requirements
Well, of course, [libprotobuf](http://code.google.com/p/protobuf/).
If you install through [MacPorts](http://www.macports.org/), then this should be enough:

    $ sudo port install protobuf-cpp protobuf-pythonVERSION # protobuf-python25, protobuf-python26 or protobuf-python27

<strong>You should avoid installing the protobuf library for the same version of Python as your Google App Engine development server uses, as [it will conflict with another protobuf package bundled in the latter](http://code.google.com/p/googleappengine/issues/detail?id=860). I use Python 2.7 system wide and let GAE be the only thing that still uses old Python 2.5.</strong>

Note that the installation seems broken, so google.protobuf.compiler cannot be imported because of a missing file. You can create it with this command:

    $ sudo python -c 'import os, google.protobuf; open("%s/compiler/__init__.py"%google.protobuf.__path__[0], "w");'

## How to generate the example service
Running the following:

    $ cd example/app
    $ protoc --plugin=../../bin/protoc-gen-rpc --rpc_out=py:. hello.proto

...will create these source files:

    gen_rpc_services:
        __init__.py  hello.py

## How to generate the example client
Run the following:

    $ cd example/client/ProtoRPCIPhoneTestClient
    $ mkdir -p gen_rpc_client_cpp
    $ protoc --plugin=../../../bin/protoc-gen-rpc --rpc_out=objc:. --cpp_out=gen_rpc_client_cpp hello.proto
    $ open ProtoRPCIPhoneTestClient.xcodeproj

Then build the project in Xcode.

## Testing the example service
Assuming you running app.yaml on port 8081,

    $ echo "my_name:'$USER'" | \
        protoc --encode=hello.HelloRequest hello.proto | \
        curl 2>/dev/null -H 'content-type:application/x-google-protobuf' \
            --data-binary @- http://localhost:8081/rpc/HelloService.hello | \
        protoc --decode=hello.HelloResponse hello.proto
    hello: "Hey, hello jcayzac!"

