
using ApiServer.Data;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// 1. Añadir servicios para los controladores de la API
builder.Services.AddControllers();

// 2. Configurar la política de CORS para permitir cualquier origen (ideal para desarrollo)
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll",
        builder => builder
            .AllowAnyOrigin()
            .AllowAnyMethod()
            .AllowAnyHeader());
});

builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    // 3. Usar Swagger para documentar y probar la API
    app.UseSwagger();
    app.UseSwaggerUI();
}

// 4. Habilitar CORS y mapear los controladores
app.UseCors("AllowAll");
// Comentamos la redirección HTTPS para desarrollo
// app.UseHttpsRedirection();

// Agregar una ruta de prueba
app.MapGet("/", () => "API Server is running!");
app.MapControllers();

app.Run();
