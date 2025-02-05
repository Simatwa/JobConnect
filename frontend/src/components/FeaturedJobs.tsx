import clsx from "clsx";
import JobCard from "./JobCard";
import { Button } from "./ui/button";
import { JobCategory, Jobs } from "typings";

type Props = {
  filteredJobs: Jobs[];
  selectedCategory: JobCategory;
  setSelectedCategory: (category: JobCategory) => void;
};

const FeaturedJobs = ({
  filteredJobs,
  selectedCategory,
  setSelectedCategory,
}: Props) => {
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
