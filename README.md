# Sistema de Control ESP32 con Blazor WebAssembly y Wokwi

Un sistema completo de control y monitoreo para ESP32 que integra simulación virtual Wokwi, interfaz web moderna con Blazor WebAssembly, API RESTful con .NET 9.0, servidor Python WebSocket y base de datos SQLite para persistencia de datos.

## 🚀 Características Principales

- **ESP32 Firmware**: Control de 2 LEDs (pines 26 y 27) vía comandos serie
- **Simulación Wokwi**: Entorno virtual con circuito definido en `diagram.json`
- **Blazor WebAssembly**: Interfaz moderna con páginas de Control, Monitor, Config, Events e Historial
- **API RESTful**: Backend .NET 9.0 con Entity Framework Core y gestión de tareas
- **Python WebSocket Server**: Comunicación bidireccional en tiempo real
- **Base de Datos SQLite**: Persistencia de tareas, eventos y historial de LEDs
- **Dashboard en Tiempo Real**: Estado de conexión, uptime y estadísticas del sistema

## 📋 Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Blazor App    │◄──►│  Python Server  │◄──►│   ESP32/Wokwi   │
│  (Frontend)     │    │  (WebSocket)    │    │   (Hardware)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   C# API        │    │   SQLite DB     │
│  (Backend)      │◄──►│   (Storage)     │
└─────────────────┘    └─────────────────┘
```

## 🛠️ Tecnologías Utilizadas

### Frontend
- **Blazor WebAssembly** (.NET 9.0)
- **Radzen Blazor Components**
- **WebSocket Client**

### Backend
- **ASP.NET Core API** (.NET 9.0)
- **Entity Framework Core**
- **SQLite Database**

### Comunicación
- **Python WebSocket Server**
- **RFC2217 Serial Bridge**
- **Real-time messaging**

### Hardware/Simulación
- **ESP32** (Arduino Framework)
- **Wokwi Simulator**
- **PlatformIO**

## 📁 Estructura del Proyecto

```
esp32-pio-wokwi-template/
├── src/                    # Código ESP32 (Arduino)
│   └── main.cpp           # Firmware principal con control de LEDs
├── BlazorApp/             # Frontend Blazor WebAssembly
│   ├── Pages/             # Páginas: Home, Control, Monitor, Config, Events, HistorialLeds
│   ├── Layout/            # Layout principal y navegación
│   ├── Shared/            # Componentes compartidos
│   ├── wwwroot/           # Recursos estáticos
│   └── WebSocketService.cs # Servicio de comunicación WebSocket
├── ApiServer/             # Backend API C# (.NET 9.0)
│   ├── Controllers/       # TareasController para gestión de tareas
│   ├── Models/            # Modelo Tarea
│   ├── Data/              # ApplicationDbContext
│   ├── Migrations/        # Migraciones de Entity Framework
│   └── tareas.db          # Base de datos SQLite
├── backend/               # Servidor Python WebSocket
│   ├── http_server.py     # Servidor HTTP
│   ├── ws_serial.py       # WebSocket y comunicación serie
│   ├── db.py              # Gestión de base de datos
│   └── config.py          # Configuración del sistema
├── data/                  # Almacenamiento de datos
│   └── events.db          # Base de datos de eventos
├── wokwigw_v0.1.2_Windows_64bit/  # Wokwi Gateway para Windows
├── diagram.json           # Definición del circuito Wokwi
├── wokwi.toml            # Configuración de Wokwi
├── platformio.ini        # Configuración de PlatformIO
└── requirements.txt      # Dependencias Python
```

## 🚀 Instalación y Configuración

### Prerequisitos

- **.NET 9.0 SDK**
- **Python 3.11+**
- **PlatformIO** (VS Code Extension)
- **Node.js** (para herramientas de desarrollo)

### 1. Clonar el Repositorio

```bash
git clone [repository-url]
cd esp32-pio-wokwi-template
```

### 2. Configurar Python Environment

```powershell
# Crear y activar entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Base de Datos

```powershell
cd ApiServer
dotnet ef database update
```

### 4. Construir el Firmware ESP32

```bash
# Usando PlatformIO
pio build
```

## 🎮 Uso del Sistema

### Iniciar el Sistema Completo

Para ejecutar el sistema completo, necesitas iniciar cada componente en terminales separadas:

1. **Wokwi Gateway** (puerto 4000)
2. **Python WebSocket Server** (puerto 8765) 
3. **C# API Server** (puerto 5000)
4. **Blazor WebAssembly App** (puerto 5001)

### Uso Manual

#### 1. Iniciar Wokwi Gateway
```powershell
cd wokwigw_v0.1.2_Windows_64bit
.\wokwigw.exe --rfc2217-server-port 4000
```

#### 2. Iniciar Python Server
```powershell
python server.py
```

#### 3. Iniciar API Server
```powershell
cd ApiServer
dotnet run
```

#### 4. Iniciar Blazor App
```powershell
cd BlazorApp
dotnet run
```

## 🔧 Funcionalidades

### Páginas Web Disponibles

- **Home** (`/`): Dashboard principal con estado de conexión, tiempo activo y estadísticas
- **Control** (`/control`): Interfaz para control manual de LEDs del ESP32
- **Monitor** (`/monitor`): Monitoreo en tiempo real del estado del sistema
- **Events** (`/events`): Registro y visualización del historial de eventos
- **Config** (`/config`): Configuración y parámetros del sistema
- **HistorialLeds** (`/historial-leds`): Historial detallado de cambios de estado de LEDs

### Comandos ESP32

| Comando | Descripción | Pin |
|---------|-------------|-----|
| `TOGGLE_1` | Alternar estado del LED 1 | GPIO 26 |
| `TOGGLE_2` | Alternar estado del LED 2 | GPIO 27 |
| `GET_STATE` | Obtener estado actual de ambos LEDs | - |

**Respuestas del ESP32:**
- `LED1_ON` / `LED1_OFF`: Estado del LED 1
- `LED2_ON` / `LED2_OFF`: Estado del LED 2

### API Endpoints

- `GET /api/tareas` - Listar todas las tareas
- `POST /api/tareas` - Crear nueva tarea
- `PUT /api/tareas/{id}` - Actualizar tarea
- `DELETE /api/tareas/{id}` - Eliminar tarea

## 🔌 Configuración de Puertos y Hardware

### Puertos de Red
| Servicio | Puerto | Descripción |
|----------|---------|-------------|
| Wokwi Gateway | 4000 | RFC2217 Serial Bridge |
| Python WebSocket | 8765 | Comunicación en tiempo real |
| C# API Server | 5000 | API RESTful |
| Blazor App | 5001 | Frontend web |

### Configuración Hardware ESP32
| Componente | Pin GPIO | Descripción |
|------------|----------|-------------|
| LED 1 | 26 | LED controlable vía comando TOGGLE_1 |
| LED 2 | 27 | LED controlable vía comando TOGGLE_2 |
| Resistencias | - | 1000Ω para limitación de corriente |

## 📊 Base de Datos

### Bases de Datos

#### ApiServer/tareas.db (SQLite)
- **Tareas**: Gestión de tareas con campos Id, Titulo, Completada

#### data/events.db (SQLite)
- **Events**: Registro cronológico de eventos del sistema
- **LedHistory**: Historial detallado de cambios de estado de LEDs

## 🐛 Troubleshooting

### Problemas Comunes

1. **Puerto ocupado**: Verificar que los puertos estén libres
2. **Base de datos**: Ejecutar migraciones si hay errores
3. **Python dependencies**: Reinstalar requirements.txt
4. **Wokwi connection**: Verificar que Wokwi Gateway esté corriendo

### Logs

- **Python Server**: `server.log`
- **API Server**: Consola de dotnet
- **Blazor App**: Consola del navegador (F12)

## 🧪 Testing

### Probar Comunicación WebSocket

```python
# Test script incluido
python -c "import asyncio; from backend.ws_serial import test_connection; asyncio.run(test_connection())"
```

### Probar API

```bash
curl http://localhost:5000/api/tareas
```

## 📝 Desarrollo

### Agregar Nuevas Páginas Blazor

1. Crear archivo `.razor` en `BlazorApp/Pages/`
2. Agregar ruta en `NavMenu.razor`
3. Implementar lógica de componente

### Extender API

1. Crear modelo en `ApiServer/Models/`
2. Agregar DbSet en `ApplicationDbContext`
3. Crear migración: `dotnet ef migrations add [Name]`
4. Crear controller en `ApiServer/Controllers/`

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📞 Soporte

Para soporte y preguntas:
- Abrir un issue en GitHub
- Revisar la documentación en el código
- Consultar logs del sistema

---

**Nota**: Este proyecto utiliza Wokwi para simulación. Para uso con hardware real, ajustar la configuración de puertos serie en el código Python.