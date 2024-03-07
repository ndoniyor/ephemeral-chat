import ChatServiceClientHandler from "../chatServiceClient/chatServiceClientHandler";
import { createContext, useState, ReactNode, useContext } from "react";

const ChatClientContext = createContext<ChatServiceClientHandler>(
	new ChatServiceClientHandler()
);

export const ChatClientProvider = ({
	children,
	client,
}: {
	children: ReactNode;
	client: ChatServiceClientHandler;
}) => {
	const [chatClient] = useState(client);
	return (
		<ChatClientContext.Provider value={chatClient}>
			{children}
		</ChatClientContext.Provider>
	);
};

export const useChatClient = () => {
	return useContext(ChatClientContext);
};
