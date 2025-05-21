const wssWebSocket = new WebSocket("wss://open-ws.coinglass.com/ws-api?cg-api-key={53b0a3236d8d4d2b9fff517c70c544ea}");
console.log(wssWebSocket.url); // 'wss://websocket.example.org'

// Do something with socket

wssWebSocket.close();
