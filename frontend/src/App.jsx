import React from 'react'

import ChatBox from './components/ChatBox.jsx';


export default function App() {
  return (
    <div className="min-h-screen bg-gray-900 flex flex-col">
      <nav className="bg-blue-600 shadow-sm py-4 px-6 flex items-center fixed top-0 left-0 right-0 z-10">
        <img src="./uwi_logo.png" alt="UWI Logo" className="h-12 w-80 mr-3" />
      </nav>
      <main className="flex-1 container mx-auto px-4 pt-24 pb-28 flex flex-col items-center">
        <ChatBox />
      </main>
    </div>
  );
}
