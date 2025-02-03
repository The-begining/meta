import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Tooltip } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const HeatMap = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch("http://127.0.0.1:8000/heatmap")
            .then((res) => res.json())
            .then((data) => setData(data.heatmap));
    }, []);

    return (
        <MapContainer center={[60, 8]} zoom={5} style={{ height: "400px", width: "100%" }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {data.map((point, idx) => (
                <CircleMarker key={idx} center={[point.latitude, point.longitude]} radius={point.avg_stress}>
                    <Tooltip>Stress Level: {point.avg_stress.toFixed(1)}</Tooltip>
                </CircleMarker>
            ))}
        </MapContainer>
    );
};

export default HeatMap;
