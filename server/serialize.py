import struct
import json

from google.protobuf.json_format import Parse

from servicer.protos.chat_pb2 import ChatUser, Empty

# Define your message as a dictionary
message_dict = {"conversationID": "", "username": "joe mama"}

# Convert the dictionary to a JSON string
message_json = json.dumps(message_dict)

# Parse the JSON string into a protobuf message
message_proto = Parse(message_json, ChatUser())

# Serialize the protobuf message into a binary string
message_binary = message_proto.SerializeToString()

# Get the length of the binary string
message_length = len(message_binary)

# Create the body of the HTTP request
body = b"\x00" + struct.pack(">I", message_length) + message_binary

import base64

# Base64 encode the body
body_base64 = base64.b64encode(body)

# Convert the bytes object to a string
body_str = body_base64.decode('utf-8')

print(body_str)