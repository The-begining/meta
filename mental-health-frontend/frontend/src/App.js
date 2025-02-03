import React, { useState } from "react";
import HeatMap from './HeatMap';
import "./App.css";


function App() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [consent, setConsent] = useState(false);
  const [showHeatMap, setShowHeatMap] = useState(false); // ✅ Toggle for Heat Map
  const userId = "user123"; // Mock User ID
  const [emotionMap, setEmotionMap] = useState([]);

  const fetchEmotionMap = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/emotion-map');
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      console.log("Fetched Emotion Map:", data);  // ✅ Debugging line
      setEmotionMap(data.map_data);
    } catch (error) {
      console.error("Error fetching emotion map:", error);
    }
  };


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
          const response = await fetch("http://127.0.0.1:8000/location", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              user_id: userId,
              latitude,
              longitude,
              stress_level: Math.floor(Math.random() * 10) + 1,
            }),
          });

          if (response.ok) {
            alert("✅ Location shared successfully!");
          } else {
            const errorData = await response.json();
            console.error("❌ Error from server:", errorData);
            alert(`❌ Server Error: ${errorData.error}`);
          }
        } catch (error) {
          console.error("❌ Network Error:", error);
          alert("❌ Failed to share location due to network error.");
        }
      }, (error) => {
        console.error("❌ Geolocation Error:", error);
        alert(`❌ Geolocation Error: ${error.message}`);
      });
    } else {
      alert("❌ Geolocation is not supported by your browser.");
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
            <button onClick={() => {
              setShowHeatMap(!showHeatMap);
              if (!showHeatMap) fetchEmotionMap();  // Fetch data when showing the map
            }}>
              {showHeatMap ? "❌ Hide Heat Map" : "🌍 View Emotion Map"}
            </button>
          </div>


          {showHeatMap && <HeatMap emotionMap={emotionMap} />}
           {/* ✅ Toggle Heat Map */}
        </div>
      )}
    </div>
  );
}

export default App;
