<script lang="ts">
  import { ChatUser, Empty, Message } from "./chat/chat.js";
  import ChatClientServicer from './chat/chatClientServicer';

  const chatClient = new ChatClientServicer();
  let userName = '';

  const handleClick = async () => {
    chatClient.setUser(ChatUser.create({ username: userName }))
    const response = await chatClient.connect();
    
    console.log(response);
  };

</script> 

<main>
  <div>
    <input type="text" bind:value={userName} placeholder="Enter a username" />
    <button on:click={handleClick}>Enter</button>
  </div>
</main>


<style>

</style>