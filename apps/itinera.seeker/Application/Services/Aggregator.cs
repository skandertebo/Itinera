using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Domain.Interfaces;
using Domain.Models;

namespace Application.Services
{
    public class Aggregator : IAggregator
    {
        public List<HotelResult> Aggregate(List<List<HotelResult>> results)
        {
            // TODO: remove duplicates and sort based on rating
            return results.SelectMany(r => r).ToList();
        }
    }
}