import React, { useState } from 'react';

function MessageInput({ onSendMessage, room }) {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!text.trim() || !room) return;
    onSendMessage(text);
    setText('');
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder={room ? 'Type your message...' : 'Select a room to start chatting'}
        className="flex-1 px-4 py-2 border rounded focus:outline-none focus:ring"
        disabled={!room}
      />
      <button
        type="submit"
        disabled={!room || !text.trim()}
        className={`px-4 py-2 rounded ${
          !room || !text.trim()
            ? 'bg-gray-300 text-gray-600 cursor-not-allowed'
            : 'bg-blue-500 text-white hover:bg-blue-600'
        }`}
      >
        Send
      </button>
    </form>
  );
}

export default MessageInput;
