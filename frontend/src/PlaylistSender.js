import React, { useState } from 'react';
import './PlaylistSender.css';  // Ensure you have this CSS file for styles

function PlaylistSender() {
    const [url, setUrl] = useState('');
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const result = await fetch('http://localhost:8010/api/playlists/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url })
            });
            const data = await result.json();
            if (result.ok) {
                setResponse(data.message);  // Assuming the server sends back a message
                setError(null);
            } else {
                throw new Error(data.message);  // Handling expected errors from the server
            }
        } catch (error) {
            setError(error.message);
            setResponse(null);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit} className="playlist-form">
                <input
                    type="text"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="Enter YouTube playlist URL"
                    className="playlist-input"
                />
                <button type="submit" className="submit-button">Submit</button>
            </form>
            {response && <div className="response success">{response}</div>}
            {error && <div className="response error">{error}</div>}
        </div>
    );
}

export default PlaylistSender;