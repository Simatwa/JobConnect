import React, { createContext, useContext, useState } from 'react';
import { authApi } from '../lib/api';
import axios from 'axios';

interface AuthContextType {
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  signIn: (username: string, password: string) => Promise<void>;
  signUp: (userData: SignUpData) => Promise<void>;
  signOut: () => Promise<void>;
  updateProfile: (userId: number, userData: UpdateUserData) => Promise<void>;
  deleteAccount: (userId: number) => Promise<void>;
}

export interface SignUpData {
  username: string;
  password: string;
  email: string;
  first_name: string;
  last_name?: string;
  phone_number: string;
  location: string;
  category: 'Organization' | 'Individual';
  description?: string;
}

export interface UpdateUserData extends Partial<SignUpData> {}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [loading, setLoading] = useState(false);

  const isAuthenticated = !!token;

  async function signIn(username: string, password: string) {
    setLoading(true);
    try {
      // First get the API token from FastAPI
      const { access_token } = await authApi.login(username, password);
      
      // Then use the token to login through Django
      await axios.get(`http://localhost:8000/d/user/login`, {
        params: { token: access_token }
      });
      
      localStorage.setItem('token', access_token);
      setToken(access_token);
    } finally {
      setLoading(false);
    }
  }

  async function signUp(userData: SignUpData) {
    setLoading(true);
    try {
      const formData = new URLSearchParams();
      Object.entries(userData).forEach(([key, value]) => {
        if (value !== undefined) {
          formData.append(key, value.toString());
        }
      });

      // Send signup data to Django endpoint
      await axios.post('http://localhost:8000/d/user/create', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      
      // After successful registration, sign in
      await signIn(userData.username, userData.password);
    } finally {
      setLoading(false);
    }
  }

  async function signOut() {
    try {
      await axios.get('http://localhost:8000/d/user/logout');
      localStorage.removeItem('token');
      setToken(null);
    } catch (error) {
      console.error('Error during logout:', error);
      // Still remove token from local storage even if server logout fails
      localStorage.removeItem('token');
      setToken(null);
    }
  }

  async function updateProfile(userId: number, userData: UpdateUserData) {
    setLoading(true);
    try {
      const formData = new URLSearchParams();
      Object.entries(userData).forEach(([key, value]) => {
        if (value !== undefined) {
          formData.append(key, value.toString());
        }
      });

      await axios.post(`http://localhost:8000/d/user/update/${userId}`, formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
    } finally {
      setLoading(false);
    }
  }

  async function deleteAccount(userId: number) {
    setLoading(true);
    try {
      await axios.post(`http://localhost:8000/d/user/delete/${userId}`);
      await signOut();
    } finally {
      setLoading(false);
    }
  }

  const value = {
    token,
    isAuthenticated,
    loading,
    signIn,
    signUp,
    signOut,
    updateProfile,
    deleteAccount,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}