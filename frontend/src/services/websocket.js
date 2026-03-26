// =========================
// WEBSOCKET CLIENT
// =========================

let socket;

export function connectWebSocket(onMessage) {
  socket = new WebSocket("ws://localhost:8000/ws");

  socket.onopen = () => {
    console.log("Connected to backend");
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (e) {
      console.error("WS parse error", e);
    }
  };

  socket.onerror = (err) => {
    console.error("WebSocket error", err);
  };

  socket.onclose = () => {
    console.log("WebSocket closed");
  };
}
