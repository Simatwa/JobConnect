import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { Hero } from './components/Hero';
import { FeaturedJobs } from './components/FeaturedJobs';
import { JobDetails } from './pages/JobDetails';
import { UserProfile } from './pages/UserProfile';
import { Login } from './pages/Login';
import { Register } from './pages/Register';

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
    <AuthProvider>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Header />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/jobs/:id" element={<JobDetails />} />
            <Route path="/profile" element={<UserProfile />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </AuthProvider>
  );
}

export default App;