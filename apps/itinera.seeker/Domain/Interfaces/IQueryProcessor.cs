using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Domain.Models.Queries;

namespace Domain.Interfaces
{
    ///<summary>
    /// Processes a given query by executing it and returning structured data.
    ///</summary>
    public interface IQueryProcessor<TQuery, TResult>
        where TQuery : BaseQuery
        where TResult : class
    {
        Task<TResult> ProcessQueryAsync(TQuery query);
    }
}