import {
  MapPinIcon,
  BriefcaseIcon,
  CurrencyDollarIcon,
  BuildingOfficeIcon,
} from "@heroicons/react/24/outline";
import { Card } from "./ui/card";
import { Jobs } from "typings";
import { Link } from "react-router-dom";

type Props = {
  job: Jobs;
};

const jobCard = ({ job }: Props) => {
  return (
    <Card className="h-full">
      <div
        key={job.id}
        className="bg-white rounded-lg shadow-sm p-4 sm:p-6 hover:shadow-md transition-shadow flex flex-col justify-between h-full "
      >
        <h3 className="text-lg sm:text-xl font-semibold text-gray-900">
          {job.title}
        </h3>
        <div className="flex items-center gap-2 mt-2 text-gray-600">
          <BuildingOfficeIcon className="h-4 sm:h-5 w-4 sm:w-5 flex-shrink-0" />
          <span className="truncate">{job.company_username}</span>
        </div>
        <div className="mt-4 space-y-2 sm:space-y-3">
          <div className="flex items-center gap-2 text-gray-500">
            <MapPinIcon className="h-4 sm:h-5 w-4 sm:w-5 flex-shrink-0" />
            <span className="truncate">Location Not Available</span>
          </div>
          <div className="flex items-center gap-2 text-gray-500">
            <BriefcaseIcon className="h-4 sm:h-5 w-4 sm:w-5 flex-shrink-0" />
            <span>{job.type}</span>
          </div>
          <div className="flex items-center gap-2 text-gray-500">
            <CurrencyDollarIcon className="h-4 sm:h-5 w-4 sm:w-5 flex-shrink-0" />
            <span>
              ${job.min_salary} - ${job.max_salary}
            </span>
          </div>
        </div>
        <Link
          to={`/jobs/details/${job.id}`}
          className="mt-4 inline-flex items-center text-blue-600 hover:text-blue-700 text-sm sm:text-base"
        >
          View Details
          <svg className="w-4 h-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
            <path
              fillRule="evenodd"
              d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
              clipRule="evenodd"
            />
          </svg>
        </Link>
      </div>
    </Card>
  );
};

export default jobCard;
