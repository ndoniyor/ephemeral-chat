import { useState } from "react";
import { useChatClient } from "../context/ChatClientContext";
import { Message } from "../chatServiceClient/generatedProtos/chat_service";

function UserCreationForm({ setConnectionStatus, setConversationID, setMessages }: { setConnectionStatus: Function, setConversationID: Function, setMessages: Function}) {
	
	const [username, setUsername] = useState("");

	const client = useChatClient()

	const handleConnect = async () => {
		client.setUser(username);
		const {status, conversationID, stream} = await client.connect()
		if(stream){
			stream.onMessage((message) => {
				setMessages((prevMessages: Message[]) => [...prevMessages, message]);
			});
			setConnectionStatus(status);
			setConversationID(conversationID);
		}
	};

	return (
		<div className="flex"> 
			<input
				id="username-field"
				placeholder="Enter username"
				className="input input-bordered w-full"
				onChange={(e) => {
					setUsername(e.target.value);
				}}
			/>
			<button
				className="btn btn-accent ml-5"
				onClick={handleConnect}
			>
				Enter
			</button>
		</div>
	);
}

export default UserCreationForm;
