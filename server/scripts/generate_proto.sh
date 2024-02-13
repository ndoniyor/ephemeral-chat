pwd
realpath ../../protos/chat.proto
../virtualenv/bin/python3 -m grpc_tools.protoc -I ../../ --python_out=../servicer --grpc_python_out=../servicer ../../protos/chat.proto