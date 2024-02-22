import { ChatUser, Message } from "../chat/protos/chat";
import ChatBubble from "./ChatBubble";

function MessageBox({ user, messageList }: { user: ChatUser; messageList: Array<Message> }){
    return (
        <div className="flex-col">
            {
                messageList.map((message, index) => (
                    <ChatBubble key={index} user={user} message={message} />
                ))
            }
        </div>
    )
}

export default MessageBox;