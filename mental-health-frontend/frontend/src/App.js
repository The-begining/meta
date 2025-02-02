import React, { useState } from 'react';

function App() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [consent, setConsent] = useState(false);
  const userId = "user123";  // Mock User ID

  const sendMessage = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, message: message, consent: consent })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setChatHistory([...chatHistory, { sender: 'You', text: message }, { sender: 'Bot', text: data.response }]);
      setMessage('');
    } catch (error) {
      console.error("Error:", error);
      setChatHistory([...chatHistory, { sender: 'Bot', text: "Sorry, something went wrong." }]);
    }
  };

  const deleteData = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/delete-data/${userId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      alert("Your data has been deleted successfully.");
      setChatHistory([...chatHistory, { sender: 'Bot', text: "Your data has been deleted." }]);
    } catch (error) {
      console.error("Error:", error);
      setChatHistory([...chatHistory, { sender: 'Bot', text: "Failed to delete data." }]);
    }
  };

  const fetchEmotionalTrends = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/emotional-trends/${userId}`);

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setChatHistory([...chatHistory, { sender: 'Bot', text: `Emotional Trend: ${data.trend}` }]);
    } catch (error) {
      console.error("Error:", error);
      setChatHistory([...chatHistory, { sender: 'Bot', text: "Failed to fetch emotional trends." }]);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Mental Health Chatbot</h1>

      {!consent ? (
        <div>
          <p>Do you consent to share anonymized data for mental health analysis?</p>
          <button onClick={() => setConsent(true)}>Yes, I Agree</button>
        </div>
      ) : (
        <div>
          <div style={{ border: '1px solid black', padding: 10, height: 300, overflowY: 'scroll' }}>
            {chatHistory.map((msg, index) => (
              <div key={index}>
                <strong>{msg.sender}:</strong> {msg.text}
              </div>
            ))}
          </div>

          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message..."
          />
          <button onClick={sendMessage}>Send</button>

          <div style={{ marginTop: 10 }}>
            <button onClick={fetchEmotionalTrends}>View Emotional Trends</button>
            <button onClick={deleteData} style={{ marginLeft: 10, color: 'red' }}>Delete My Data</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
