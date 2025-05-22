const argIndex = process.argv.indexOf('--api-key');
let apiKey = process.env.COINGLASS_API_KEY;
if (argIndex !== -1 && process.argv.length > argIndex + 1) {
  apiKey = process.argv[argIndex + 1];
}

if (!apiKey) {
  console.error('An API key is required. Use --api-key or set COINGLASS_API_KEY.');
  process.exit(1);
}

const wssWebSocket = new WebSocket(`wss://open-ws.coinglass.com/ws-api?cg-api-key=${apiKey}`);
console.log(wssWebSocket.url); // 'wss://open-ws.coinglass.com/ws-api?cg-api-key=***'
wssWebSocket.close();
