import { useState } from 'react';
import axios from 'axios';

function Chat({ userId }) {
    const [message, setMessage] = useState("");
    const [chat, setChat] = useState([]);

    const sendMessage = async () => {
        if (message.trim() === "") return;

        const response = await axios.post("http://localhost:8000/chat", {
            user_id: userId,
            message: message,
            consent: true
        });

        setChat([...chat, { role: "user", text: message }, { role: "ai", text: response.data.response }]);
        setMessage("");
    };

    const sendFeedback = async (index, rating) => {
        const feedback = chat[index];
        await axios.post("http://localhost:8000/feedback", {
            user_id: userId,
            prompt: feedback.text,
            response: chat[index + 1].text,
            rating: rating
        });
        alert("Feedback recorded!");
    };

    return (
        <div>
            <h2>AI Psychologist 🧠</h2>
            <div style={{ height: '300px', overflowY: 'scroll', border: '1px solid black', padding: '10px' }}>
                {chat.map((msg, index) => (
                    <p key={index} style={{ textAlign: msg.role === "user" ? "right" : "left" }}>
                        <strong>{msg.role === "user" ? "You" : "AI"}:</strong> {msg.text}
                        {msg.role === "ai" && (
                            <span>
                                {" "} | Rate:{" "}
                                <button onClick={() => sendFeedback(index - 1, 1)}>😡</button>
                                <button onClick={() => sendFeedback(index - 1, 3)}>😐</button>
                                <button onClick={() => sendFeedback(index - 1, 5)}>😊</button>
                            </span>
                        )}
                    </p>
                ))}
            </div>
            <input value={message} onChange={e => setMessage(e.target.value)} placeholder="Type your message..." />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
}

export default Chat;
