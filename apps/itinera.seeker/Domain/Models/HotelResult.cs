using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Domain.Models
{
    ///<summary>
    /// Represents the structure of the final result Itinera Seekers provides.
    ///</summary>
    public class HotelResult
    {
        public string Name { get; set; }
        public string Url { get; set; }
        public string Rating { get; set; }
        public string Description { get; set; }
        public string ExtraDataStr { get; set; }        
        public string PricingStr { get; set; }
    }
}