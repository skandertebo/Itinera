using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Domain.enums;
using Domain.Interfaces;
using Domain.Models;
using Domain.Models.Queries;

namespace Infrastructure.Data.Booking.com
{
    public class BookingDataSource : IDataSource
    {
        private readonly BookingQueryProcessor _processor;
        private readonly BookingResultsParser _parser;
        private readonly IQueryFactory _queryFactory;
        public BookingDataSource(HttpClient httpClient, IQueryFactory queryFactory)
        {
            _processor = new BookingQueryProcessor(httpClient);
            _parser = new BookingResultsParser();
            _queryFactory = queryFactory;
        }

        public async Task<List<HotelResult>> QueryAsync(FilteringModel filteringModel)
        {
            BookingQuery query = (BookingQuery)_queryFactory.CreateQuery(filteringModel, QueryType.Booking);

            var bookingResults = await _processor.ProcessQueryAsync(query);
            return _parser.Parse(bookingResults);
        }
    }
}