import React from "react";
import { Routes, Route } from "react-router-dom";
import { Header } from "./components/Header";
import { Hero } from "./components/Hero";
import FeaturedJobs from "./components/FeaturedJobs";

function HomePage() {
  return (
    <>
      <Hero />
      <FeaturedJobs />
    </>
  );
}

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          {/* Other routes will be added here */}
        </Routes>
      </main>
    </div>
  );
}

export default App;
