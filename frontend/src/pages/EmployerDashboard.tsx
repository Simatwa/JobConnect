import React from 'react';
import { Link } from 'react-router-dom';
import {
  BriefcaseIcon,
  UserGroupIcon,
  ChartBarIcon,
  PlusIcon,
} from '@heroicons/react/24/outline';

export function EmployerDashboard() {
  const stats = [
    { label: 'Active Jobs', value: '12', icon: BriefcaseIcon },
    { label: 'Total Applicants', value: '48', icon: UserGroupIcon },
    { label: 'Views', value: '1,234', icon: ChartBarIcon },
  ];

  const activeJobs = [
    {
      id: 1,
      title: 'Senior Software Engineer',
      applicants: 15,
      views: 234,
      status: 'active',
      postedDate: '2023-08-15',
    },
    // Add more jobs...
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        {stats.map((stat) => (
          <div key={stat.label} className="bg-white p-6 rounded-lg shadow-sm">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <stat.icon className="h-6 w-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Actions */}
      <div className="mb-8">
        <Link
          to="/employers/post-job"
          className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          <PlusIcon className="h-5 w-5 mr-2" />
          Post New Job
        </Link>
      </div>

      {/* Active Jobs */}
      <div className="bg-white rounded-lg shadow-sm">
        <div className="p-6 border-b">
          <h2 className="text-lg font-semibold text-gray-900">Active Job Listings</h2>
        </div>
        <div className="divide-y">
          {activeJobs.map((job) => (
            <div key={job.id} className="p-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between">
                <div>
                  <h3 className="text-lg font-medium text-gray-900">{job.title}</h3>
                  <p className="text-sm text-gray-500">Posted on {job.postedDate}</p>
                </div>
                <div className="mt-4 sm:mt-0 flex flex-wrap gap-4">
                  <div className="text-sm">
                    <span className="text-gray-500">Applicants:</span>{' '}
                    <span className="font-medium text-gray-900">{job.applicants}</span>
                  </div>
                  <div className="text-sm">
                    <span className="text-gray-500">Views:</span>{' '}
                    <span className="font-medium text-gray-900">{job.views}</span>
                  </div>
                  <Link
                    to={`/employers/jobs/${job.id}`}
                    className="text-blue-600 hover:text-blue-700"
                  >
                    View Details
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}