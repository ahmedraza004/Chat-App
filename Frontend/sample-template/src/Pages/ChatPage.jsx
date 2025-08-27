import React, { useState, useEffect, useRef } from 'react';
import ChatRoomList from '../Components/ChatRoomList';
import MessageList from '../Components/MessageList';
import MessageInput from '../Components/MessageInput';
import api from '../services/api';

function ChatPage() {
  const [chatRooms, setChatRooms] = useState([]);
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [messages, setMessages] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const socketRef = useRef(null);

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (!token) return;

    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;

    const fetchInitialData = async () => {
      try {
        const userRes = await api.get('user/info/');
        setCurrentUser(userRes.data);

        const roomsRes = await api.get('chat/');
        setChatRooms(roomsRes.data);
      } catch (err) {
        console.error('Error loading initial data:', err);
      }
    };

    fetchInitialData();
  }, []);

  useEffect(() => {
    if (!selectedRoom) return;

    const fetchMessages = async () => {
      try {
        const res = await api.get(`chat/${selectedRoom.id}/messages/`);
        setMessages(res.data);
      } catch (err) {
        console.error('Error loading messages:', err);
      }
    };

    fetchMessages();

    // WebSocket setup
    socketRef.current = new WebSocket(`ws://localhost:8000/ws/chat/${selectedRoom.id}/`);

    socketRef.current.onmessage = (e) => {
      const data = JSON.parse(e.data);
      setMessages((prev) => [...prev, data]);
    };

    socketRef.current.onerror = (e) => console.error('WebSocket error:', e);

    return () => {
      socketRef.current?.close();
    };
  }, [selectedRoom]);

  const handleSendMessage = async (text) => {
    if (!selectedRoom || !text.trim()) return;

    try {
      await api.post(`chat/${selectedRoom.id}/messages/`, { content: text });
    } catch (err) {
      console.error('Failed to send message:', err);
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <div className="w-2/5 border-r border-gray-300 p-4 overflow-y-auto bg-white">
        <h2 className="text-xl font-semibold mb-4 text-gray-800">Chat Rooms</h2>
        <ChatRoomList
          rooms={chatRooms}
          selectedRoom={selectedRoom}
          onSelect={setSelectedRoom}
          currentUser={currentUser}
        />
      </div>
      <div className="w-3/5 flex flex-col">
        <div className="flex-1 p-4 overflow-y-auto bg-white">
          <MessageList messages={messages} currentUser={currentUser} room={selectedRoom} />
        </div>
        <div className="p-4 border-t border-gray-300 bg-gray-50">
          <MessageInput onSendMessage={handleSendMessage} room={selectedRoom} />
        </div>
      </div>
    </div>
  );
}

export default ChatPage;
