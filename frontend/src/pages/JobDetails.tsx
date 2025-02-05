import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import {
  MapPinIcon,
  BriefcaseIcon,
  CurrencyDollarIcon,
  BuildingOfficeIcon,
} from "@heroicons/react/24/outline";
import axios from "axios";
import { Jobs, JobType } from "../../typings";

export function JobDetails() {
  const [jobs, setJobs] = useState<JobType[]>([]);
  const [jobDetails, setJobDetails] = useState<Jobs | null>(null);
  const { id } = useParams();
  console.log(id);
  const fetchJobDetails = async () => {
    const response = await axios.get(`http://localhost:8000/api/v1/job/${id}`, {
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.data;
    setJobs(data);
    console.log(data);
  };

  useEffect(() => {
    fetchJobDetails();
  }, [id]);

  useEffect(() => {
    if (id && jobs.length > 0) {
      const job = jobs.find((job) => job.id === parseInt(id));
      setJobDetails(job || null);
    }
  }, []);

  if (!job) {
    return (
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">Job Not Found</h2>
          <p className="mt-2 text-gray-600">
            The job you're looking for doesn't exist.
          </p>
          <Link
            to="/"
            className="mt-4 inline-block text-blue-600 hover:text-blue-700"
          >
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
            <span>{job.company_username}</span>
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
              <span>
                {" "}
                ${job.min_salary} - ${job.max_salary}
              </span>
            </div>
          </div>

          <div className="prose max-w-none">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Job Description
            </h2>
            <div className="whitespace-pre-wrap text-gray-600">
              {job.description ? job.description : "No description provided"}
            </div>
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
