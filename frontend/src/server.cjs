const { createClient } = require("@redis/client");

const express = require("express");
const http = require("http");
const cors = require("cors");
const { Server } = require("socket.io");

const app = express();
app.use(cors()); // This sets up CORS for all routes and methods.

const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "http://localhost:5173", // Specify the client origin explicitly
    methods: ["GET", "POST"],
  },
});

const redisClient = createClient({
  url: "redis://3.84.243.99:6380",
});

async function startServer() {
  await redisClient.connect();

  // Subscribe to Redis channel
  await redisClient.subscribe("prediction_channel", (message) => {
    console.log("Received message from Redis:", message);
    io.emit("new-data", JSON.parse(message)); // Emitting data to all connected WebSocket clients
  });

  io.on("connection", (socket) => {
    console.log("A user connected");

    socket.on("disconnect", () => {
      console.log("User disconnected");
    });
  });

  server.listen(3000, () => {
    console.log("Server listening on *:3000");
  });
}

startServer().catch((err) => {
  console.error("Error starting server:", err);
  process.exit(1);
});
