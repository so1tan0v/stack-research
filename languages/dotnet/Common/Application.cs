using Dapper;
using MySqlConnector;

namespace Application;

public static class LocalStorage
{
    public static int Amount { get; set; } = 0;
}

public record TestData
{
    public string name { get; set; }

    public int code { get; set; }
}

public class MySqlStorage(MySqlConnection connection)
{
    private const string TargetRecordName = "amount";

    public async Task<TestData?> GetData()
    {
        var results = await connection.QueryAsync<TestData>("SELECT * FROM test WHERE name = @name LIMIT 1", new { name = TargetRecordName });
        return results.FirstOrDefault();
    }

    public async Task<bool> UpdateData(decimal code)
    {
        return await connection.ExecuteAsync("UPDATE test SET code = @code WHERE name = @name", new { code, name = TargetRecordName }) > 0;
    }
}
