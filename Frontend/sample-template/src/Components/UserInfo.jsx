import React from 'react';

function UserInfo({ user }) {
  if (!user) return null;

  return (
    <div className="flex items-center justify-between p-4 border-b bg-gray-50">
      <div>
        <h2 className="text-lg font-semibold">{user.username}</h2>
        <p className="text-sm text-gray-500">{user.email}</p>
      </div>
      <div className="text-xs text-gray-400">
        {user.is_staff ? 'Admin' : 'User'}
      </div>
    </div>
  );
}

export default UserInfo;