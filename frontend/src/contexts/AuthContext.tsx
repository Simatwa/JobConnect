import React, { createContext, useContext, useState } from 'react';
import { authApi } from '../lib/api';

interface AuthContextType {
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  signIn: (username: string, password: string) => Promise<void>;
  signOut: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [loading, setLoading] = useState(false);

  const isAuthenticated = !!token;

  async function signIn(username: string, password: string) {
    setLoading(true);
    try {
      const { access_token } = await authApi.login(username, password);
      localStorage.setItem('token', access_token);
      setToken(access_token);
    } finally {
      setLoading(false);
    }
  }

  function signOut() {
    localStorage.removeItem('token');
    setToken(null);
  }

  const value = {
    token,
    isAuthenticated,
    loading,
    signIn,
    signOut,
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