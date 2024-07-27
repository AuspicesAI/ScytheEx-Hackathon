import React from "react";
import { useState } from "react";

const DropdownMenu = () => {
  const [isOpen, setIsOpen] = useState(false);
  const toggleDropdown = () => setIsOpen(!isOpen);

  return (
    <div className="relative">
      <button
        onClick={toggleDropdown}
        className="flex items-center text-primary-white"
      >
        <div className="inset-y-0 left-0 flex items-center mr-3 pointer-events-none">
          <i className="fas fa-user"></i>
        </div>
        <span>Admin</span>

        {!isOpen && <i className="fas pr-2 fa-chevron-down ml-3"></i>}
        {isOpen && <i className="fas fa-chevron-up pr-2 ml-3"></i>}
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 py-2 sm:mt-3 w-48 bg-white rounded-md shadow-xl z-20">
          <button className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">
            <i className="fas fa-sign-out-alt mr-4 text-gray-700"></i> Sign Out
          </button>
          <button className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">
            <i className="fas fa-power-off mr-4 text-gray-700"></i> Shut Down
          </button>
        </div>
      )}
    </div>
  );
};

const Navbar = () => {
  return (
    <div className="fixed w-full flex items-center bg-gray-800 justify-between h-14 text-white z-10">
      <div className="flex items-center justify-start md:justify-center border-none">
        <img
          className="w-auto h-7 md:w-auto md:h-10 m-2 rounded-md overflow-hidden"
          src="./scth.png"
        />
      </div>
      <div className="flex justify-between items-center h-14 bg-blue-800 dark:bg-gray-800 header-right">
        <ul className="flex items-center">
          <li>
            <div className="block w-px h-6 mx-3 bg-gray-400 dark:bg-gray-700"></div>
          </li>
          <li>
            <DropdownMenu />
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Navbar;
