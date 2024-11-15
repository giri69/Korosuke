import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './Chat.css';
import ReactMarkdown from 'react-markdown';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const chatBoxRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [scrollToBottom]);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const sendMessage = async () => {
    if (inputMessage.trim() === '') return;

    // Add user message to state
    const newUserMessage = { text: inputMessage, sender: 'user' };
    setMessages(prevMessages => [...prevMessages, newUserMessage]);
    setInputMessage('');

    try {
      // Send message to FastAPI endpoint (replace with your actual endpoint)
      const response = await axios.post('http://127.0.0.1:8000/ask', { name: inputMessage, username: localStorage.getItem('username') });

      const botResponse = response.data.message;
      console.log(botResponse);
      // Add bot response to state
      const newBotMessage = { text: botResponse, sender: 'bot' };
      setMessages(prevMessages => [...prevMessages, newBotMessage]);
    } catch (error) {
      console.error('Error fetching response:', error);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="App">
      <div className="chat-container">
        <div className="chat-box" ref={chatBoxRef}>
          <div className="message-container">
            {messages.map((message, index) => (
              <div key={index} className={`message ${message.sender}`}>
                <ReactMarkdown>{message.text}</ReactMarkdown>
              </div>
            ))}
          </div>
        </div>
        <div className="input-field">
          <input
            type="text"
            placeholder="Type your message..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            ref={inputRef}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;