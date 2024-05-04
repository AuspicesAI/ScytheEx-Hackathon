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
        {/* Replace with user's photo */}
        <div className="inset-y-0 left-0 flex items-center mr-4 pointer-events-none">
          <i className="fas fa-user"></i>
        </div>
        <span>Admin</span>

        {!isOpen && <i className="fas fa-chevron-down ml-4"></i>}
        {isOpen && <i className="fas fa-chevron-up ml-4"></i>}
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 py-2 sm:mt-3 w-48 bg-white rounded-md shadow-xl z-20">
          <div className="before:content-[''] before:block before:absolute before:border-solid before:border-transparent before:border-b-white before:border-l-8 before:border-r-8 before:border-b-8 before:-top-1 lg:before:right-12 sm:before:right-32 before:w-0 before:h-0"></div>
          <button className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">
            <i className="fas fa-screen mr-4"></i>
            Go to Screen
          </button>

          <button className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">
            <i className="fas fa-alt-bar mr-4"></i>
            Dashboard
          </button>

          <button className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">
            <i className="fas fa-alt-bar mr-4"></i>
            Reset Cameras
          </button>
        </div>
      )}
    </div>
  );
};

const Navbar = () => {
  return (
    <nav className="flex items-center p-6 bg-gradient-to-r from-black to-purple text-white">
      <div style={{ flex: 1 }}>
        <img src="/scth.png" className="h-16 w-auto cursor-pointer" />
      </div>

      <div style={{ flex: 1 }} className="flex justify-end">
        <DropdownMenu />
      </div>
    </nav>
  );
};

export default Navbar;
