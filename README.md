<img width="1366" height="768" alt="Screenshot (9)" src="https://github.com/user-attachments/assets/f9b1da32-f1a7-406b-9344-eeb20878bbf0" />
# Real-Time Chat Application

A real-time chat application built with **Django**, **Django Channels**, **WebSockets**, and **React**. This app supports user authentication, private messaging, and real-time updates.

## 🚀 Features
- Real-time messaging using WebSockets
- User authentication (login/register)
- Private and group chats
- Responsive UI with React

## 🛠 Tech Stack
- **Backend:** Django, Django Channels, DRF
- **Frontend:** React, Axios
- **Database:** PostgreSQL
- **Deployment:** Railway (Backend), Vercel (Frontend)

## 🔗 Live Demo
Live App | API Docs

## 📂 Installation
```bash
# Clone the repository
git clone https://github.com/ahmedraza004/chat-app.git
cd chat-app

# Backend setup
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend setup
cd frontend
npm install
npm start
