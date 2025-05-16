using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Application.Services;
using Domain.Models;
using Microsoft.AspNetCore.Mvc;

namespace Presentation.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ItineraSeekerController : ControllerBase
    {
        private readonly ItineraSeekerService _seekerService;

        public ItineraSeekerController(ItineraSeekerService seekerService)
        {
            _seekerService = seekerService;
        }

        [HttpPost]
        public async Task<ActionResult<List<HotelResult>>> PostQuery([FromBody] FilteringModel model)
        {
            Console.WriteLine("sex");
            var results = await _seekerService.ExecuteQueryAsync(filteringModel: model);
            return Ok(results);
        }
    }
}