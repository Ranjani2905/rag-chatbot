import React, { useState } from "react";
import axios from "axios";

const Chatbot = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { sender: "User", text: input };
    setMessages([...messages, userMessage]);

    try {
      const response = await axios.get(`http://localhost:8000/ask/?question=${input}`);
      const botMessage = { sender: "Bot", text: response.data.answers.join("\n") };
      setMessages([...messages, userMessage, botMessage]);
    } catch (error) {
      setMessages([...messages, userMessage, { sender: "Bot", text: "Error fetching response." }]);
    }

    setInput("");
  };

  return (
    <div style={{ padding: "20px", maxWidth: "500px", margin: "auto" }}>
      <div style={{ height: "300px", overflowY: "auto", border: "1px solid #ccc", padding: "10px" }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.sender === "User" ? "right" : "left", margin: "5px 0" }}>
            <strong>{msg.sender}: </strong> {msg.text}
          </div>
        ))}
      </div>
      <input type="text" value={input} onChange={(e) => setInput(e.target.value)} style={{ width: "80%" }} />
      <button onClick={sendMessage} style={{ width: "18%" }}>Send</button>
    </div>
  );
};

export default Chatbot;
