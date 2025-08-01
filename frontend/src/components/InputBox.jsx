import React from 'react'

const InputBox = ({ userInput, setUserInput, sendMessage, loading }) => {
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
  
    return (
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-3xl bg-gray-800 border border-gray-700 rounded-xl shadow-sm p-2 fixed bottom-6"
      >
        <div className="flex items-center">
          <textarea
            rows={1}
            className="flex-1 px-4 py-3 text-white bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none placeholder-gray-400"
            placeholder="Ask me anything about UWI..."
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
          />
          <button
            type="submit"
            className="ml-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-3 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={loading}
          >
            Send
          </button>
        </div>
      </form>
    );
  }

export default InputBox;
  