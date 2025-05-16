using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Domain.Interfaces;
using Domain.Models;

namespace Application.Services
{
    public class ItineraSeekerService
    {
        private readonly List<IDataSource> _dataSources;
        private readonly IAggregator _aggregator;

        public ItineraSeekerService(List<IDataSource> dataSources, IAggregator aggregator)
        {
            _dataSources = dataSources;
            _aggregator = aggregator;
        }

        public async Task<List<HotelResult>> ExecuteQueryAsync(FilteringModel filteringModel)
        {
            // Execute all data sources in parallel
            var queryTasks = _dataSources.Select(ds => ds.QueryAsync(filteringModel)).ToList();
            var results = await Task.WhenAll(queryTasks);

            // Aggregate results
            return _aggregator.Aggregate(results.ToList());
        }
    }
}