# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos import chat_pb2 as protos_dot_chat__pb2


class ChatStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Connect = channel.unary_unary(
                '/grpc.Chat/Connect',
                request_serializer=protos_dot_chat__pb2.ChatUser.SerializeToString,
                response_deserializer=protos_dot_chat__pb2.ChatRoomInfo.FromString,
                )
        self.Disconnect = channel.unary_unary(
                '/grpc.Chat/Disconnect',
                request_serializer=protos_dot_chat__pb2.ChatUser.SerializeToString,
                response_deserializer=protos_dot_chat__pb2.ChatRoomInfo.FromString,
                )
        self.SendMessage = channel.unary_unary(
                '/grpc.Chat/SendMessage',
                request_serializer=protos_dot_chat__pb2.Message.SerializeToString,
                response_deserializer=protos_dot_chat__pb2.Empty.FromString,
                )
        self.SubscribeMessages = channel.unary_stream(
                '/grpc.Chat/SubscribeMessages',
                request_serializer=protos_dot_chat__pb2.ChatUser.SerializeToString,
                response_deserializer=protos_dot_chat__pb2.Message.FromString,
                )


class ChatServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Connect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Disconnect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribeMessages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChatServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Connect': grpc.unary_unary_rpc_method_handler(
                    servicer.Connect,
                    request_deserializer=protos_dot_chat__pb2.ChatUser.FromString,
                    response_serializer=protos_dot_chat__pb2.ChatRoomInfo.SerializeToString,
            ),
            'Disconnect': grpc.unary_unary_rpc_method_handler(
                    servicer.Disconnect,
                    request_deserializer=protos_dot_chat__pb2.ChatUser.FromString,
                    response_serializer=protos_dot_chat__pb2.ChatRoomInfo.SerializeToString,
            ),
            'SendMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.SendMessage,
                    request_deserializer=protos_dot_chat__pb2.Message.FromString,
                    response_serializer=protos_dot_chat__pb2.Empty.SerializeToString,
            ),
            'SubscribeMessages': grpc.unary_stream_rpc_method_handler(
                    servicer.SubscribeMessages,
                    request_deserializer=protos_dot_chat__pb2.ChatUser.FromString,
                    response_serializer=protos_dot_chat__pb2.Message.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'grpc.Chat', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Chat(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Connect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.Chat/Connect',
            protos_dot_chat__pb2.ChatUser.SerializeToString,
            protos_dot_chat__pb2.ChatRoomInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Disconnect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.Chat/Disconnect',
            protos_dot_chat__pb2.ChatUser.SerializeToString,
            protos_dot_chat__pb2.ChatRoomInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.Chat/SendMessage',
            protos_dot_chat__pb2.Message.SerializeToString,
            protos_dot_chat__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubscribeMessages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/grpc.Chat/SubscribeMessages',
            protos_dot_chat__pb2.ChatUser.SerializeToString,
            protos_dot_chat__pb2.Message.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
