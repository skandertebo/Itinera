"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useCallback, useState } from "react";

type Filters = {
  country: string;
  city: string;
  rating: string;
  facilities: string;
};

export function HotelFilters() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [filters, setFilters] = useState<Filters>({
    country: searchParams.get("country") ?? "",
    city: searchParams.get("city") ?? "",
    rating: searchParams.get("rating") ?? "",
    facilities: searchParams.get("facilities") ?? "",
  });

  const updateFilters = useCallback(
    (key: keyof Filters, value: string) => {
      const newFilters = { ...filters, [key]: value };
      setFilters(newFilters);

      const params = new URLSearchParams(searchParams.toString());
      if (value) {
        params.set(key, value);
      } else {
        params.delete(key);
      }
      router.push(`/hotels?${params.toString()}`);
    },
    [filters, router, searchParams],
  );

  return (
    <div className="space-y-4 rounded-lg bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-gray-900">Filters</h2>
      <div className="space-y-4">
        {/* Country Filter */}
        <div>
          <label htmlFor="country" className="block text-sm font-medium text-gray-700">
            Country
          </label>
          <input
            type="text"
            id="country"
            value={filters.country}
            onChange={(e) => updateFilters("country", e.target.value)}
            placeholder="Enter country"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        {/* City Filter */}
        <div>
          <label htmlFor="city" className="block text-sm font-medium text-gray-700">
            City
          </label>
          <input
            type="text"
            id="city"
            value={filters.city}
            onChange={(e) => updateFilters("city", e.target.value)}
            placeholder="Enter city"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        {/* Rating Filter */}
        <div>
          <label htmlFor="rating" className="block text-sm font-medium text-gray-700">
            Rating
          </label>
          <select
            id="rating"
            value={filters.rating}
            onChange={(e) => updateFilters("rating", e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
            <option value="">All Ratings</option>
            <option value="ThreeStar">3 Stars</option>
            <option value="FourStar">4 Stars</option>
            <option value="FiveStar">5 Stars</option>
          </select>
        </div>

        {/* Facilities Filter */}
        <div>
          <label htmlFor="facilities" className="block text-sm font-medium text-gray-700">
            Facilities
          </label>
          <input
            type="text"
            id="facilities"
            value={filters.facilities}
            onChange={(e) => updateFilters("facilities", e.target.value)}
            placeholder="Enter facilities (comma-separated)"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>
      </div>
    </div>
  );
} 