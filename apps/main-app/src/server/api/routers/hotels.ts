import { createTRPCRouter, publicProcedure } from "@/server/api/trpc";
import { z } from "zod";

const hotelFiltersSchema = z.object({
  country: z.string().optional(),
  city: z.string().optional(),
  rating: z.string().optional(),
  facilities: z.string().optional(),
  page: z.number().min(1).default(1),
  limit: z.number().min(1).max(50).default(6),
});

export const hotelsRouter = createTRPCRouter({
  getHotels: publicProcedure
    .input(hotelFiltersSchema)
    .query(async ({ ctx, input }) => {
      const { country, city, rating, facilities, page, limit } = input;
      const skip = (page - 1) * limit;

      // Build the where clause based on filters
      const where = {
        ...(country && { country_name: { contains: country, mode: "insensitive" as const } }),
        ...(city && { city_name: { contains: city, mode: "insensitive" as const } }),
        ...(rating && { hotel_rating: { contains: rating } }),
        ...(facilities && { hotel_facilities: { contains: facilities, mode: "insensitive" as const } }),
      };

      // Get total count for pagination
      const total = await ctx.db.hotels.count({ where });

      // Get hotels with pagination and filters
      const hotels = await ctx.db.hotels.findMany({
        where,
        skip,
        take: limit,
        orderBy: { hotel_name: "asc" },
      });

      return {
        hotels,
        total,
        totalPages: Math.ceil(total / limit),
        currentPage: page,
      };
    }),

  getHotelById: publicProcedure
    .input(z.string())
    .query(async ({ ctx, input }) => {
      return ctx.db.hotels.findUnique({
        where: { id: input },
      });
    }),
}); 