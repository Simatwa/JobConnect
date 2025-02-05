import { JobCategory, Jobs } from "typings";
import FeaturedJobs from "./FeaturedJobs";
import { Hero } from "./Hero";

type Props = {
  filteredJobs: Jobs[];
  selectedCategory: JobCategory;
  setSelectedCategory: (category: JobCategory) => void;
};

export default function HomePage({
  filteredJobs,
  selectedCategory,
  setSelectedCategory,
}: Props) {
  return (
    <>
      <Hero />
      <FeaturedJobs
        filteredJobs={filteredJobs}
        selectedCategory={selectedCategory}
        setSelectedCategory={setSelectedCategory}
      />
    </>
  );
}
