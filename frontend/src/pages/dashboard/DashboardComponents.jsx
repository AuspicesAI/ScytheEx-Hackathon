export const DashTable = ({ title, columns = [], data = [] }) => {
  // Add "ID" column and Status column to columns array
  const modifiedColumns = [
    { header: "ID", key: "id" },
    ...columns,
    { header: "Status", key: "status" },
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
                  {columns.map((column, colIndex) => (
                    <td
                      key={colIndex}
                      className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4"
                    >
                      <div className="flex items-center">{row[column.key]}</div>
                    </td>
                  ))}
                  <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                    <div className="flex items-center">
                      <StatusSpan status={row.status} />
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

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

export const DashboardCard = ({
  title,
  value,
  icon,
  percentageChange,
  changeType,
}) => {
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
                className={`text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 shadow-lg rounded-full bg-primary-pink`}
              >
                <i className={icon}></i>
              </div>
            </div>
          </div>
          <p className="text-sm text-blueGray-500 mt-4">
            <span
              className={
                changeType === "up" ? "text-emerald-500" : "text-red-500"
              }
            >
              <i
                className={
                  changeType === "up" ? "fas fa-arrow-up" : "fas fa-arrow-down"
                }
              ></i>{" "}
              {percentageChange}%
            </span>
            <span className="whitespace-nowrap"> Yesterday</span>
          </p>
        </div>
      </div>
    </div>
  );
};
