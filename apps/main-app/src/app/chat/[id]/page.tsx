import Chat from "@/app/_components/Chat";

export default function ChatPage({ params }: { params: { id: string } }) {
  return <Chat conversationId={params.id} />;
}