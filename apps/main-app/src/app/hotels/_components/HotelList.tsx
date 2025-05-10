"use client";

import { api } from "@/trpc/react";
import Image from "next/image";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useState } from "react";

type Hotel = {
  id: string;
  hotel_name: string;
  hotel_rating: string | null;
  city_name: string;
  country_name: string;
  description: string | null;
  hotel_facilities: string | null;
  hotel_website_url: string | null;
};

type HotelsResponse = {
  hotels: Hotel[];
  total: number;
  totalPages: number;
  currentPage: number;
};

export function HotelList() {
  const searchParams = useSearchParams();
  const [currentPage, setCurrentPage] = useState(1);
  const hotelsPerPage = 6;

  const { data, isLoading } = api.hotels.getHotels.useQuery<HotelsResponse>({
    country: searchParams.get("country") ?? undefined,
    city: searchParams.get("city") ?? undefined,
    rating: searchParams.get("rating") ?? undefined,
    facilities: searchParams.get("facilities") ?? undefined,
    page: currentPage,
    limit: hotelsPerPage,
  });

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-600 border-t-transparent"></div>
      </div>
    );
  }

  if (!data?.hotels?.length) {
    return (
      <div className="flex h-96 flex-col items-center justify-center text-center">
        <h3 className="text-lg font-semibold text-gray-900">No hotels found</h3>
        <p className="mt-2 text-sm text-gray-600">
          Try adjusting your filters to find more hotels.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Hotels Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {data.hotels.map((hotel: Hotel) => (
          <Link
            key={hotel.id}
            href={`/hotels/${hotel.id}`}
            className="group overflow-hidden rounded-lg bg-white shadow-sm transition-all hover:shadow-md"
          >
            <div className="relative h-48 w-full">
              <Image
                src="https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80"
                alt={hotel.hotel_name}
                fill
                className="object-cover transition-transform duration-300 group-hover:scale-105"
              />
            </div>
            <div className="p-4">
              <div className="mb-2 flex items-center justify-between">
                <h3 className="text-lg font-semibold text-gray-900 group-hover:text-indigo-600">
                  {hotel.hotel_name}
                </h3>
                {hotel.hotel_rating && (
                  <span className="rounded-full bg-yellow-100 px-2.5 py-0.5 text-sm font-medium text-yellow-800">
                    {hotel.hotel_rating}
                  </span>
                )}
              </div>
              <p className="mb-2 text-sm text-gray-600">
                {hotel.city_name}, {hotel.country_name}
              </p>
              {hotel.description && (
                <p
                  className="mb-4 line-clamp-2 text-sm text-gray-500"
                  dangerouslySetInnerHTML={{ __html: hotel.description }}
                />
              )}
              <div className="flex items-center justify-between">
                {hotel.hotel_facilities && (
                  <div className="flex flex-wrap gap-1">
                    {hotel.hotel_facilities.split(",").slice(0, 3).map((facility: string, index: number) => (
                      <span
                        key={index}
                        className="rounded-full bg-gray-100 px-2 py-1 text-xs text-gray-600"
                      >
                        {facility.trim()}
                      </span>
                    ))}
                  </div>
                )}
                <span className="text-sm font-medium text-indigo-600 group-hover:text-indigo-500">
                  View Details →
                </span>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {/* Pagination */}
      {data.totalPages > 1 && (
        <div className="flex items-center justify-center space-x-2">
          <button
            onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
            className="rounded-md bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
          >
            Previous
          </button>
          <span className="text-sm text-gray-700">
            Page {currentPage} of {data.totalPages}
          </span>
          <button
            onClick={() => setCurrentPage((prev) => Math.min(prev + 1, data.totalPages))}
            disabled={currentPage === data.totalPages}
            className="rounded-md bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
} 