import { api } from "@/trpc/server";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";

export default async function HotelPage({ params }: { params: { id: string } }) {
  const hotel = await api.hotels.getHotelById(params.id);

  if (!hotel) {
    notFound();
  }

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
            {hotel.hotel_rating && (
              <div className="rounded-full bg-yellow-100 px-4 py-2">
                <span className="text-lg font-semibold text-yellow-800">{hotel.hotel_rating}</span>
              </div>
            )}
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