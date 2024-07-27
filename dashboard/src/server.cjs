const { createClient } = require("@redis/client");

const express = require("express");
const http = require("http");
const cors = require("cors");
const { Server } = require("socket.io");

const app = express();
const allowedOrigins = ["http://localhost:5173", "http://127.0.0.1:5173"];

app.use(
  cors({
    origin: function (origin, callback) {
      if (!origin || allowedOrigins.includes(origin)) {
        callback(null, true);
      } else {
        callback(new Error("Not allowed by CORS"));
      }
    },
    methods: ["GET", "POST"],
  })
);

const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: allowedOrigins,
    methods: ["GET", "POST"],
  },
});

const redisClient = createClient({
  url: "redis://100.26.220.36:6380",
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
