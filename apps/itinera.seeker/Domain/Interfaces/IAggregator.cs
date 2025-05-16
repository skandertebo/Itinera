using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Domain.Models;

namespace Domain.Interfaces
{

    ///<summary>
    /// Aggregates the different results provided by the data sources.
    ///</summary>
    public interface IAggregator
    {
        List<HotelResult> Aggregate(List<List<HotelResult>> results);

    }
}