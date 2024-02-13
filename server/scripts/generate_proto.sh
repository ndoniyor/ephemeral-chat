pwd
realpath ../protos/chat.proto
/opt/homebrew/anaconda3/envs/ephem-chat/bin/python -m grpc_tools.protoc -I ../ --python_out=./servicer/protos --grpc_python_out=./servicer/protos ../protos/chat.proto