import { useState } from 'react'
import { ChatClient} from './chat/client'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  const tryConnect = async () => {}

  return (
      <div className="App">
        <button onClick={tryConnect}>Click to connect</button>
      </div>
  )
}

export default App;
