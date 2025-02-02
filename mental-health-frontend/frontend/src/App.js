import React, { useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [consent, setConsent] = useState(false);
  const userId = "user123"; // Mock User ID

  // ✅ Send Message to Chatbot
  const sendMessage = async () => {
    if (!message.trim()) return;

    const newMessage = { sender: "user", text: message };
    setChatHistory((prevChat) => [...prevChat, newMessage]);
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, message, consent }),
      });

      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

      const data = await response.json();
      setChatHistory((prevChat) => [...prevChat, { sender: "bot", text: data.response }]);
    } catch (error) {
      console.error("Error:", error);
      setChatHistory((prevChat) => [...prevChat, { sender: "bot", text: "Sorry, something went wrong." }]);
    }
  };

  // ✅ Delete User Data
  const deleteData = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/delete-data/${userId}`, {
        method: "DELETE",
      });

      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

      alert("Your data has been deleted successfully.");
      setChatHistory((prevChat) => [...prevChat, { sender: "bot", text: "Your data has been deleted." }]);
    } catch (error) {
      console.error("Error:", error);
      setChatHistory((prevChat) => [...prevChat, { sender: "bot", text: "Failed to delete data." }]);
    }
  };

  // ✅ Fetch Emotional Trends
  const fetchEmotionalTrends = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/emotional-trends/${userId}`);

      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

      const data = await response.json();
      setChatHistory((prevChat) => [...prevChat, { sender: "bot", text: `Emotional Trend: ${data.trend}` }]);
    } catch (error) {
      console.error("Error:", error);
      setChatHistory((prevChat) => [...prevChat, { sender: "bot", text: "Failed to fetch emotional trends." }]);
    }
  };

  // ✅ Location Tracking
  const trackLocation = async () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(async (position) => {
        const { latitude, longitude } = position.coords;

        try {
          const stressLevel = Math.floor(Math.random() * 10) + 1; // Mock stress level (1-10)

          const response = await fetch("http://127.0.0.1:8000/location", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              user_id: userId,
              latitude,
              longitude,
              stress_level: stressLevel,
            }),
          });

          if (response.ok) {
            alert("✅ Location shared successfully!");
          } else {
            throw new Error("Failed to share location.");
          }
        } catch (error) {
          console.error("Location Error:", error);
          alert("Failed to share location.");
        }
      });
    } else {
      alert("Geolocation is not supported by your browser.");
    }
  };

  return (
    <div className="App">
      {!consent ? (
        <div className="consent-screen">
          <h1>Mental Health Chatbot 🤖</h1>
          <p>Do you consent to share anonymized data for mental health analysis?</p>
          <button onClick={() => setConsent(true)}>Yes, I Agree</button>
        </div>
      ) : (
        <div className="chat-container">
          <h1>Mental Health Chatbot</h1>

          <div className="chat-box">
            {chatHistory.map((msg, index) => (
              <div key={index} className={`chat-message ${msg.sender}`}>
                <span className="message-text">{msg.text}</span>
              </div>
            ))}
          </div>

          <div className="chat-input">
            <input
              type="text"
              placeholder="Type your message..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            />
            <button onClick={sendMessage}>Send</button>
          </div>

          <div className="action-buttons">
            <button onClick={fetchEmotionalTrends}>📊 View Emotional Trends</button>
            <button onClick={deleteData} style={{ color: "red" }}>🗑️ Delete My Data</button>
            <button onClick={trackLocation}>📍 Share My Location</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
