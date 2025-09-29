namespace ApiServer.Models
{
    public class Tarea
    {
        public int Id { get; set; }
        public string Titulo { get; set; } = string.Empty;
        public bool Completada { get; set; }
    }
}
