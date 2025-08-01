export default function ChatMessage({ message }) {
    return (
      <div className={`flex ${message.isUser ? "justify-end" : "justify-start"}`}>
        <div
          className={`max-w-[80%] rounded-xl p-4 ${
            message.isUser
              ? "bg-blue-600 text-white rounded-br-none"
              : "bg-gray-800 text-gray-100 rounded-bl-none"
          }`}
        >
          <p className="whitespace-pre-line">{message.text}</p>
        </div>
      </div>
    );
  }
  