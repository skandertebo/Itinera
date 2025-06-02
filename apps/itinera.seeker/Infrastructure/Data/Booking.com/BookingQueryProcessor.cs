using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Domain.Interfaces;
using Domain.Models.DTOs;
using Domain.Models.Queries;

namespace Infrastructure.Data.Booking.com
{
    public class BookingQueryProcessor : IQueryProcessor<BookingQuery, List<BookingResult>>
    {
        private readonly HttpClient _httpClient;

        public BookingQueryProcessor(HttpClient httpClient)
        {
            httpClient.Timeout = TimeSpan.FromSeconds(3000);
            _httpClient = httpClient;
        }

        public async Task<List<BookingResult>> ProcessQueryAsync(BookingQuery query)
        {
            // Build the payload object matching the API’s expected JSON shape
            var payload = query.GetRequestPayloadFromQuery();

            // Serialize to JSON
            var json = JsonSerializer.Serialize(payload);

            // Create the HTTP content
            using var content = new StringContent(json, Encoding.UTF8, "application/json");

            // Send the POST
            // TODO: put in env vars
            var response = await _httpClient.PostAsync("http://localhost:5001/scrape", content);

            // Throw if not successful
            response.EnsureSuccessStatusCode();

            // Read and deserialize the response body
            var responseStream = await response.Content.ReadAsStreamAsync();
            
            var result = await JsonSerializer.DeserializeAsync<List<BookingResult>>(responseStream, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            if (result == null)
            {
                throw new InvalidOperationException("Failed to deserialize BookingResult from scrape service.");
            }

            return result;
        }
  }
}