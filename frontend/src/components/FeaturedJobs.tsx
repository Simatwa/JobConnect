import axios from "axios";
import { useEffect, useState } from "react";
import JobCard from "./JobCard";
import { JobCategory, Jobs } from "../../typings";
import { Button } from "./ui/button";
import clsx from "clsx";

const FeaturedJobs = () => {
  const [jobs, setJobs] = useState<Jobs[]>([]);
  const [selectedCategory, setSelectedCategory] =
    useState<JobCategory>("full-time");

  const fetchJobs = async () => {
    const response = await axios.get(`http://localhost:8000/api/v1/jobs`, {
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.data.jobs;

    // console.log(data);
    setJobs(data);
    console.log(data);

    if (Array.isArray(data)) {
      setJobs(data);
    } else {
      setJobs([]);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);
  //Filtering jobs based on category

  const filteredJobs =
    selectedCategory === "all"
      ? jobs
      : jobs.filter((job) => job.type.toLowerCase() === selectedCategory);

  // console.log(jobs.type)

  return (
    <section className="py-8 sm:py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 ">
        <div className=" flex flex-col justify-start items-center sm:items-start   gap-4 sm:gap-3  mb-8 ">
          <h2 className="text-2xl text-start sm:text-3xl font-bold text-gray-900">
            Featured Jobs
          </h2>

          <div className="flex flex-wrap gap-2 ml-auto">
            {(["all", "full-time", "internship"] as const).map((category) => (
              <Button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={clsx(
                  "px-3 sm:px-4 py-1.5 sm:py-2 text-sm sm:text-base rounded-lg font-medium transition-colors capitalize",
                  selectedCategory === category
                    ? "bg-blue-600 text-white"
                    : "bg-white text-gray-600 hover:bg-gray-100"
                )}
              >
                {category.charAt(0).toUpperCase() +
                  category.slice(1).replace("-", " ")}
              </Button>
            ))}
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {filteredJobs.length > 0 ? (
              filteredJobs?.map((job) => {
                // console.log(job.category_id);

                return (
                  <div key={job.id} className="">
                    <JobCard job={job} />
                  </div>
                );
              })
            ) : (
              <p>No job available for this category</p>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};

export default FeaturedJobs;

// import React, { useEffect, useState } from "react";
// import { Link } from "react-router-dom";
// import clsx from "clsx";
// import {
//   MapPinIcon,
//   BriefcaseIcon,
//   CurrencyDollarIcon,
//   BuildingOfficeIcon,
// } from "@heroicons/react/24/outline";
// import axios from "axios";

// type Job = {
//   id: number;
//   title: string;
//   type: string;
//   category_id: number;
//   category_name: string;
//   company_id: number;
//   company_username: string;
//   min_salary: number;
//   max_salary: number;
//   updated_at: string;
// };

// type JobCategory = "all" | "full-time" | "internship";

// export function FeaturedJobs() {
//   const [selectedCategory, setSelectedCategory] = useState<JobCategory>("all");
//   const [jobs, setJobs] = useState<Job[]>([]);

//   const fetchJobs = async () => {
//     try {
//       const response = await axios.get("http://localhost:8000/api/v1/jobs", {
//         headers: {
//           "Content-Type": "application/json",
//         },
//       });
//       setJobs(response.data);

//       if (Array.isArray(response.data)) {
//         setJobs(response.data);
//       } else {
//         console.error("Unexpected API response:", response.data);
//         setJobs([]);
//       }
//     } catch (error) {
//       console.error("Error fetching jobs:", error);
//     }
//   };

//   useEffect(() => {
//     fetchJobs();
//   }, []);

//   // Filter jobs based on the selected category
//   const filteredJobs =
//     selectedCategory === "all"
//       ? jobs
//       : jobs.filter(
//           (job) => job.category_name.toLowerCase() === selectedCategory
//         );

//   return (
//     <section className="py-8 sm:py-16 bg-gray-50">
//       <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
//         <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 sm:gap-0 mb-8">
//           <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">
//             Featured Jobs
//           </h2>
//           <div className="flex flex-wrap gap-2">
//             {(["all", "full-time", "internship"] as const).map((category) => (
//               <button
//                 key={category}
//                 onClick={() => setSelectedCategory(category)}
//                 className={clsx(
//                   "px-3 sm:px-4 py-1.5 sm:py-2 text-sm sm:text-base rounded-lg font-medium transition-colors",
//                   selectedCategory === category
//                     ? "bg-blue-600 text-white"
//                     : "bg-white text-gray-600 hover:bg-gray-100"
//                 )}
//               >
//                 {category.charAt(0).toUpperCase() +
//                   category.slice(1).replace("-", " ")}
//               </button>
//             ))}
//           </div>
//         </div>
//         <div className="grid gap-4 sm:gap-6 sm:grid-cols-2 lg:grid-cols-3">
//           {filteredJobs.length > 0 ? (
//             filteredJobs.map((job) => {
//               console.log(job);

//               return (
//                 <div
//                   key={job.id}
//                   className="bg-white rounded-lg shadow-sm p-4 sm:p-6 hover:shadow-md transition-shadow"
//                 >
//                   <h3 className="text-lg sm:text-xl font-semibold text-gray-900">
//                     {job.title}
//                   </h3>
//                   <div className="flex items-center gap-2 mt-2 text-gray-600">
//                     <BuildingOfficeIcon className="h-4 sm:h-5 w-4 sm:w-5 flex-shrink-0" />
//                     <span className="truncate">{job.company_username}</span>
//                   </div>
//                   <div className="mt-4 space-y-2 sm:space-y-3">
//                     <div className="flex items-center gap-2 text-gray-500">
//                       <MapPinIcon className="h-4 sm:h-5 w-4 sm:w-5 flex-shrink-0" />
//                       <span className="truncate">Location Not Available</span>
//                     </div>
//                     <div className="flex items-center gap-2 text-gray-500">
//                       <BriefcaseIcon className="h-4 sm:h-5 w-4 sm:w-5 flex-shrink-0" />
//                       <span>{job.type}</span>
//                     </div>
//                     <div className="flex items-center gap-2 text-gray-500">
//                       <CurrencyDollarIcon className="h-4 sm:h-5 w-4 sm:w-5 flex-shrink-0" />
//                       <span>
//                         ${job.min_salary} - ${job.max_salary}
//                       </span>
//                     </div>
//                   </div>
//                   <Link
//                     to={`/jobs/${job.id}`}
//                     className="mt-4 inline-flex items-center text-blue-600 hover:text-blue-700 text-sm sm:text-base"
//                   >
//                     View Details
//                     <svg
//                       className="w-4 h-4 ml-1"
//                       viewBox="0 0 20 20"
//                       fill="currentColor"
//                     >
//                       <path
//                         fillRule="evenodd"
//                         d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
//                         clipRule="evenodd"
//                       />
//                     </svg>
//                   </Link>
//                 </div>
//               );
//             })
//           ) : (
//             <p className="text-gray-500 text-center col-span-full">
//               No jobs available in this category.
//             </p>
//           )}
//         </div>
//         <div className="text-center mt-8 sm:mt-10">
//           <Link
//             to="/jobs"
//             className="inline-block bg-blue-600 text-white px-6 sm:px-8 py-2.5 sm:py-3 rounded-lg font-semibold hover:bg-blue-700 text-sm sm:text-base"
//           >
//             View All Jobs
//           </Link>
//         </div>
//       </div>
//     </section>
//   );
// }
