import React, { useState } from "react";
import HeatMap from './HeatMap';
import "./App.css";

function App() {
    const [message, setMessage] = useState("");
    const [chatHistory, setChatHistory] = useState([]);
    const [showHeatMap, setShowHeatMap] = useState(false);
    const userId = "user123";

    const sendMessage = async () => {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, message }),
        });
        const data = await response.json();
        setChatHistory((prev) => [...prev, { sender: "user", text: message }, { sender: "bot", text: data.response }]);
        setMessage("");
    };

    return (
        <div className="App">
            <h1>Mental Health Chatbot 🤖</h1>
            <div className="chat-box">
                {chatHistory.map((msg, index) => (
                    <div key={index} className={msg.sender}>{msg.text}</div>
                ))}
            </div>
            <input value={message} onChange={(e) => setMessage(e.target.value)} />
            <button onClick={sendMessage}>Send</button>
            <button onClick={() => setShowHeatMap(!showHeatMap)}>
                {showHeatMap ? "Hide Heatmap" : "Show Heatmap"}
            </button>
            {showHeatMap && <HeatMap />}
        </div>
    );
}

export default App;
