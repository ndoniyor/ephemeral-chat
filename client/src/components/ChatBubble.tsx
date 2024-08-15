import { ChatUser, Message } from "../chatServiceClient/generatedProtos/chat_service";
function ChatBubble({
	user,
	message,
}: {
	key: Number;
	user: ChatUser;
	message: Message;
}) {
	return user.username === message.senderID ? (
		<div className="chat chat-end">
            <div className="chat-header">{message.senderID}</div>
			<div className="chat-bubble">{message.message}</div>
		</div>
	) : (
		<div className="chat chat-start">
            <div className="chat-header">{message.senderID}</div>
			<div className="chat-bubble chat-bubble-accent">{message.message}</div>
		</div>
	);
}

export default ChatBubble;
