import { useState } from 'react'
import {BrowserRouter,Routes,Route,Navigate} from 'react-router-dom'
import LoginPage from './Pages/LoginPage'
import Registration from './Pages/Registration'
import ChatPage from './Pages/ChatPage'
function App() {

  return (
    <>
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<Navigate to="/register" replace />} />
      <Route path="/register" element={<Registration />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/chat" element={<ChatPage />} />
    </Routes>
    </BrowserRouter>
     
    </>
  )
}

export default App

