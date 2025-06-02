using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using Domain.Interfaces;
using Domain.Models;
using Domain.Models.DTOs;

namespace Infrastructure.Data.Booking.com
{
    public class BookingResultsParser : IParser<List<BookingResult>>
    {
        public List<HotelResult> Parse(List<BookingResult> bookingResults)
        {
            return bookingResults.Select(BookingToHotelResult).ToList();
        }

        private HotelResult BookingToHotelResult(BookingResult booking)
        {
            return new HotelResult
            {
                Name = booking.Name,
                Url = booking.Url,
                Rating = booking.Rating,
                Description = booking.Description,
                ExtraDataStr = JsonSerializer.Serialize(new
                {
                    booking.Facilities,
                    booking.Surroundings,
                    booking.Detailed_Ratings
                }),
                PricingStr = JsonSerializer.Serialize(booking.Pricing),
                ReviewsStr = JsonSerializer.Serialize(booking.Reviews)
            };
        }
    }
}