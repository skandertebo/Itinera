import { auth } from "@/server/auth";
import { Suspense } from "react";
import { HotelFilters } from "./_components/HotelFilters";
import { HotelList } from "./_components/HotelList";

export default async function HotelsPage() {
  const session = await auth();

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900">Discover Your Perfect Stay</h1>
          <p className="mt-2 text-lg text-gray-600">
            Browse through our curated collection of hotels and find your ideal accommodation
          </p>
        </div>

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-4">
          {/* Filters Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-8 rounded-lg bg-white p-6 shadow-sm">
              <HotelFilters />
            </div>
          </div>

          {/* Hotels List */}
          <div className="lg:col-span-3">
            <Suspense fallback={<div>Loading hotels...</div>}>
              <HotelList />
            </Suspense>
          </div>
        </div>
      </div>
    </main>
  );
} 