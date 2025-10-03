using System.Net.WebSockets;
using System.Text;

namespace BlazorApp;

public class WebSocketService : IDisposable
{
    private ClientWebSocket? _ws;
    private readonly Uri _uri = new("ws://localhost:8765");
    private CancellationTokenSource _cts = new();
    private bool _isConnected;

    public bool IsConnected
    {
        get => _isConnected;
        private set
        {
            if (_isConnected != value)
            {
                _isConnected = value;
                ConnectionStateChanged?.Invoke(value);
            }
        }
    }

    public event Action<string>? MessageReceived;
    public event Action<bool>? ConnectionStateChanged;

    public async Task ConnectAsync()
    {
        if (_ws?.State == WebSocketState.Open) return;

        while (!_cts.Token.IsCancellationRequested)
        {
            try
            {
                _ws = new ClientWebSocket();
                await _ws.ConnectAsync(_uri, _cts.Token);
                IsConnected = true;
                Console.WriteLine("WebSocket Connected!");
                await ReceiveLoop();
                break;
            }
            catch (Exception e)
            {
                IsConnected = false;
                Console.WriteLine($"WebSocket connection failed: {e.Message}");
                await Task.Delay(3000, _cts.Token); // Esperar 3 segundos antes de reintentar
            }
        }
    }

    public async Task SendAsync(string message)
    {
        if (_ws?.State != WebSocketState.Open)
        {
            Console.WriteLine("Cannot send message, WebSocket is not open.");
            return;
        }
        var buffer = Encoding.UTF8.GetBytes(message);
        await _ws.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, true, _cts.Token);
    }

    private async Task ReceiveLoop()
    {
        var buffer = new byte[1024 * 4];
        try
        {
            while (_ws?.State == WebSocketState.Open)
            {
                var result = await _ws.ReceiveAsync(new ArraySegment<byte>(buffer), _cts.Token);
                if (result.MessageType == WebSocketMessageType.Close) break;

                var message = Encoding.UTF8.GetString(buffer, 0, result.Count);
                MessageReceived?.Invoke(message);
            }
        }
        catch (Exception e)
        {
            Console.WriteLine($"WebSocket receive loop error: {e.Message}");
            IsConnected = false;
            await AttemptReconnect();
        }
        finally
        {
            if (!_cts.Token.IsCancellationRequested)
            {
                IsConnected = false;
                Console.WriteLine("WebSocket receive loop ended, attempting to reconnect...");
                await AttemptReconnect();
            }
        }
    }

    private async Task AttemptReconnect()
    {
        while (!_cts.Token.IsCancellationRequested && (_ws?.State != WebSocketState.Open))
        {
            try
            {
                _ws?.Dispose();
                _ws = new ClientWebSocket();
                await _ws.ConnectAsync(_uri, _cts.Token);
                IsConnected = true;
                Console.WriteLine("WebSocket reconnected successfully!");
                break;
            }
            catch (Exception e)
            {
                Console.WriteLine($"WebSocket reconnection failed: {e.Message}");
                await Task.Delay(3000, _cts.Token);
            }
        }
    }

    public void Dispose()
    {
        IsConnected = false;
        _cts.Cancel();
        _ws?.Dispose();
    }
}
