// Function to return a styled span based on status
const SeveritySpan = ({ status }) => {
  const style = {
    display: "inline-block",
    padding: "0.25em 0.7em",
    borderRadius: "12px",
    backgroundColor:
      status === "Critical"
        ? "#3E2723" // Darker green
        : status === "High"
        ? "#e53e3e" // Darker blue
        : status === "Medium"
        ? "#FF9800" // Darker red
        : status === "Low"
        ? "#FFEE58"
        : "#8b0000", // Darker red
    color: status === "Background" ? "#e2e2e2de" : "#e2e2e2de",
  };
  return <span style={style}>{status}</span>;
};

export const AlertTable = ({ title, columns = [], data = [] }) => {
  // Add "ID" column and Status column to columns array
  const modifiedColumns = [
    { header: "ID", key: "id" },
    { header: "Severity", key: "severity" },
    ...columns,
  ];

  return (
    <div className="w-full px-4">
      <div className="relative flex flex-col min-w-0 break-words w-full mb-8 shadow-lg rounded-lg bg-gray-900 text-blueGray-700">
        <div className="px-6 py-4 border-0">
          <div className="flex flex-wrap items-center">
            <div className="relative w-full max-w-full flex-grow flex-1">
              <h3 className="font-bold text-lg text-blueGray-700">{title}</h3>
            </div>
          </div>
        </div>
        <div className="block w-full overflow-x-auto">
          <table className="items-center w-full bg-transparent border-collapse">
            <thead>
              <tr>
                {modifiedColumns.map((column, index) => (
                  <th
                    key={index}
                    className="px-6 align-middle border border-solid py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-bold text-left bg-gray-800 text-blueGray-500 border-blueGray-200"
                  >
                    {column.header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                    <div className="flex items-center">{row.id}</div>
                  </td>
                  <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                    <div className="flex items-center">
                      <SeveritySpan status={row.severity} />
                    </div>
                  </td>
                  {columns.map((column, colIndex) => (
                    <td
                      key={colIndex}
                      className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4"
                    >
                      <div className="flex items-center">{row[column.key]}</div>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export const AlertsCard = ({
  title,
  value,
  icon,
  color, // Expected to be the color class name
}) => {
  const backgroundColor =
    {
      "brown-900": "#3E2723",
      "red-600": "#e53e3e",
      "orange-500": "#FF9800",
      "yellow-400": "#FFEE58",
      // Add more colors here if needed
    }[color] || "#000"; // Fallback color

  return (
    <div className="w-full lg:w-6/12 xl:w-3/12 px-4">
      <div className="relative flex flex-col min-w-0 break-words bg-gray-900 rounded-lg mb-6 xl:mb-0 shadow-lg">
        <div className="flex-auto p-4">
          <div className="flex flex-wrap">
            <div className="relative w-full pr-4 max-w-full flex-grow flex-1">
              <h5 className="text-blueGray-400 uppercase font-bold text-xs">
                {title}
              </h5>
              <span className="font-bold text-xl">{value}</span>
            </div>
            <div className="relative w-auto pl-4 flex-initial">
              <div
                className="text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 shadow-lg rounded-full"
                style={{ backgroundColor }}
              >
                <i className={icon}></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
