import React from 'react';
import { Link } from 'react-router-dom';

export function Hero() {
  return (
    <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 md:py-20">
        <div className="text-center">
          <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
            Find Your Dream Job or Internship Today
          </h1>
          <p className="mt-4 sm:mt-6 text-lg sm:text-xl text-blue-100 max-w-3xl mx-auto">
            Connect with top employers and opportunities. Whether you're looking for a full-time position or an internship, your next career move starts here.
          </p>
          <div className="mt-8 sm:mt-10 flex flex-col sm:flex-row justify-center gap-4 sm:gap-6">
            <Link
              to="/register"
              className="bg-white text-blue-600 px-6 sm:px-8 py-2.5 sm:py-3 rounded-lg font-semibold hover:bg-blue-50 text-sm sm:text-base"
            >
              Get Started
            </Link>
            <Link
              to="/jobs"
              className="border-2 border-white text-white px-6 sm:px-8 py-2.5 sm:py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 text-sm sm:text-base"
            >
              Browse Jobs
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}