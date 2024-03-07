import { useState } from "react";
import { useChatClient } from "../context/ChatClientContext";
import { Message } from "../chat/protos/chat";

function SendMessageBox({setMessages}: {setMessages: Function}) {

    const [messageToSend, setMessageToSend] = useState("");
    
    const client = useChatClient()

    const handleSendMessage = async () => {
		const success = await client.sendMessage(messageToSend);
        
		if (success) {
			const message = Message.create({
				senderID: client.user.username,
				message: messageToSend,
			});

			setMessages((prevMessages: Message[]) => [...prevMessages, message]);
			setMessageToSend("");
		}
	};

	return (
		<div className="flex py-5">
			<input
				id="message-field"
				className="input input-bordered w-full"
				onChange={(e) => {
					setMessageToSend(e.target.value);
				}}
				value={messageToSend}
			/>
			<button className="btn btn-accent ml-5" onClick={handleSendMessage}>
				Send
			</button>
		</div>
	);
}

export default SendMessageBox;