import { useEffect, useState } from "react";
import { Route, Routes } from "react-router-dom";
import { Footer } from "./components/Footer";
import { Header } from "./components/Header";
import { AuthProvider } from "./contexts/AuthContext";

import axios from "axios";
import { JobCategory, Jobs } from "typings";
import FindJobs from "./pages/FindJobs";
import { JobDetails } from "./pages/JobDetails";
import { Login } from "./pages/Login";
import { Register } from "./pages/Register";
import { UserProfile } from "./pages/UserProfile";
import HomePage from "./components/home";

const API_OPTIONS = {
  headers: {
    "Content-Type": "application/json",
  },
};

function App() {
  const [jobs, setJobs] = useState<Jobs[]>([]);
  const [selectedCategory, setSelectedCategory] =
    useState<JobCategory>("full-time");
  const [searchQuery, setSearchQuery] = useState("");

  const fetchJobs = async (query = "") => {
    const endpoint = query
      ? `http://localhost:8000/api/v1/jobs?query=${searchQuery}`
      : `http://localhost:8000/api/v1/jobs`;

    const response = await axios.get(endpoint, API_OPTIONS);

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
  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Header searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
        <main className="flex-1">
          <Routes>
            <Route
              path="/"
              element={
                <HomePage
                  filteredJobs={filteredJobs}
                  selectedCategory={selectedCategory}
                  setSelectedCategory={setSelectedCategory}
                />
              }
            />
            <Route path="/jobs/details/:id" element={<JobDetails />} />
            <Route path="/profile" element={<UserProfile />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/jobs" element={<FindJobs />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </AuthProvider>
  );
}

export default App;
