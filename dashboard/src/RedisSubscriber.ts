import { useState, useEffect } from "react";
import io from "socket.io-client";

interface PacketData {
  id: number;
  duration: string;
  protocol: string;
  sourceIP: string;
  sourcePort: number;
  destinationIP: string;
  destinationPort: number;
  flags: string;
  status: string;
}

// URL of the Node.js server where Socket.IO is running
const SERVER_URL = "http://localhost:3000";

export const useRedisSubscriber = () => {
  const [rows, setRows] = useState<PacketData[]>([]);
  const socket = io(SERVER_URL);

  useEffect(() => {
    // Connect to the WebSocket server
    socket.on("connect", () => {
      console.log("Connected to WebSocket server!");
    });

    // Subscribe to the data stream from the server
    socket.on("new-data", (newData) => {
      console.log(newData);
      const formattedData = {
        id: newData[0]["id"] || "N/A",
        duration: newData[0]["Duration"] || "N/A",
        protocol: newData[0]["Protocol"] || "N/A",
        sourceIP: newData[0]["Source IP"] || "N/A",
        sourcePort: newData[0]["Source Port"] || "N/A",
        destinationIP: newData[0]["Destination IP"] || "N/A",
        destinationPort: newData[0]["Destination Port"] || "N/A",
        flags: newData[0]["Flags"] || "N/A",
        status: newData[0]["Status"] || "N/A",
      };

      setRows((prevRows) => {
        const updatedRows = [...prevRows, formattedData];
        return updatedRows.length > 8 ? updatedRows.slice(-8) : updatedRows;
      });
    });

    console.log("new-data");

    // Clean up the effect
    return () => {
      socket.off("new-data");
      socket.close();
    };
  }, [socket]); // Include socket in dependency array to handle clean up correctly
  console.log(rows);
  return rows;
};
