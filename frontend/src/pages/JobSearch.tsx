import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  MapPinIcon, 
  BriefcaseIcon, 
  CurrencyDollarIcon, 
  BuildingOfficeIcon,
  FunnelIcon,
} from '@heroicons/react/24/outline';
import { jobsApi } from '../lib/api';

export function JobSearch() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    type: '',
    category: '',
  });

  useEffect(() => {
    async function fetchJobs() {
      try {
        const data = await jobsApi.getJobs({
          type: filters.type as any || undefined,
        });
        setJobs(data.jobs);
      } catch (err) {
        setError('Failed to load jobs');
        console.error('Error fetching jobs:', err);
      } finally {
        setLoading(false);
      }
    }

    fetchJobs();
  }, [filters]);

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  if (error) {
    return <div className="text-center py-8 text-red-600">{error}</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex flex-col md:flex-row gap-6">
        {/* Filters */}
        <div className="w-full md:w-64 flex-shrink-0">
          <div className="bg-white p-4 rounded-lg shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Filters</h2>
              <FunnelIcon className="h-5 w-5 text-gray-500" />
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Job Type
                </label>
                <select
                  className="w-full px-3 py-2 border rounded-md"
                  value={filters.type}
                  onChange={(e) => setFilters({ ...filters, type: e.target.value })}
                >
                  <option value="">All Types</option>
                  <option value="Full-time">Full Time</option>
                  <option value="Internship">Internship</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Job Listings */}
        <div className="flex-1">
          <div className="space-y-4">
            {jobs.map((job) => (
              <div key={job.id} className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{job.title}</h3>
                    <div className="flex items-center gap-2 mt-2 text-gray-600">
                      <BuildingOfficeIcon className="h-5 w-5 flex-shrink-0" />
                      <span className="truncate">{job.company_username}</span>
                    </div>
                  </div>
                  <Link
                    to={`/jobs/${job.id}`}
                    className="mt-4 sm:mt-0 inline-flex items-center text-blue-600 hover:text-blue-700"
                  >
                    View Details
                    <svg className="w-4 h-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                  </Link>
                </div>
                <div className="mt-4 flex flex-wrap gap-4">
                  <div className="flex items-center gap-2 text-gray-500">
                    <MapPinIcon className="h-5 w-5 flex-shrink-0" />
                    <span>{job.category_name}</span>
                  </div>
                  <div className="flex items-center gap-2 text-gray-500">
                    <BriefcaseIcon className="h-5 w-5 flex-shrink-0" />
                    <span>{job.type}</span>
                  </div>
                  <div className="flex items-center gap-2 text-gray-500">
                    <CurrencyDollarIcon className="h-5 w-5 flex-shrink-0" />
                    <span>${job.min_salary.toLocaleString()} - ${job.max_salary.toLocaleString()}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}