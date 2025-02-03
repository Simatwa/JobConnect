import React from 'react';
import { Link } from 'react-router-dom';

export function Footer() {
  return (
    <footer className="bg-white border-t">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">JobConnect</h3>
            <p className="text-gray-600">
              Connecting talented professionals with great opportunities.
            </p>
          </div>
          
          <div>
            <h4 className="text-sm font-semibold text-gray-900 mb-4">For Job Seekers</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/jobs" className="text-gray-600 hover:text-blue-600">
                  Browse Jobs
                </Link>
              </li>
              <li>
                <Link to="/profile" className="text-gray-600 hover:text-blue-600">
                  Create Profile
                </Link>
              </li>
              <li>
                <Link to="/saved-jobs" className="text-gray-600 hover:text-blue-600">
                  Saved Jobs
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-gray-900 mb-4">For Employers</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/employers" className="text-gray-600 hover:text-blue-600">
                  Post a Job
                </Link>
              </li>
              <li>
                <Link to="/pricing" className="text-gray-600 hover:text-blue-600">
                  Pricing
                </Link>
              </li>
              <li>
                <Link to="/resources" className="text-gray-600 hover:text-blue-600">
                  Resources
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-gray-900 mb-4">Company</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/about" className="text-gray-600 hover:text-blue-600">
                  About Us
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-gray-600 hover:text-blue-600">
                  Contact
                </Link>
              </li>
              <li>
                <Link to="/privacy" className="text-gray-600 hover:text-blue-600">
                  Privacy Policy
                </Link>
              </li>
            </ul>
          </div>
        </div>
        
        <div className="mt-8 pt-8 border-t">
          <p className="text-center text-gray-500">
            © {new Date().getFullYear()} JobConnect. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}