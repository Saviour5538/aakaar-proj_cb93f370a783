import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
  };

  return (
    <nav className="bg-gray-800 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold">
              DocMind
            </Link>
            <div className="hidden md:block ml-10 space-x-4">
              <Link to="/dashboard" className="hover:text-gray-300">
                Dashboard
              </Link>
              <Link to="/documents" className="hover:text-gray-300">
                Documents
              </Link>
              <Link to="/conversations" className="hover:text-gray-300">
                Conversations
              </Link>
              <Link to="/chat" className="hover:text-gray-300">
                Chat
              </Link>
            </div>
          </div>
          <div className="hidden md:block">
            {user ? (
              <button
                onClick={handleLogout}
                className="bg-red-500 hover:bg-red-600 text-white px-3 py-2 rounded"
              >
                Logout
              </button>
            ) : (
              <Link to="/login" className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-2 rounded">
                Login
              </Link>
            )}
          </div>
          <div className="md:hidden">
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="text-gray-300 hover:text-white focus:outline-none"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d={isMobileMenuOpen ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16m-7 6h7'}
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
      {isMobileMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <Link to="/dashboard" className="block hover:bg-gray-700 px-3 py-2 rounded">
              Dashboard
            </Link>
            <Link to="/documents" className="block hover:bg-gray-700 px-3 py-2 rounded">
              Documents
            </Link>
            <Link to="/conversations" className="block hover:bg-gray-700 px-3 py-2 rounded">
              Conversations
            </Link>
            <Link to="/chat" className="block hover:bg-gray-700 px-3 py-2 rounded">
              Chat
            </Link>
            {user && (
              <button
                onClick={handleLogout}
                className="block w-full text-left hover:bg-gray-700 px-3 py-2 rounded"
              >
                Logout
              </button>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;