import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import clsx from 'clsx';
import { 
  MapPinIcon, 
  BriefcaseIcon, 
  CurrencyDollarIcon, 
  BuildingOfficeIcon 
} from '@heroicons/react/24/outline';

const FEATURED_JOBS = [
  {
    id: 1,
    title: 'Senior Software Engineer',
    company: 'TechCorp',
    location: 'Kitale',
    type: 'Full-time',
    salary: '$120k - $180k',
    category: 'full-time'
  },
  {
    id: 2,
    title: 'Product Manager',
    company: 'InnovateCo',
    location: 'Nakuru',
    type: 'Full-time',
    salary: '$100k - $150k',
    category: 'full-time'
  },
  {
    id: 3,
    title: 'UX Designer',
    company: 'DesignHub',
    location: 'Remote',
    type: 'Full-time',
    salary: '$90k - $130k',
    category: 'full-time'
  },
  {
    id: 4,
    title: 'Software Engineering Intern',
    company: 'TechCorp',
    location: 'Makutano',
    type: 'Internship',
    salary: '$40/hr',
    category: 'internship'
  },
  {
    id: 5,
    title: 'Marketing Intern',
    company: 'InnovateCo',
    location: 'Bamburi',
    type: 'Internship',
    salary: '$35/hr',
    category: 'internship'
  },
  {
    id: 6,
    title: 'Data Science Intern',
    company: 'DataTech',
    location: 'Remote',
    type: 'Internship',
    salary: '$38/hr',
    category: 'internship'
  }
];

type JobCategory = 'all' | 'full-time' | 'internship';

export function FeaturedJobs() {
  const [selectedCategory, setSelectedCategory] = useState<JobCategory>('all');

  const filteredJobs = FEATURED_JOBS.filter(job => 
    selectedCategory === 'all' || job.category === selectedCategory
  );

  return (
    <section className="py-8 sm:py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 sm:gap-0 mb-8">
          <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">Featured Jobs</h2>
          <div className="flex flex-wrap gap-2">
            {(['all', 'full-time', 'internship'] as const).map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={clsx(
                  'px-3 sm:px-4 py-1.5 sm:py-2 text-sm sm:text-base rounded-lg font-medium transition-colors',
                  selectedCategory === category
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-600 hover:bg-gray-100'
                )}
              >
                {category.charAt(0).toUpperCase() + category.slice(1).replace('-', ' ')}
              </button>
            ))}
          </div>
        </div>
        <div className="grid gap-4 sm:gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {filteredJobs.map((job) => (
            <div key={job.id} className="bg-white rounded-lg shadow-sm p-4 sm:p-6 hover:shadow-md transition-shadow">
              <h3 className="text-lg sm:text-xl font-semibold text-gray-900">{job.title}</h3>
              <div className="flex items-center gap-2 mt-2 text-gray-600">
                <BuildingOfficeIcon className="h-4 sm:h-5 w-4 sm:w-5 flex-shrink-0" />
                <span className="truncate">{job.company}</span>
              </div>
              <div className="mt-4 space-y-2 sm:space-y-3">
                <div className="flex items-center gap-2 text-gray-500">
                  <MapPinIcon className="h-4 sm:h-5 w-4 sm:w-5 flex-shrink-0" />
                  <span className="truncate">{job.location}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-500">
                  <BriefcaseIcon className="h-4 sm:h-5 w-4 sm:w-5 flex-shrink-0" />
                  <span>{job.type}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-500">
                  <CurrencyDollarIcon className="h-4 sm:h-5 w-4 sm:w-5 flex-shrink-0" />
                  <span>{job.salary}</span>
                </div>
              </div>
              <Link
                to={`/jobs/${job.id}`}
                className="mt-4 inline-flex items-center text-blue-600 hover:text-blue-700 text-sm sm:text-base"
              >
                View Details
                <svg className="w-4 h-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </Link>
            </div>
          ))}
        </div>
        <div className="text-center mt-8 sm:mt-10">
          <Link
            to="/jobs"
            className="inline-block bg-blue-600 text-white px-6 sm:px-8 py-2.5 sm:py-3 rounded-lg font-semibold hover:bg-blue-700 text-sm sm:text-base"
          >
            View All Jobs
          </Link>
        </div>
      </div>
    </section>
  );
}