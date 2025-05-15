using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Domain.Models;
using Domain.Models.Queries;

namespace Domain.Interfaces
{
    public interface IDataSource
    {
        Task<List<HotelResult>> QueryAsync<T>(T query) where T : BaseQuery;
    }
}