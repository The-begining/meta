import React from "react";

const HeatMap = ({ emotionMap }) => {
    return (
        <div>
            <h2>Emotion Map 🌍</h2>
            <div style={{ border: "1px solid black", padding: "10px", height: "300px", overflowY: "scroll" }}>
                {emotionMap.length > 0 ? (
                    emotionMap.map((entry, index) => (
                        <div key={index}>
                            <strong>Location:</strong> ({entry.latitude.toFixed(4)}, {entry.longitude.toFixed(4)}) —
                            <strong> Emotion:</strong> {entry.emotion}
                        </div>
                    ))
                ) : (
                    <p>No emotion data available.</p>
                )}
            </div>
        </div>
    );
};

export default HeatMap;