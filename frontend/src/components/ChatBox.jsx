import React from 'react'
import { useState, useRef, useEffect } from "react";
import ChatMessage from "./ChatMessage";
import QuickQuestionButtons from "./QuickQuestionButtons";
import LoadingSpinner from "./LoadingSpinner";
import InputBox from "./InputBox";
import getRealAnswer from "../utils/getRealAnswer";

const ChatBox = () => {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleClick = async (question) => {
    if (loading) return;
    setMessages((prev) => [...prev, { text: question, isUser: true }]);
    setLoading(true);
    const answer = await getRealAnswer(question);
    setMessages((prev) => [...prev, { text: answer, isUser: false }]);
    setLoading(false);
  };

  const sendMessage = async () => {
    if (loading || !userInput.trim()) return;
    setMessages((prev) => [...prev, { text: userInput, isUser: true }]);
    setUserInput("");
    setLoading(true);
    const answer = await getRealAnswer(userInput);
    setMessages((prev) => [...prev, { text: answer, isUser: false }]);
    setLoading(false);
  };

  return (
    <div className="w-full max-w-3xl flex-1 flex flex-col">
      {messages.length === 0 ? (
        <QuickQuestionButtons loading={loading} onClick={handleClick} />
      ) : (
        <div className="flex-1 overflow-y-auto max-h-[calc(100vh-280px)] scrollbar space-y-4">
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))}
          <div ref={messagesEndRef} />
        </div>
      )}

      {loading && <LoadingSpinner />}

      <InputBox
        userInput={userInput}
        setUserInput={setUserInput}
        sendMessage={sendMessage}
        loading={loading}
      />
    </div>
  );
}

export default ChatBox;
