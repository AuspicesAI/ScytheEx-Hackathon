import React, { useState, useEffect } from "react";
import { useRedisSubscriber } from "../../RedisSubscriber";
import { AlertTable, AlertsCard } from "./AlertsComponents";
import { AlertCardData, AlertTableColumns } from "./AlertsAssets";

// Sample data for the table
const initialRows = [
  {
    id: 1,
    reportedAt: "12:33:11",
    sourceIP: "192.168.1.1",
    sourcePort: 8080,
    destinationIP: "192.168.1.2",
    destinationPort: 80,
    flags: "SYN, ACK",
    severity: "Critical",
  },
  // Add more initial rows here...
];

function Dashboard() {
  const [rows, setRows] = useState(initialRows);

  const redisRows = useRedisSubscriber();

  useEffect(() => {
    // Format and merge the new rows with the existing ones
    const formattedRows = redisRows.map((row, index) => ({
      id: index + 1,
      duration: row.duration || "N/A",
      reportedAt: row.reportedAt || "N/A",
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
    <div className="relative py-8">
      <div className="flex flex-wrap">
        {AlertCardData.map((data, index) => (
          <AlertsCard key={index} {...data} />
        ))}
      </div>
      <div class="my-4 md:my-6 mx-auto w-full">
        <div class="flex flex-wrap">
          <AlertTable
            title="Latest Traffic"
            columns={AlertTableColumns}
            data={rows}
          />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
