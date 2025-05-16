using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Domain.Models
{
    ///<summary>
    /// Represents the high level model external apps use to communicate with Itinera Seeker
    ///</summary>
    public class FilteringModel
    {
        public Destination Destination { get; set; }
        public DateTime CheckIn { get; set; }
        public DateTime CheckOut { get; set; }
        public Travelers Travelers { get; set; }
        public Accommodation Accommodation { get; set; }
        public Budget Budget { get; set; }
        public string UserCurrency { get; set; }
        public string UserCountry { get; set; }
        public string UserLanguage { get; set; }
    }

    public record Destination
    {
        public string City { get; set; }
        public string Country { get; set; }
    }

    public record Travelers
    {
        public int Adults { get; set; }
        public int Children { get; set; }
    }

    public record Accommodation
    {
        public int Rooms { get; set; }
        public List<string> RoomTypes { get; set; }
    }

    public record Budget
    {
        public double Min { get; set; }
        public double Max { get; set; }
    }
}