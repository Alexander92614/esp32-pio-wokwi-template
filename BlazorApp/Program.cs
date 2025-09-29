using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using BlazorApp;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri("http://localhost:5000/") });

builder.Services.AddSingleton<WebSocketService>();

// Configurar el servicio WebSocket
var webSocketService = new WebSocketService();
await webSocketService.ConnectAsync();
builder.Services.AddSingleton(webSocketService);

await builder.Build().RunAsync();
