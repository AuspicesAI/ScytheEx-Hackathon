export const Dropdown = ({ label, value, options, onChange, className }) => {
  return (
    <div className={`grid grid-cols-1 md:grid-cols-2 gap-4 ${className}`}>
      <div>
        <label className="block text-sm font-medium mb-1">{label}</label>
        <select
          value={value}
          onChange={onChange}
          className="bg-gray-900 rounded-lg mb-6 xl:mb-0 shadow-lg p-3 w-full"
        >
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};

export const TextInput = ({ label, type, value, onChange }) => {
  return (
    <div>
      <label className="block text-sm font-medium mb-1">{label}</label>
      <input
        type={type}
        value={value}
        onChange={onChange}
        className="bg-gray-900 rounded-lg mb-6 xl:mb-0 shadow-lg p-3 w-full"
      />
    </div>
  );
};

export const CustomCheckbox = ({ checked, onChange, label }) => {
  return (
    <label className="flex items-center cursor-pointer">
      <div className="relative">
        <input
          type="checkbox"
          checked={checked}
          onChange={onChange}
          className="sr-only"
        />
        <div className="w-6 h-6 border border-gray-300 rounded-md bg-white flex items-center justify-center shadow-sm">
          {checked && (
            <svg
              className="w-4 h-4 text-primary-pink"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M5 13l4 4L19 7"
              />
            </svg>
          )}
        </div>
      </div>
      <span className="ml-3 text-sm text-gray-700 dark:text-gray-300">
        {label}
      </span>
    </label>
  );
};
