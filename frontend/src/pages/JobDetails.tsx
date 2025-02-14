import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { 
  MapPinIcon, 
  BriefcaseIcon, 
  CurrencyDollarIcon, 
  BuildingOfficeIcon 
} from '@heroicons/react/24/outline';
import { jobsApi, JobDetails as JobDetailsType } from '../lib/api';
import { useAuth } from '../contexts/AuthContext';

export function JobDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [job, setJob] = useState<JobDetailsType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [applying, setApplying] = useState(false);
  const [applicationSuccess, setApplicationSuccess] = useState(false);
  const [applicationError, setApplicationError] = useState('');

  useEffect(() => {
    async function fetchJob() {
      try {
        const data = await jobsApi.getJobById(Number(id));
        setJob(data);
      } catch (err) {
        setError('Failed to load job details');
        console.error('Error fetching job:', err);
      } finally {
        setLoading(false);
      }
    }

    if (id) {
      fetchJob();
    }
  }, [id]);

  const handleApply = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    setApplying(true);
    setApplicationError('');
    try {
      await jobsApi.applyForJob(Number(id));
      setApplicationSuccess(true);
    } catch (err) {
      setApplicationError('Failed to apply for the job. Please try again.');
      console.error('Error applying for job:', err);
    } finally {
      setApplying(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">Loading...</div>
      </div>
    );
  }

  if (error || !job) {
    return (
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">Job Not Found</h2>
          <p className="mt-2 text-gray-600">{error || "The job you're looking for doesn't exist."}</p>
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
          <h1 className="text-2xl font-bold text-gray-900">{job.details?.title}</h1>
          <div className="mt-2 flex items-center gap-2 text-gray-600">
            <BuildingOfficeIcon className="h-5 w-5" />
            <span>{job.details?.company_username}</span>
          </div>
        </div>
        
        <div className="p-6">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
            <div className="flex items-center gap-2 text-gray-600">
              <MapPinIcon className="h-5 w-5" />
              <span>{job.details?.category_name}</span>
            </div>
            <div className="flex items-center gap-2 text-gray-600">
              <BriefcaseIcon className="h-5 w-5" />
              <span>{job.details?.type}</span>
            </div>
            <div className="flex items-center gap-2 text-gray-600">
              <CurrencyDollarIcon className="h-5 w-5" />
              <span>${job.details?.min_salary.toLocaleString()} - ${job.details?.max_salary.toLocaleString()}</span>
            </div>
          </div>

          <div className="prose max-w-none">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Job Description</h2>
            <div className="whitespace-pre-wrap text-gray-600">{job.description}</div>
          </div>

          {applicationSuccess ? (
            <div className="mt-8 bg-green-50 text-green-700 p-4 rounded-md">
              Your application has been submitted successfully!
            </div>
          ) : (
            <div className="mt-8">
              {applicationError && (
                <div className="mb-4 text-red-600">{applicationError}</div>
              )}
              <button
                onClick={handleApply}
                disabled={applying}
                className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {applying ? 'Applying...' : 'Apply Now'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}