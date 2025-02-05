import { useState } from "react";
import { Link } from "react-router-dom";
import {
  MagnifyingGlassIcon,
  Bars3Icon,
  XMarkIcon,
} from "@heroicons/react/24/outline";

type Props = {
  searchQuery: string;
  setSearchQuery: (query: string) => void;
};

export function Header({ searchQuery, setSearchQuery }: Props) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  console.log(searchQuery);

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex-shrink-0">
            <Link to="/" className="text-2xl font-bold text-blue-600">
              JobConnect
            </Link>
          </div>

          <div className="hidden md:block flex-1 max-w-2xl mx-8">
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search jobs..."
                className="w-full pl-4 pr-10 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <MagnifyingGlassIcon className="h-5 w-5 text-gray-400 absolute right-3 top-2.5" />
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2 rounded-md text-gray-700 hover:text-blue-600 focus:outline-none"
            >
              {isMenuOpen ? (
                <XMarkIcon className="h-6 w-6" />
              ) : (
                <Bars3Icon className="h-6 w-6" />
              )}
            </button>
          </div>

          <nav className="hidden md:flex space-x-4">
            <Link to="/jobs" className="text-gray-700 hover:text-blue-600">
              Find Jobs
            </Link>
            <Link to="/employers" className="text-gray-700 hover:text-blue-600">
              For Employers
            </Link>
            <Link to="/login" className="text-gray-700 hover:text-blue-600">
              Sign In
            </Link>
            <Link
              to="/register"
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              Sign Up
            </Link>
          </nav>
        </div>

        {/* Mobile menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t">
            <div className="mb-4">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search jobs..."
                  className="w-full pl-4 pr-10 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <MagnifyingGlassIcon className="h-5 w-5 text-gray-400 absolute right-3 top-2.5" />
              </div>
            </div>
            <div className="flex flex-col space-y-3">
              <Link
                to="/jobs"
                className="text-gray-700 hover:text-blue-600 px-2 py-1"
              >
                Find Jobs
              </Link>
              <Link
                to="/employers"
                className="text-gray-700 hover:text-blue-600 px-2 py-1"
              >
                For Employers
              </Link>
              <Link
                to="/login"
                className="text-gray-700 hover:text-blue-600 px-2 py-1"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 text-center"
              >
                Sign Up
              </Link>
            </div>
          </div>
        )}
      </div>
    </header>
  );
}
