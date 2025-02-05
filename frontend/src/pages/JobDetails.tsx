import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import {
  MapPinIcon,
  BriefcaseIcon,
  CurrencyDollarIcon,
  BuildingOfficeIcon,
} from "@heroicons/react/24/outline";
import axios from "axios";
import { JobType } from "../../typings";

export function JobDetails() {
  const [jobDetails, setjobDetailsDetails] = useState<JobType | null>(null);
  const { id } = useParams();
  // console.log(id);
  const fetchjobDetailsDetails = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/api/v1/job/${id}`,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      setjobDetailsDetails(response.data);
      console.log(jobDetails);
    } catch (error) {
      setjobDetailsDetails(null);
    }
  };

  useEffect(() => {
    if (id) fetchjobDetailsDetails();
  }, [id]);

  if (!jobDetails) {
    return (
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">
            Job Details Not Found
          </h2>
          <p className="mt-2 text-gray-600">
            The job details you're looking for doesn't exist.
          </p>
          <Link
            to="/"
            className="mt-4 inline-block text-blue-600 hover:text-blue-700"
          >
            View All job
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-white rounded-lg shadow-sm">
        <div className="p-6 border-b">
          <h1 className="text-2xl font-bold text-gray-900">
            {jobDetails.details.title}
          </h1>
          <div className="mt-2 flex items-center gap-2 text-gray-600">
            <BuildingOfficeIcon className="h-5 w-5" />
            <span>{jobDetails.details.company_username}</span>
          </div>
        </div>

        <div className="p-6">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
            <div className="flex items-center gap-2 text-gray-600">
              <MapPinIcon className="h-5 w-5" />
              <span>{jobDetails.details.location || "Not provided"}</span>
            </div>
            <div className="flex items-center gap-2 text-gray-600">
              <BriefcaseIcon className="h-5 w-5" />
              <span>{jobDetails.details.type}</span>
            </div>
            <div className="flex items-center gap-2 text-gray-600">
              <CurrencyDollarIcon className="h-5 w-5" />
              <span>
                {" "}
                ${jobDetails.details.max_salary} - $
                {jobDetails.details.min_salary}
              </span>
            </div>
          </div>

          <div className="prose max-w-none">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Job Description
            </h2>
            <div className="whitespace-pre-wrap text-gray-600">
              {jobDetails?.description
                ? jobDetails?.description
                : "No description provided"}
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
