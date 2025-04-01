using Application;
using MySqlConnector;
using System.Reflection;

var builder = WebApplication.CreateBuilder(args);

// Load environment variables from .env file
var envFilePath = Path.Combine(Directory.GetParent(Assembly.GetEntryAssembly()!.Location)!.FullName, "env", ".env");
DotEnv.Load(envFilePath);
builder.Configuration.AddEnvironmentVariables();

var connectionStringBuilder = new MySqlConnectionStringBuilder
{
    Server = builder.Configuration["MYSQL_HOST"],
    UserID = builder.Configuration["MYSQL_USER"],
    Password = builder.Configuration["MYSQL_PASSWORD"],
    Database = builder.Configuration["MYSQL_SCHEMA"],
};
Console.WriteLine($"Connecting to {connectionStringBuilder.ConnectionString}");

// Add services to the container.
builder.Services.AddTransient(sp => new MySqlConnection(connectionStringBuilder.ConnectionString));
builder.Services.AddTransient<MySqlStorage>();

// Add services to the container.

builder.Services.AddControllers();

var app = builder.Build();

// Configure the HTTP request pipeline.

app.MapControllers();

await app.RunAsync();
