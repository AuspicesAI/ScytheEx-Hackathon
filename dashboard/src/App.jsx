import React, { useState, useEffect } from "react";
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
import { useRedisSubscriber } from "./RedisSubscriber";

// Sample data for the table
const initialRows = [
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
  // Add more initial rows here...
];

// Function to return a styled span based on status
const StatusSpan = ({ status }) => {
  const style = {
    display: "inline-block",
    padding: "0.25em 0.7em",
    borderRadius: "12px",
    backgroundColor:
      status === "LEGITIMATE"
        ? "#006400" // Darker green
        : status === "Background"
        ? "#003366" // Darker blue
        : "#8b0000", // Darker red
    color: status === "Background" ? "#e2e2e2de" : "#e2e2e2de",
  };
  return <span style={style}>{status}</span>;
};

const CustomTable = ({ rows }) => {
  const tableCellStyles = {
    color: "#e2e2e2de",
    borderBottom: "1px solid #242424",
    padding: "8px 24px",
    height: "36px",
  };

  return (
    <TableContainer
      component={Paper}
      style={{ backgroundColor: "#0c0c0c", color: "white" }}
    >
      <Table aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell
              colSpan={9}
              align="center"
              style={{ backgroundColor: "#0c0c0c", color: "#e2e2e2de" }}
            >
              Network Traffic Data
            </TableCell>
          </TableRow>
          <TableRow>
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
            ].map((header) => (
              <TableCell key={header} style={tableCellStyles}>
                {header}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row, index) => (
            <TableRow key={index}>
              {Object.entries(row).map(([key, value]) => (
                <TableCell key={key} style={tableCellStyles}>
                  {key === "status" ? (
                    <StatusSpan status={value} />
                  ) : (
                    value.toString()
                  )}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

const MiniTable = ({ rows, title }) => {
  const tableCellStyles = {
    color: "#e2e2e2de",
    borderBottom: "1px solid #242424",
    padding: "8px 24px",
    height: "36px",
    width: "130px",
  };
  const headerCellStyles = { ...tableCellStyles, backgroundColor: "#0c0c0c" };

  return (
    <TableContainer
      component={Paper}
      style={{ backgroundColor: "#0c0c0c", color: "white" }}
    >
      <Table aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell
              colSpan={4}
              align="center"
              style={{ color: "white", backgroundColor: "#EF476F" }}
            >
              {title}
            </TableCell>
          </TableRow>
          <TableRow>
            {["ID", "Source IP", "Destination IP", "Status"].map((text) => (
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
          {rows.map((row, index) => (
            <TableRow key={index} style={{ borderBottom: "1px solid #242424" }}>
              <TableCell style={tableCellStyles}>{row.id}</TableCell>
              <TableCell style={tableCellStyles}>{row.sourceIP}</TableCell>
              <TableCell style={tableCellStyles}>{row.destinationIP}</TableCell>
              <TableCell style={tableCellStyles}>
                {row.status ? <StatusSpan status={row.status} /> : "N/A"}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

function App() {
  const [rows, setRows] = useState(initialRows);

  const redisRows = useRedisSubscriber();

  useEffect(() => {
    // Format and merge the new rows with the existing ones
    const formattedRows = redisRows.map((row, index) => ({
      id: index + 1,
      duration: row.duration || "N/A",
      protocol: row.protocol || "N/A",
      sourceIP: row.sourceIP || "N/A",
      sourcePort: row.sourcePort || "N/A",
      destinationIP: row.destinationIP || "N/A",
      destinationPort: row.destinationPort || "N/A",
      flags: row.flags || "N/A",
      status: row.status || "N/A",
    }));

    // Merge formatted rows with existing rows and ensure the maximum length is 8
    const newRows = [...rows, ...formattedRows].slice(-8);

    setRows(newRows);
  }, [redisRows]);

  return (
    <section className="flex flex-col items-center h-screen text-white">
      <div className="py-6 max-w-[1280px]">
        <CustomTable rows={rows} />
      </div>
      <div className="flex flex-row justify-between gap-4 max-w-[1280px]">
        <MiniTable
          rows={rows.filter(
            (row) => row.status !== "Background" && row.status !== "LEGITIMATE"
          )}
          title="Latest Malicious Traffic"
        />
        <MiniTable
          rows={rows.filter(
            (row) => row.status === "Background" || row.status === "LEGITIMATE"
          )}
          title="Latest Benign Traffic"
        />
      </div>
    </section>
  );
}

export default App;
