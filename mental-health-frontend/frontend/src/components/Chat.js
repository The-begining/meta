import { useState } from 'react';
import axios from 'axios';

function Chat() {
    const [message, setMessage] = useState("");
    const [chat, setChat] = useState([]);
    const userId = "user123"; // You can dynamically assign this

    const sendMessage = async () => {
        if (message.trim() === "") return;

        const response = await axios.post("http://localhost:8000/chat", {
            user_id: userId,
            message: message
        });

        setChat([...chat, { role: "user", text: message }, { role: "ai", text: response.data.response }]);
        setMessage("");
    };

    return (
        <div>
            <h2>AI Psychologist</h2>
            <div style={{ height: '300px', overflowY: 'scroll', border: '1px solid black', padding: '10px' }}>
                {chat.map((msg, index) => (
                    <p key={index} style={{ textAlign: msg.role === "user" ? "right" : "left" }}>
                        <strong>{msg.role === "user" ? "You" : "AI"}:</strong> {msg.text}
                    </p>
                ))}
            </div>
            <input value={message} onChange={e => setMessage(e.target.value)} placeholder="Type your message..." />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
}

export default Chat;
