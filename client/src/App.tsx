import { useState, useEffect } from "react";
import "./App.css";
import ChatClientServicer from "./chat/chatClientServicer";
import { Message } from "./chat/chat";

const chatClient = new ChatClientServicer();

function App() {
  const [connectionStatus, setConnectionStatus] = useState(false);
  const [conversationID, setConversationID] = useState("");
  const [username, setUsername] = useState("");
  const [messageToSend, setMessageToSend] = useState("");
  const [messageHistory, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    let isSubscribed = true;

    const receiveMessages
  }, []);

  const handleConnect = async () => {
    chatClient.setUser(username);
    const [status, id] = await chatClient.connect();
    setConnectionStatus(status as boolean);
    setConversationID(id as string);

    for await (let message of chatClient.receiveMessages()){
      setMessages(prevMessages => [...prevMessages, message]);
    }
  };

  const handleSendMessage = async () => {
    await chatClient.sendMessage(messageToSend);
  }



  return (
    <>
      <div>
        {connectionStatus ? (
          <div>
            <h2>You are connected to: {conversationID}</h2>
            <h3>Username: {username}</h3>
          </div>
        ) : (
          <h2>You are not connected</h2>
        )}
      </div>
      <div>
        {!connectionStatus ? (
          <div>
            <label htmlFor="username-field">Name:</label>
            <input
              id="username-field"
              onChange={(e) => {
                setUsername(e.target.value);
              }}
            />
            <button onClick={handleConnect}>Enter</button>
          </div>
        ) : (
          <div>
            <div>
              {messageHistory.map((message, index) => (
                <div key={index}>
                  <p>
                    [{message.senderID}]: {message.message}
                  </p>
                </div>
              ))}
            </div>
            <label htmlFor="message-field">[{username}]: </label>
            <input
              id="message-field"
              onChange={(e) => {
                setMessageToSend(e.target.value);
              }}
            />
            <button onClick={handleSendMessage}>Send</button>
          </div>
        )}
      </div>
    </>
  );
}

export default App;
