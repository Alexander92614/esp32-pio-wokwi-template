using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using BlazorApp;
using Radzen;
using Microsoft.Extensions.Logging;

try
{
    var builder = WebAssemblyHostBuilder.CreateDefault(args);
    builder.RootComponents.Add<App>("#app");
    builder.RootComponents.Add<HeadOutlet>("head::after");

    // Habilitar errores detallados en desarrollo
    #if DEBUG
    builder.Services.AddLogging(logging =>
    {
        logging.SetMinimumLevel(LogLevel.Debug);
        logging.AddFilter("Microsoft.AspNetCore.Components.WebAssembly", LogLevel.Warning);
    });
    #endif

    // Agregar servicios Radzen
    builder.Services.AddScoped<DialogService>();
    builder.Services.AddScoped<NotificationService>();
    builder.Services.AddScoped<TooltipService>();
    builder.Services.AddScoped<ContextMenuService>();

    builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) });
    builder.Services.AddSingleton<WebSocketService>();

    var host = builder.Build();
    await host.RunAsync();
}
catch (Exception ex)
{
    Console.Error.WriteLine($"Application startup failed: {ex.Message}");
    throw;
}
