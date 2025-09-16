import React from 'react';
import { ChevronDown } from 'lucide-react';
import { useSearch } from '../context/SearchContext';

type SortOption = {
  label: string;
  value: string;
  order: 'asc' | 'desc';
};

export const SortResults: React.FC = () => {
  const { sortResults } = useSearch();

  const sortOptions: SortOption[] = [
    { label: 'Price: Low to High', value: 'price_per_night', order: 'asc' },
    { label: 'Price: High to Low', value: 'price_per_night', order: 'desc' },
    { label: 'Rating: High to Low', value: 'rating', order: 'desc' },
    { label: 'Rating: Low to High', value: 'rating', order: 'asc' },
    { label: 'Name: A to Z', value: 'name', order: 'asc' },
    { label: 'Name: Z to A', value: 'name', order: 'desc' },
  ];

  const handleSort = (option: SortOption) => {
    sortResults(option.value, option.order);
  };

  return (
    <div className="relative inline-block text-left">
      <div className="group">
        <button
          type="button"
          className="inline-flex justify-between items-center w-48 rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          aria-haspopup="true"
          aria-expanded="true"
        >
          Sort By
          <ChevronDown className="h-4 w-4 ml-2" />
        </button>

        {/* Dropdown menu */}
        <div className="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 divide-y divide-gray-100 focus:outline-none z-50 hidden group-hover:block">
          <div className="py-1">
            {sortOptions.map((option) => (
              <button
                key={`${option.value}-${option.order}`}
                onClick={() => handleSort(option)}
                className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SortResults;
