using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Domain.enums;
using Domain.Interfaces;
using Domain.Models;
using Domain.Models.Queries;

namespace Application.Services
{
    public class QueryFactory : IQueryFactory
    {
        public BaseQuery CreateQuery(FilteringModel model, QueryType type)
        {
            switch (type)
            {
                case QueryType.Booking:
                    return new BookingQuery(model);
                default:
                    throw new ArgumentException("Invalid query type", nameof(type));
            }
        }
    }
}