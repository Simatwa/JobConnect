import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  MapPinIcon, 
  BriefcaseIcon, 
  CurrencyDollarIcon, 
  BuildingOfficeIcon 
} from '@heroicons/react/24/outline';

const JOBS = [
  {
    id: 1,
    title: 'Senior Software Engineer',
    company: 'TechCorp',
    location: 'San Francisco, CA',
    type: 'Full-time',
    salary: '$120k - $180k',
    description: `We are seeking a Senior Software Engineer to join our team. The ideal candidate will have:

- 5+ years of experience with modern web technologies
- Strong knowledge of React, TypeScript, and Node.js
- Experience with cloud platforms (AWS, GCP, or Azure)
- Excellent problem-solving and communication skills
- Track record of leading technical projects

You will be responsible for:
- Architecting and implementing new features
- Mentoring junior developers
- Contributing to technical decisions
- Improving system performance and reliability`
  },
  {
    id: 2,
    title: 'Product Manager',
    company: 'InnovateCo',
    location: 'New York, NY',
    type: 'Full-time',
    salary: '$100k - $150k',
    description: 'Experienced Product Manager needed to lead product development...'
  }
];

export function JobDetails() {
  const { id } = useParams();
  const job = JOBS.find(j => j.id === Number(id));

  if (!job) {
    return (
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">Job Not Found</h2>
          <p className="mt-2 text-gray-600">The job you're looking for doesn't exist.</p>
          <Link to="/jobs" className="mt-4 inline-block text-blue-600 hover:text-blue-700">
            View All Jobs
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-white rounded-lg shadow-sm">
        <div className="p-6 border-b">
          <h1 className="text-2xl font-bold text-gray-900">{job.title}</h1>
          <div className="mt-2 flex items-center gap-2 text-gray-600">
            <BuildingOfficeIcon className="h-5 w-5" />
            <span>{job.company}</span>
          </div>
        </div>
        
        <div className="p-6">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
            <div className="flex items-center gap-2 text-gray-600">
              <MapPinIcon className="h-5 w-5" />
              <span>{job.location}</span>
            </div>
            <div className="flex items-center gap-2 text-gray-600">
              <BriefcaseIcon className="h-5 w-5" />
              <span>{job.type}</span>
            </div>
            <div className="flex items-center gap-2 text-gray-600">
              <CurrencyDollarIcon className="h-5 w-5" />
              <span>{job.salary}</span>
            </div>
          </div>

          <div className="prose max-w-none">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Job Description</h2>
            <div className="whitespace-pre-wrap text-gray-600">{job.description}</div>
          </div>

          <div className="mt-8">
            <Link
              to="/apply"
              className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700"
            >
              Apply Now
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}