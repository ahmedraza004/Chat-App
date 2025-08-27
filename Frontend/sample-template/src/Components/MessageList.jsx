import React from 'react';

function MessageList({ messages, currentUser, room }) {
  if (!room) return (
    <div className="text-center text-gray-500 mt-10">
      Select a chat room to view messages.
    </div>
  );

  return (
    <div className="space-y-4">
      {messages.length === 0 ? (
        <div className="text-center text-gray-400">No messages yet.</div>
      ) : (
        messages.map((msg) => (
          <div
            key={msg.id}
            className={`p-3 rounded-lg max-w-md ${
              msg.sender.id === currentUser?.id
                ? 'bg-blue-100 ml-auto text-right'
                : 'bg-gray-200 mr-auto text-left'
            }`}
          >
            <div className="text-sm text-gray-700">{msg.content}</div>
            <div className="text-xs text-gray-500 mt-1">
              {msg.sender.username}
            </div>
          </div>
        ))
      )}
    </div>
  );
}

export default MessageList;
