using Application;
using Microsoft.AspNetCore.Mvc;

namespace Net8_Controllers.Controllers;

[ApiController]
[Route("/")]
public class EndpointsController : ControllerBase
{
    [HttpGet]
    [Route("endpoint_fast")]
    public int Fast() => ++LocalStorage.Amount;

    [HttpGet]
    [Route("endpoint_slow")]
    public async Task<OkObjectResult> Slow(MySqlStorage storage)
    {
        ++LocalStorage.Amount;
        var result = await storage.GetData();
        await storage.UpdateData(LocalStorage.Amount);
        return Ok(new { amount = LocalStorage.Amount, result });
    }
}