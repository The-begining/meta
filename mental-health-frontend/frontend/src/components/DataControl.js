import axios from 'axios';

function DataControl({ userId }) {
    const handleDelete = async () => {
        await axios.delete(`http://localhost:8000/delete-data/${userId}`);
        alert("Your data has been deleted successfully.");
    };

    return (
        <div>
            <p>Notice: You control your data. You can request deletion at any time.</p>
            <button onClick={handleDelete}>🗑️ Delete My Data</button>
        </div>
    );
}

export default DataControl;
