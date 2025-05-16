using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json.Serialization;
using System.Threading.Tasks;
using Domain.Models.Queries;

namespace Infrastructure.Data.Booking.com
{
    public static class Utilities
    {
        public record ScrapeRequestPayload(
        [property: JsonPropertyName("search_string")] string SearchString,
        [property: JsonPropertyName("checkin_date")] string CheckinDate,
        [property: JsonPropertyName("checkout_date")] string CheckoutDate,
        [property: JsonPropertyName("min_budget")] int MinBudget,
        [property: JsonPropertyName("max_budget")] int MaxBudget,
        [property: JsonPropertyName("number_of_adults")] int NumberOfAdults,
        [property: JsonPropertyName("number_of_children")] int NumberOfChildren,
        [property: JsonPropertyName("number_of_rooms")] int NumberOfRooms,
        [property: JsonPropertyName("language")] string Language,
        [property: JsonPropertyName("currency")] string Currency,
        [property: JsonPropertyName("user_country")] string UserCountry
    );

        // extension to map BookingQuery → ScrapeRequestPayload
        public static ScrapeRequestPayload GetRequestPayloadFromQuery(this BookingQuery query) =>
            new(
                query.SearchString,
                query.CheckinDate,
                query.CheckoutDate,
                query.MinBudget,
                query.MaxBudget,
                query.NumberOfAdults,
                query.NumberOfChildren,
                query.NumberOfRooms,
                query.Language,
                query.Currency,
                query.UserCountry
            );
    }
}