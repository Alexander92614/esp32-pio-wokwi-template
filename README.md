# Sistema de Control de LEDs con ESP32, Python y Blazor

Este proyecto implementa un sistema de control de LEDs utilizando un ESP32 (simulado en Wokwi), un servidor backend en Python, y una interfaz web en Blazor WebAssembly.

## Requisitos Previos

1. **Software necesario:**
   - [Visual Studio Code](https://code.visualstudio.com/)
   - [.NET SDK 9.0](https://dotnet.microsoft.com/download/dotnet/9.0)
   - [Python 3.12 o superior](https://www.python.org/downloads/)
   - [Git](https://git-scm.com/downloads)

2. **Extensiones de VS Code recomendadas:**
   - C# Dev Kit
   - Python
   - Python Extension Pack

## Estructura del Proyecto

```
esp32-pio-wokwi-template/
├── ApiServer/          # API Server en ASP.NET Core
├── BlazorApp/         # Aplicación web Blazor
├── backend/           # Servidor Python
│   ├── db.py         # Manejo de base de datos
│   ├── http_server.py # Servidor HTTP
│   └── ws_serial.py  # Puente WebSocket-Serial
├── data/             # Carpeta para la base de datos
├── src/              # Código del ESP32
└── wokwigw_v0.1.2_Windows_64bit/ # Gateway de Wokwi
```

## Instalación

1. **Clonar el repositorio:**
   
   a. Abre PowerShell o Command Prompt (cmd)
   
   b. Navega a la carpeta donde quieres guardar el proyecto, por ejemplo:
   ```bash
   cd C:\Users\TuUsuario\Documents\GitHub
   ```
   
   c. Clona el repositorio (reemplaza la URL con la de tu repositorio):
   ```bash
   git clone https://github.com/tuusuario/esp32-pio-wokwi-template.git
   ```
   
   d. Entra a la carpeta del proyecto:
   ```bash
   cd esp32-pio-wokwi-template
   ```

   > **Nota**: Si estás usando el proyecto por primera vez, deberás crear la carpeta `data` para la base de datos:
   ```bash
   mkdir data
   ```

2. **Instalar dependencias de Python:**
   ```bash
   pip install websockets
   pip install pyserial
   pip install pyserial-asyncio
   ```

3. **Instalar dependencias de .NET:**
   ```bash
   cd BlazorApp
   dotnet restore
   cd ../ApiServer
   dotnet restore
   ```

## Configuración

1. **Base de datos:**
   - La base de datos SQLite se creará automáticamente en la carpeta `data/`
   - No se requiere configuración adicional

2. **Configuración de puertos:**
   - Servidor Python HTTP: Puerto 5000
   - Servidor WebSocket: Puerto 8765
   - Gateway Wokwi: Puerto 4000
   - Aplicación Blazor: Puerto 5277

## Ejecución del Proyecto

0. **Antes de iniciar** - Si hay instancias previas corriendo, detenerlas:
   ```bash
   # Abre PowerShell como administrador y ejecuta:
   taskkill /F /IM python.exe /IM wokwigw.exe /IM dotnet.exe
   ```

1. **Iniciar el Gateway de Wokwi:**
   ```bash
   # En la carpeta raíz del proyecto:
   cd wokwigw_v0.1.2_Windows_64bit
   .\wokwigw.exe
   ```
   > Mantén esta ventana abierta

2. **Iniciar el Servidor Python:**
   ```bash
   # Abre una nueva terminal en la carpeta raíz del proyecto:
   python server.py
   ```
   > Mantén esta ventana abierta

3. **Iniciar la Aplicación Blazor:**
   ```bash
   # Abre una nueva terminal en la carpeta raíz del proyecto:
   cd BlazorApp
   dotnet run
   ```
   > Mantén esta ventana abierta

> **IMPORTANTE**: Cada servicio debe ejecutarse en su propia ventana de terminal y mantenerse en ejecución.

4. **Acceder a la Interfaz Web:**
   - Abrir en el navegador: http://localhost:5277/events

## Funcionalidades

1. **Control de LEDs:**
   - LED 1 (Azul): Control mediante botón en la interfaz
   - LED 2 (Verde): Control mediante botón en la interfaz

2. **Historial de Eventos:**
   - Registro de cambios de estado de los LEDs
   - Botones para eliminar eventos individuales
   - Botón para eliminar todo el historial

3. **Características Adicionales:**
   - Indicador de carga durante operaciones
   - Manejo de errores y reconexión automática
   - Interfaz responsiva

## Solución de Problemas

1. **Error de Puertos en Uso:**
   ```bash
   # Windows
   taskkill /F /IM python.exe /IM wokwigw.exe /IM dotnet.exe
   ```

2. **Base de Datos No Disponible:**
   - Verificar permisos en la carpeta `data/`
   - Reiniciar el servidor Python

3. **Problemas de Conexión WebSocket:**
   - La aplicación intentará reconectar automáticamente
   - Verificar que el servidor Python esté corriendo

## Contribución

1. Hacer fork del repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.