using System.Net.WebSockets;
using System.Text;

namespace BlazorApp;

public class WebSocketService : IDisposable
{
    private ClientWebSocket? _ws;
    private readonly Uri _uri = new("ws://localhost:8765");
    private CancellationTokenSource _cts = new();

    public event Action<string>? MessageReceived;
    public event Action? ConnectionClosed;
    public event Action<string>? ConnectionError;

    public async Task ConnectAsync()
    {
        if (_ws?.State == WebSocketState.Open) return;

        _ws = new ClientWebSocket();
        try
        {
            await _ws.ConnectAsync(_uri, _cts.Token);
            Console.WriteLine("WebSocket Connected!");
            _ = ReceiveLoop();
        }
        catch (Exception e)
        {
            Console.WriteLine($"WebSocket connection failed: {e.Message}");
            ConnectionError?.Invoke(e.Message);
            throw;
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
                if (result.MessageType == WebSocketMessageType.Close)
                {
                    ConnectionClosed?.Invoke();
                    break;
                }

                var message = Encoding.UTF8.GetString(buffer, 0, result.Count);
                MessageReceived?.Invoke(message);
            }

            if (_ws?.State != WebSocketState.Open)
            {
                ConnectionClosed?.Invoke();
            }
        }
        catch (Exception e)
        {
            Console.WriteLine($"WebSocket receive loop error: {e.Message}");
            ConnectionError?.Invoke(e.Message);
        }
        finally
        {
            Console.WriteLine("WebSocket receive loop ended.");
            if (_ws?.State != WebSocketState.Open)
            {
                ConnectionClosed?.Invoke();
            }
        }
    }

    public void Dispose()
    {
        _cts.Cancel();
        _ws?.Dispose();
    }
}
