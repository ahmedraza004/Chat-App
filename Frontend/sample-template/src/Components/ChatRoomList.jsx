import React from 'react';

function ChatRoomList({ rooms, selectedRoom, onSelect, currentUser }) {
  return (
    <div className="space-y-3">
      {rooms.map((room) => {
        const isSelected = selectedRoom?.id === room.id;
        const displayName = room.is_group
          ? room.name
          : `Chat with ${room.participants.find(p => p.username !== currentUser?.username)?.username}`;

        return (
          <div
            key={room.id}
            onClick={() => onSelect(room)}
            className={`p-3 rounded cursor-pointer ${
              isSelected ? 'bg-blue-100 border border-blue-400' : 'hover:bg-gray-100'
            }`}
          >
            <h4 className="font-semibold text-gray-800">{displayName}</h4>
            <ul className="text-sm text-gray-600">
              {room.participants.map((p) => (
                <li key={p.id}>- {p.username}</li>
              ))}
            </ul>
          </div>
        );
      })}
    </div>
  );
}

export default ChatRoomList;
