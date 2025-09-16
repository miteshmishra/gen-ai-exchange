import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';
import { toast } from 'react-hot-toast';

interface PreferenceOptions {
  travel_styles: string[];
  room_types: string[];
  seat_preferences: string[];
  cabin_classes: string[];
  currencies: string[];
  languages: string[];
  amenities: string[];
  activities: string[];
  accessibility_options: string[];
}

interface UserPreferences {
  preferred_destinations: string[];
  preferred_activities: string[];
  travel_style: string;
  preferred_amenities: string[];
  room_type: string;
  max_price_per_night: number;
  preferred_airlines: string[];
  seat_preference: string;
  cabin_class: string;
  email_notifications: boolean;
  price_alerts: boolean;
  deal_notifications: boolean;
  preferred_currency: string;
  preferred_language: string;
  accessibility_needs: string[];
}

interface PreferencesContextType {
  preferences: UserPreferences | null;
  options: PreferenceOptions | null;
  isLoading: boolean;
  updatePreferences: (updates: Partial<UserPreferences>) => Promise<void>;
}

const PreferencesContext = createContext<PreferencesContextType | undefined>(undefined);

export const PreferencesProvider: React.FC<{ children: React.ReactNode }> = ({
  children
}) => {
  const [preferences, setPreferences] = useState<UserPreferences | null>(null);
  const [options, setOptions] = useState<PreferenceOptions | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const { isAuthenticated, token } = useAuth();

  const fetchPreferences = async () => {
    if (!isAuthenticated || !token) {
      setPreferences(null);
      setIsLoading(false);
      return;
    }

    try {
      const response = await axios.get('http://localhost:8000/api/preferences', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPreferences(response.data);
    } catch (error) {
      console.error('Error fetching preferences:', error);
      toast.error('Failed to load preferences');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchOptions = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/preferences/available-options');
      setOptions(response.data);
    } catch (error) {
      console.error('Error fetching preference options:', error);
    }
  };

  useEffect(() => {
    fetchPreferences();
    fetchOptions();
  }, [isAuthenticated, token]);

  const updatePreferences = async (updates: Partial<UserPreferences>) => {
    if (!isAuthenticated) {
      toast.error('Please log in to update preferences');
      return;
    }

    try {
      const response = await axios.put(
        'http://localhost:8000/api/preferences',
        updates,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setPreferences(response.data);
      toast.success('Preferences updated successfully');
    } catch (error) {
      console.error('Error updating preferences:', error);
      toast.error('Failed to update preferences');
    }
  };

  return (
    <PreferencesContext.Provider
      value={{
        preferences,
        options,
        isLoading,
        updatePreferences,
      }}
    >
      {children}
    </PreferencesContext.Provider>
  );
};

export const usePreferences = () => {
  const context = useContext(PreferencesContext);
  if (context === undefined) {
    throw new Error('usePreferences must be used within a PreferencesProvider');
  }
  return context;
};
