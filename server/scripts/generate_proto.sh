pwd
/opt/homebrew/anaconda3/envs/ephem-chat/bin/python -m grpc_tools.protoc -I ./server/proto --python_out=./server/proto --grpc_python_out=./server/proto ./server/proto/chat.proto