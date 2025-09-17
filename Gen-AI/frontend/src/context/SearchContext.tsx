import React, { createContext, useContext, useState } from 'react';
import axios from 'axios';

interface FilterOptions {
  priceRange: { min: number; max: number };
  rating: number;
  amenities: string[];
  travelDates: { start: string; end: string };
  tripDuration: { min: number; max: number };
}

interface SortConfig {
  key: string;
  order: 'asc' | 'desc';
}

interface SearchContextType {
  searchResults: any[];
  loading: boolean;
  error: string | null;
  filters: FilterOptions;
  setFilters: (filters: FilterOptions) => void;
  search: (criteria: any) => Promise<void>;
  sortResults: (key: string, order: 'asc' | 'desc') => void;
  currentSort: SortConfig | null;
}

const SearchContext = createContext<SearchContextType | undefined>(undefined);

const initialFilters: FilterOptions = {
  priceRange: { min: 0, max: 10000 },
  rating: 0,
  amenities: [],
  travelDates: { start: '', end: '' },
  tripDuration: { min: 1, max: 30 }
};

export const SearchProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<FilterOptions>(initialFilters);
  const [currentSort, setCurrentSort] = useState<SortConfig | null>(null);

  const search = async (criteria: any) => {
    try {
      setLoading(true);
      setError(null);

      const response = await axios.post(
        `http://localhost:8000/api/search/${criteria.type}s`,
        { ...criteria, filters }
      );

      let results = response.data[`${criteria.type}s`] || [];
      
      // Apply current sort if exists
      if (currentSort) {
        results = sortByConfig(results, currentSort);
      }
      
      setSearchResults(results);
    } catch (err) {
      setError('Failed to fetch search results');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const sortByConfig = (results: any[], config: SortConfig) => {
    return [...results].sort((a, b) => {
      let aVal = a[config.key];
      let bVal = b[config.key];
      
      // Handle nested properties (e.g., 'location.city')
      if (config.key.includes('.')) {
        aVal = config.key.split('.').reduce((obj, key) => obj[key], a);
        bVal = config.key.split('.').reduce((obj, key) => obj[key], b);
      }
      
      if (aVal < bVal) return config.order === 'asc' ? -1 : 1;
      if (aVal > bVal) return config.order === 'asc' ? 1 : -1;
      return 0;
    });
  };

  const sortResults = (key: string, order: 'asc' | 'desc') => {
    const newConfig = { key, order };
    setCurrentSort(newConfig);
    setSearchResults(sortByConfig(searchResults, newConfig));
  };

  return (
    <SearchContext.Provider 
      value={{ 
        searchResults, 
        loading, 
        error, 
        search, 
        filters, 
        setFilters,
        sortResults,
        currentSort
      }}
    >
      {children}
    </SearchContext.Provider>
  );
};

export const useSearch = () => {
  const context = useContext(SearchContext);
  if (context === undefined) {
    throw new Error('useSearch must be used within a SearchProvider');
  }
  return context;
};
