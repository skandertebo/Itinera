using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Domain.enums;
using Domain.Models;
using Domain.Models.Queries;

namespace Domain.Interfaces
{
    public interface IQueryFactory
    {
        public BaseQuery CreateQuery(FilteringModel model, QueryType type);
    }
}