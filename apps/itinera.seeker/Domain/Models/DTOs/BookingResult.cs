using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Domain.Models.DTOs
{
    public class BookingResult
    {
        public string Name { get; set; }
        public string Url { get; set; }
        public string Rating { get; set; }
        public string Description { get; set; }
        public List<string>? Facilities { get; set; }
        public Dictionary<string, object> Surroundings { get; set; } = new(); // Empty in sample
        public Dictionary<string, string> Detailed_Ratings { get; set; } = new();
        public List<Pricing>? Pricing { get; set; }
    }

    public class Pricing
    {
        public string Room_Type { get; set; }
        public string Price { get; set; }
    }
}