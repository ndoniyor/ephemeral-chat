import ChatClientServicer from "../chat/chatClientServicer";
import React from "react";

const ChatClientContext = React.createContext<ChatClientServicer>(new ChatClientServicer());

export const ChatClientProvider = ({ children, client }: { children: React.ReactNode, client: ChatClientServicer }) => {
    const [chatClient] = React.useState(client);
    return <ChatClientContext.Provider value={chatClient}>{children}</ChatClientContext.Provider>;
};


export const useChatClient = () => {
    return React.useContext(ChatClientContext);
}