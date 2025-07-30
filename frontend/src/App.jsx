import { useState, useRef, useEffect } from "react";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleClick = (question) => {
    setMessages(prev => [...prev, { text: question, isUser: true }]);
    setTimeout(() => {
      setMessages(prev => [...prev, { text: getMockAnswer(question), isUser: false }]);
    }, 500);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage();
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const sendMessage = () => {
    if (!userInput.trim()) return;
    
    setMessages(prev => [...prev, { text: userInput, isUser: true }]);
    setUserInput("");
    
    setTimeout(() => {
      setMessages(prev => [...prev, { text: getMockAnswer(userInput), isUser: false }]);
    }, 500);
  };

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col">
      {/* Fixed Navbar */}
      <nav className="bg-blue-600 shadow-sm py-4 px-6 flex items-center fixed top-0 left-0 right-0 z-10">
        <div className="flex items-center">
          <img 
            src="./uwi_logo.png" 
            alt="UWI Logo" 
            className="h-12 w-80 mr-3"
          />
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 container mx-auto px-4 pt-24 pb-28 flex flex-col items-center">
        {/* Chat Area - Scrollable */}
        <div className="w-full max-w-3xl flex-1 flex flex-col">
          {/* Welcome Message (centered when no messages) */}
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full">
              <div className="text-center max-w-2xl">
                <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">
                  What can I help you with?
                </h1>
                <p className="text-gray-300 text-lg mb-8">
                  Ask me anything about UWI admissions, registration, or student services.
                </p>

                {/* Suggested Questions */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <button
                    className="bg-gray-800 border border-gray-700 rounded-xl p-4 shadow-sm hover:bg-gray-700 hover:border-blue-500 transition-all duration-200 text-left"
                    onClick={() => handleClick("How do I apply to UWI?")}
                  >
                    <h3 className="font-medium text-white mb-1">Application</h3>
                    <p className="text-gray-300">
                      How do I apply to <span className="font-semibold text-blue-400">UWI</span>?
                    </p>
                  </button>
                  <button
                    className="bg-gray-800 border border-gray-700 rounded-xl p-4 shadow-sm hover:bg-gray-700 hover:border-blue-500 transition-all duration-200 text-left"
                    onClick={() => handleClick("How do I register for GATE?")}
                  >
                    <h3 className="font-medium text-white mb-1">GATE Funding</h3>
                    <p className="text-gray-300">
                      How do I register for <span className="font-semibold text-blue-400">GATE</span>?
                    </p>
                  </button>
                  <button
                    className="bg-gray-800 border border-gray-700 rounded-xl p-4 shadow-sm hover:bg-gray-700 hover:border-blue-500 transition-all duration-200 text-left"
                    onClick={() => handleClick("What to do if I have an AR Hold?")}
                  >
                    <h3 className="font-medium text-white mb-1">AR Hold</h3>
                    <p className="text-gray-300">What to do if I have an AR Hold?</p>
                  </button>
                </div>
              </div>
            </div>
          ) : (
            /* Scrollable Chat Messages when conversation exists */
            <div className="flex-1 overflow-y-auto max-h-[calc(100vh-280px)] scrollbar">
              <div className="space-y-4">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-xl p-4 ${message.isUser
                        ? 'bg-blue-600 text-white rounded-br-none'
                        : 'bg-gray-800 text-gray-100 rounded-bl-none'
                      }`}
                    >
                      <p className="whitespace-pre-line">{message.text}</p>
                    </div>
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>
            </div>
          )}
        </div>

        {/* Fixed Input Box at bottom */}
        <form
          onSubmit={handleSubmit}
          className="w-full max-w-3xl bg-gray-800 border border-gray-700 rounded-xl shadow-sm p-2 fixed bottom-6"
        >
          <div className="flex items-center">
            <textarea
              ref={textareaRef}
              rows={1}
              className="flex-1 px-4 py-3 text-white bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none placeholder-gray-400"
              placeholder="Ask me anything about UWI..."
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            <button
              type="submit"
              className="ml-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-3 transition-colors duration-200"
            >
              Send
            </button>
          </div>
        </form>
      </main>
      <style jsx global>{`
        .scrollbar::-webkit-scrollbar {
          width: 8px;
        }
        .scrollbar::-webkit-scrollbar-track {
          background: #1f2937;
          border-radius: 4px;
        }
        .scrollbar::-webkit-scrollbar-thumb {
          background: #4b5563;
          border-radius: 4px;
        }
        .scrollbar::-webkit-scrollbar-thumb:hover {
          background: #6b7280;
        }
      `}</style>
    </div>
  );
}

// TEMP: Mock response logic for demo
function getMockAnswer(question) {
  const answers = {
    "How do I apply to UWI?":
      "To apply to UWI, visit the official admissions portal, complete the application form, and submit required documents like transcripts and identification. Deadlines and requirements vary by program.",
    "How do I register for GATE?":
      "To register for GATE, you need to follow a few steps. First, make sure you are an eligible undergraduate student under 50 years old and a national of Trinidad & Tobago. Then, visit the GATE Registration Centre (GRC) to register for GATE e-Service. Provide your birth certificate, ID (National ID or passport), and a valid email. You will receive a GATE e-Service ID and password via email. Apply online with scanned documents like your acceptance letter and birth certificate. Select the correct academic period and semester on the e-GATE application form. Finally, print, sign, and submit the Student Copy of the form. If you have any specific questions about registration, it would be best to contact Student Administration for assistance.",
    "What to do if I have an AR Hold?":
      "If you have an AR Hold, it usually means there's an outstanding balance on your account. Contact the Bursary or Student Administration to resolve it before continuing with registration or exams.",
  };

  return answers[question] || "I'll find the answer for you. Please check back soon...";
}