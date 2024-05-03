import React, { useState } from "react";
import "./App.css";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";

// Sample data for the table
const rows = [
  {
    id: 1,
    duration: "30s",
    protocol: "HTTP",
    sourceIP: "192.168.1.1",
    sourcePort: 8080,
    destinationIP: "192.168.1.2",
    destinationPort: 80,
    flags: "SYN, ACK",
    status: "Normal",
  },
  {
    id: 2,
    duration: "45s",
    protocol: "HTTPS",
    sourceIP: "192.168.1.3",
    sourcePort: 443,
    destinationIP: "192.168.1.4",
    destinationPort: 443,
    flags: "FIN",
    status: "Background",
  },
  {
    id: 3,
    duration: "10s",
    protocol: "FTP",
    sourceIP: "192.168.1.5",
    sourcePort: 21,
    destinationIP: "192.168.1.6",
    destinationPort: 21,
    flags: "SYN",
    status: "Error",
  },
];

// Function to return a styled span based on status
const StatusSpan = ({ status }) => {
  const style = {
    display: "inline-block",
    padding: "0.25em 0.7em",
    borderRadius: "12px",
    backgroundColor:
      status === "Normal"
        ? "#006400" // Darker green
        : status === "Background"
        ? "#003366" // Darker blue
        : "#8b0000", // Darker red
    color: status === "Background" ? "#e2e2e2de" : "#e2e2e2de",
  };
  return <span style={style}>{status}</span>;
};

const CustomTable = () => {
  const tableCellStyles = {
    color: "#e2e2e2de",
    borderBottom: "1px solid #242424",
    padding: "8px 24px",
    height: "36px",
  };
  const headerCellStyles = { ...tableCellStyles, backgroundColor: "#0c0c0c" };

  return (
    <TableContainer
      component={Paper}
      style={{ backgroundColor: "#0c0c0c", color: "white" }}
    >
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow style={{ borderBottom: "1px solid #242424" }}>
            {[
              "ID",
              "Duration",
              "Protocol",
              "Source IP",
              "Source Port",
              "Destination IP",
              "Destination Port",
              "Flags",
              "Status",
            ].map((text) => (
              <TableCell
                key={text}
                align={text === "ID" ? "inherit" : "right"}
                style={headerCellStyles}
              >
                {text}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={row.id}
              sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              style={{ borderBottom: "1px solid #242424" }}
            >
              {Object.entries(row).map(([key, value]) => (
                <TableCell
                  key={key}
                  component={key === "id" ? "th" : undefined}
                  scope={key === "id" ? "row" : undefined}
                  align={key === "id" ? "inherit" : "right"}
                  style={tableCellStyles}
                >
                  {key === "status" ? <StatusSpan status={value} /> : value}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

function App() {
  const [count, setCount] = useState(0);

  return (
    <section className="flex items-center justify-center h-screen text-white">
      <div className="w-full">
        <CustomTable />
      </div>
    </section>
  );
}

export default App;
