using Microsoft.EntityFrameworkCore;
using ApiServer.Models;

namespace ApiServer.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options) { }

        public DbSet<Tarea> Tareas { get; set; }
    }
}
