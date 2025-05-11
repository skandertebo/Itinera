"use client";

import { api } from "@/trpc/react";
import { useSession } from "next-auth/react";
import Image from "next/image";
import Link from "next/link";
import { notFound, useRouter } from "next/navigation";

export default function HotelPage({ params }: { params: { id: string } }) {
  const { data: session } = useSession();
  const router = useRouter();

  const { data: hotel, isLoading: isLoadingHotel } = api.hotels.getHotelById.useQuery(params.id);
  const { data: isFavorite, isLoading: isLoadingFavorite, refetch } = api.hotels.isFavorite.useQuery(
    { hotelId: params.id },
    { enabled: !!session },
  );

  const toggleFavorite = api.hotels.toggleFavorite.useMutation({
    onSuccess: () => {
      void refetch();
    },
  });

  const handleFavoriteClick = () => {
    if (!session) {
      router.push("/api/auth/signin");
      return;
    }
    toggleFavorite.mutate({ hotelId: params.id });
  };

  if (isLoadingHotel) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-32 w-32 animate-spin rounded-full border-b-2 border-t-2 border-indigo-500"></div>
      </div>
    );
  }

  if (!hotel) {
    notFound();
  }

  const isButtonLoading = isLoadingFavorite || toggleFavorite.isPending;

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Breadcrumb */}
        <nav className="mb-8">
          <ol className="flex items-center space-x-2 text-sm">
            <li>
              <Link href="/" className="text-gray-500 hover:text-gray-700">
                Home
              </Link>
            </li>
            <li className="text-gray-500">/</li>
            <li>
              <Link href="/hotels" className="text-gray-500 hover:text-gray-700">
                Hotels
              </Link>
            </li>
            <li className="text-gray-500">/</li>
            <li className="text-gray-900">{hotel.hotel_name}</li>
          </ol>
        </nav>

        {/* Hotel Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{hotel.hotel_name}</h1>
              <p className="mt-2 text-lg text-gray-600">
                {hotel.city_name}, {hotel.country_name}
              </p>
            </div>
            <div className="flex items-center gap-4">
              {hotel.hotel_rating && (
                <div className="rounded-full bg-yellow-100 px-4 py-2">
                  <span className="text-lg font-semibold text-yellow-800">{hotel.hotel_rating}</span>
                </div>
              )}
              <button
                onClick={handleFavoriteClick}
                disabled={isButtonLoading}
                className={`rounded-full p-2 transition-colors ${
                  isFavorite
                    ? "bg-red-500 text-white hover:bg-red-600"
                    : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                } ${isButtonLoading ? "opacity-50 cursor-not-allowed" : ""}`}
                title={session ? (isFavorite ? "Remove from favorites" : "Add to favorites") : "Sign in to add favorites"}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  className="h-6 w-6"
                >
                  <path d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0112 5.052 5.5 5.5 0 0116.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 01-4.244 3.17 15.247 15.247 0 01-.383.219l-.022.012-.007.004-.003.001a.752.752 0 01-.704 0l-.003-.001z" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        {/* Hotel Image */}
        <div className="mb-8 overflow-hidden rounded-lg">
          <div className="relative h-[400px] w-full">
            <Image
              src="https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80"
              alt={hotel.hotel_name}
              fill
              className="object-cover"
              priority
            />
          </div>
        </div>

        {/* Hotel Details Grid */}
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {/* Description */}
            {hotel.description && (
              <div className="mb-8">
                <h2 className="mb-4 text-xl font-semibold text-gray-900">About</h2>
                <div
                  className="prose prose-indigo max-w-none text-gray-600"
                  dangerouslySetInnerHTML={{ __html: hotel.description }}
                />
              </div>
            )}

            {/* Facilities */}
            {hotel.hotel_facilities && (
              <div className="mb-8">
                <h2 className="mb-4 text-xl font-semibold text-gray-900">Facilities</h2>
                <div className="flex flex-wrap gap-2">
                  {hotel.hotel_facilities.split(",").map((facility, index) => (
                    <span
                      key={index}
                      className="rounded-full bg-gray-100 px-3 py-1 text-sm text-gray-700"
                    >
                      {facility.trim()}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="rounded-lg bg-white p-6 shadow-sm">
              {/* Contact Information */}
              <div className="mb-6">
                <h2 className="mb-4 text-xl font-semibold text-gray-900">Contact Information</h2>
                <div className="space-y-3">
                  {hotel.address && (
                    <div>
                      <h3 className="text-sm font-medium text-gray-700">Address</h3>
                      <p className="text-sm text-gray-600">{hotel.address}</p>
                    </div>
                  )}
                  {hotel.phone_number && (
                    <div>
                      <h3 className="text-sm font-medium text-gray-700">Phone</h3>
                      <p className="text-sm text-gray-600">{hotel.phone_number}</p>
                    </div>
                  )}
                  {hotel.fax_number && (
                    <div>
                      <h3 className="text-sm font-medium text-gray-700">Fax</h3>
                      <p className="text-sm text-gray-600">{hotel.fax_number}</p>
                    </div>
                  )}
                  {hotel.pin_code && (
                    <div>
                      <h3 className="text-sm font-medium text-gray-700">PIN Code</h3>
                      <p className="text-sm text-gray-600">{hotel.pin_code}</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Location */}
              {hotel.map_position && (
                <div className="mb-6">
                  <h2 className="mb-4 text-xl font-semibold text-gray-900">Location</h2>
                  <div className="aspect-video w-full overflow-hidden rounded-lg">
                    <iframe
                      src={`https://www.google.com/maps/embed?pb=${hotel.map_position}`}
                      width="100%"
                      height="100%"
                      style={{ border: 0 }}
                      allowFullScreen
                      loading="lazy"
                      referrerPolicy="no-referrer-when-downgrade"
                    ></iframe>
                  </div>
                </div>
              )}

              {/* Website */}
              {hotel.hotel_website_url && (
                <div>
                  <Link
                    href={hotel.hotel_website_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex w-full items-center justify-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                  >
                    Visit Website
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
} 