// Sample data for the table
export const initialRows = [
  {
    id: 1,
    protocol: "HTTP",
    sourceIP: "192.168.1.1",
    sourcePort: 8080,
    destinationIP: "192.168.1.2",
    destinationPort: 80,
    flags: "SYN, ACK",
    status: "Background",
  },
  // Add more initial rows here...
];

export const DashboardCardData = [
  {
    title: "Total Traffic",
    value: "350,897",
    icon: "far fa-chart-bar",
    percentageChange: "3.48",
    timePeriod: "Since last month",
    changeType: "up",
  },
  {
    title: "Normal Traffic",
    value: "2,356",
    icon: "fas fa-chart-pie",
    percentageChange: "3.48",
    timePeriod: "Since last week",
    changeType: "down",
  },
  {
    title: "Malacious Traffic",
    value: "924",
    icon: "fas fa-users",
    percentageChange: "1.10",
    timePeriod: "Since yesterday",
    changeType: "down",
  },
  {
    title: "Automated Prevention",
    value: "49,65%",
    icon: "fas fa-percent",
    percentageChange: "12",
    timePeriod: "Since last month",
    changeType: "up",
  },
];

export const trafficColumns = [
  { header: "Protocol", key: "protocol" },
  { header: "Source IP", key: "sourceIP" },
  { header: "Source Port", key: "sourcePort" },
  { header: "Destination IP", key: "destinationIP" },
  { header: "Destination Port", key: "destinationPort" },
  { header: "Flags", key: "flags" },
];

export const subColumns = [
  { header: "Source IP", key: "sourceIP" },
  { header: "Destination IP", key: "destinationIP" },
];
