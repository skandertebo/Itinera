"use client";

import { useState } from "react";

export default function ChatPage() {
  const [messages, setMessages] = useState<Array<{ role: "user" | "assistant"; content: string }>>([
    {
      role: "assistant",
      content: "Hello! I'm your AI travel assistant. Tell me about your ideal hotel stay, and I'll help you find the perfect match.",
    },
  ]);
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    setMessages((prev) => [...prev, { role: "user", content: input }]);
    setInput("");

    // TODO: Implement actual AI chat functionality
    // For now, just add a placeholder response
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "I understand you're looking for a hotel. Could you tell me more about your preferences, such as location, budget, and any specific amenities you're interested in?",
        },
      ]);
    }, 1000);
  };

  return (
    <main className="flex min-h-screen flex-col bg-gray-50">
      <div className="mx-auto w-full max-w-4xl flex-1 p-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Chat with AI Assistant</h1>
          <p className="mt-2 text-gray-600">
            Describe your ideal hotel stay, and I&apos;ll help you find the perfect match.
          </p>
        </div>

        {/* Chat Messages */}
        <div className="mb-4 flex-1 space-y-4 overflow-y-auto rounded-lg bg-white p-4 shadow-sm">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.role === "user"
                    ? "bg-indigo-600 text-white"
                    : "bg-gray-100 text-gray-900"
                }`}
              >
                <p className="text-sm">{message.content}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Chat Input */}
        <form onSubmit={handleSubmit} className="mt-4">
          <div className="flex gap-4">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Tell me about your ideal hotel stay..."
              className="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />
            <button
              type="submit"
              className="rounded-lg bg-indigo-600 px-6 py-2 text-white hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </main>
  );
} 