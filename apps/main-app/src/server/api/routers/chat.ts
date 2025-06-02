import { createTRPCRouter, protectedProcedure } from "@/server/api/trpc";
import { z } from "zod";


const predictResponseSchema = z.object({
  output: z.object({
    sender: z.string(),
    content: z.string(),
  }),
});

export const chatRouter = createTRPCRouter({
  sendMessage: protectedProcedure
    .input(
      z.object({
        conversationId: z.string().nullable(),
        message: z.string(),
      })
    )
    .mutation(async ({ ctx, input }) => {
      let conversationId = input.conversationId;

      // If no conversationId, create a new conversation
      if (!conversationId) {
        const newConversation = await ctx.db.conversation.create({
          data: {
            userId: ctx.session.user.id,
          },
        });
        conversationId = newConversation.id;
      }

      // Get message history for this conversation
      const messageHistory = await ctx.db.message.findMany({
        where: {
          conversationId,
        },
        orderBy: {
          createdAt: "asc",
        },
      });

      // Format message history for the AI endpoint
      const formattedHistory = messageHistory.map((msg) => ({
        sender: msg.sender,
        content: msg.content,
      }));

      // Add the new user message to history
      formattedHistory.push({
        sender: "user",
        content: input.message,
      });

      // Save the user message to the database
      const userMessage = await ctx.db.message.create({
        data: {
          content: input.message,
          sender: "user",
          conversationId,
        },
      });

      // Call the AI endpoint
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages_history: formattedHistory,
          input: input.message,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get AI response");
      }

      const aiResponse = predictResponseSchema.parse(await response.json());

      // Save the AI response to the database
      const aiMessage = await ctx.db.message.create({
        data: {
          content: aiResponse.output.content,
          sender: "assistant",
          conversationId,
        },
      });

      return {
        conversationId,
        messages: [userMessage, aiMessage],
      };
    }),

  getConversation: protectedProcedure
    .input(z.string())
    .query(async ({ ctx, input }) => {
      const conversation = await ctx.db.conversation.findUnique({
        where: {
          id: input,
          userId: ctx.session.user.id,
        },
        include: {
          messages: {
            orderBy: {
              createdAt: "asc",
            },
          },
        },
      });

      if (!conversation) {
        throw new Error("Conversation not found");
      }

      return conversation;
    }),
}); 