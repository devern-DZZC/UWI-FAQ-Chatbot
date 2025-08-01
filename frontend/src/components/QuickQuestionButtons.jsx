export default function QuickQuestionButtons({ loading, onClick }) {
    const questions = [
      { label: "Application", text: "How do I register at UWI?" },
      { label: "GATE Funding", text: "How do I register for GATE?" },
      { label: "AR Hold", text: "I have an AR Hold. What shall I do?" },
    ];
  
    return (
      <div className="flex flex-col items-center justify-center h-full text-center max-w-2xl mx-auto">
        <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">
          What can I help you with?
        </h1>
        <p className="text-gray-300 text-lg mb-8">
          Ask me anything about UWI admissions, registration, or student services.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {questions.map(({ label, text }, i) => (
            <button
              key={i}
              disabled={loading}
              className={`bg-gray-800 border border-gray-700 rounded-xl p-4 shadow-sm transition-all duration-200 text-left ${
                loading
                  ? "opacity-50 cursor-not-allowed"
                  : "hover:bg-gray-700 hover:border-blue-500"
              }`}
              onClick={() => onClick(text)}
            >
              <h3 className="font-medium text-white mb-1">{label}</h3>
              <p className="text-gray-300">{text}</p>
            </button>
          ))}
        </div>
      </div>
    );
  }
  