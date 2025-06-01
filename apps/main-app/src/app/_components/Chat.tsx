"use client";

import { api } from "@/trpc/react";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import Markdown from "react-markdown";

interface Message {
  id: string;
  content: string;
  sender: "user" | "assistant";
  createdAt: Date;
}

interface Props {
  conversationId?: string;
}

export default function ChatPage({ conversationId }: Props) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const conversationIdRef = useRef<string>(conversationId);
  const router = useRouter();
  const { data: conversation, isLoading: isLoadingConversation } = api.chat.getConversation.useQuery(conversationId ?? "", {
    enabled: !!conversationId,
  });
 
  useEffect(() => {
    if (conversation) {
      setMessages(conversation.messages.map(msg => ({
        ...msg,
        sender: msg.sender as "user" | "assistant"
      })));
    }
  }, [conversation]);

  const sendMessage = api.chat.sendMessage.useMutation({
    onSuccess: (data) => {
      // Add both messages from the response, ensuring they match our Message type
      const newMessages = data.messages.map(msg => ({
        ...msg,
        sender: msg.sender as "user" | "assistant"
      }));
      setMessages((prev) => [...prev, ...newMessages]);
      
      // If this is a new conversation, update the URL
      if (!conversationId && data.conversationId) {
        conversationIdRef.current = data.conversationId;
        router.push(`/chat/${data.conversationId}`);
      }
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    try {
      await sendMessage.mutateAsync({
        conversationId: conversationIdRef.current ?? null,
        message: input,
      });
      setInput("");
    } catch (error) {
      console.error("Failed to send message:", error);
      // You might want to show an error message to the user here
    }
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
        <div className="mb-4 min-h-[400px] flex-1 space-y-4 overflow-y-auto rounded-lg bg-white p-4 shadow-sm">
          {isLoadingConversation ? (
            <div className="w-full h-full flex justify-center items-center">
             <AiOutlineLoading3Quarters className="w-8 h-8 animate-spin" />
            </div>
          ) : (
            <>
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.sender === "user"
                    ? "bg-indigo-600 text-white"
                    : "bg-gray-100 text-gray-900"
                }`}
              >
                <Markdown>{message.content}</Markdown>
                <span className="text-xs opacity-70">
                  {new Date(message.createdAt).toLocaleTimeString()}
                </span>
              </div>
              </div>
            ))}
            </>
          )}
          {sendMessage.isPending && (
            <div className="flex justify-start">
              <div className="max-w-[80%] rounded-lg bg-gray-100 px-4 py-2">
                <div className="flex space-x-2">
                  <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400"></div>
                  <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: "0.2s" }}></div>
                  <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: "0.4s" }}></div>
                </div>
              </div>
            </div>
          )}
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
              disabled={sendMessage.isPending || isLoadingConversation}
            />
            <button
              type="submit"
              className="rounded-lg bg-indigo-600 px-6 py-2 text-white hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
              disabled={sendMessage.isPending}
            >
              {sendMessage.isPending ? "Sending..." : "Send"}
            </button>
          </div>
        </form>
      </div>
    </main>
  );
} 