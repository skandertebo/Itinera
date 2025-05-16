using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Application.Services;
using Domain.Interfaces;
using Domain.Models.DTOs;
using Domain.Models.Queries;
using Infrastructure.Data.Booking.com;

namespace Presentation.Helpers
{
    public static class DependencyInjection
    {
        public static IServiceCollection AddInfrastructure(this IServiceCollection services)
        {
            // Register processors and parsers
            services.AddSingleton<IQueryProcessor<BookingQuery, List<BookingResult>>, BookingQueryProcessor>();
            services.AddSingleton<IParser<List<BookingResult>>, BookingResultsParser>();

            // Register data sources
            services.AddSingleton<IDataSource>(sp => new BookingDataSource(
                sp.GetService<HttpClient>(),
                sp.GetService<IQueryFactory>()));

            return services;
        }

        public static IServiceCollection AddApplication(this IServiceCollection services)
        {
            // Register Services
            services.AddSingleton<IQueryFactory, QueryFactory>();
            services.AddSingleton<IAggregator, Aggregator>();
            services.AddSingleton(sp =>
            {
                var dataSources = sp.GetServices<IDataSource>().ToList();
                var aggregator = sp.GetService<IAggregator>();
                return new ItineraSeekerService(dataSources, aggregator);
            });

            return services;
        }
    }
}