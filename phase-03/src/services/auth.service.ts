import { supabase } from "@/lib/auth/supabase";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export const authService = {
  async signIn({ email, password }: any) {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }
    
    const data = await response.json();
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token);
    }
    return data;
  },

  async signUp({ email, password }: any) {
    const response = await fetch(`${API_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Registration failed');
    }
    
    return response.json();
  },

  async signOut() {
    // Clear Supabase session if exists
    if (supabase) {
      await supabase.auth.signOut();
    }
    // Clear local JWT if exists
    localStorage.removeItem('access_token');
    
    // Clear all cookies as a fallback to ensure session is destroyed
    document.cookie.split(";").forEach((c) => {
      document.cookie = c
        .replace(/^ +/, "")
        .replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
    });
  },
};
