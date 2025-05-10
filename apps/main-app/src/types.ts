import type { api } from "@/trpc/server";

type Hotel = Awaited<ReturnType<typeof api.hotels.getHotels>>['hotels'][number];

export type { Hotel };
