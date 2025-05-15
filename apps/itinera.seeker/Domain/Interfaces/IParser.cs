using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Domain.Models;

namespace Domain.Interfaces
{
    ///<summary>
    /// Parses the different types of structured data Itinera Seekers supports 
    /// into a structured common result.
    ///</summary>
    public interface IParser
    {
        List<HotelResult> Parse<T>(T rawData) where T : class;
    }
}