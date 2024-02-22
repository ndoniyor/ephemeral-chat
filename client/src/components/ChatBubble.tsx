import { ChatUser, Message } from "../chat/protos/chat";

function ChatBubble({ user, message }: { key: Number, user: ChatUser; message: Message }) {
	return user.username === message.senderID ? (
		<div className="flex items-center justify-end text-right bac ">
            <div className="flex-col">
                <p>{message.senderID}: </p>
                <p>{message.message}</p>
            </div>
		</div>
	) : (
		<div className="flex items-center justify-start text-left">
            <div className="flex-col">
                <p>{message.senderID}: </p>
                <p>{message.message}</p>
            </div>
			
		</div>
	);
}

export default ChatBubble;
