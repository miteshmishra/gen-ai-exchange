import React from 'react';
import { useSearch } from '../context/SearchContext';

interface FilterOptions {
  priceRange: { min: number; max: number };
  rating: number;
  amenities: string[];
  travelDates: { start: string; end: string };
  tripDuration: { min: number; max: number };
}

export const AdvancedFilters: React.FC = () => {
  const { filters, setFilters } = useSearch();

  const amenitiesList = [
    'Wi-Fi',
    'Pool',
    'Spa',
    'Restaurant',
    'Fitness Center',
    'Room Service',
    'Airport Shuttle',
    'Beach Access'
  ];

  const handlePriceChange = (value: [number, number]) => {
    setFilters(prev => ({
      ...prev,
      priceRange: { min: value[0], max: value[1] }
    }));
  };

  const handleRatingChange = (value: number) => {
    setFilters(prev => ({
      ...prev,
      rating: value
    }));
  };

  const handleAmenityToggle = (amenity: string) => {
    setFilters(prev => ({
      ...prev,
      amenities: prev.amenities.includes(amenity)
        ? prev.amenities.filter(a => a !== amenity)
        : [...prev.amenities, amenity]
    }));
  };

  const handleDateChange = (type: 'start' | 'end', value: string) => {
    setFilters(prev => ({
      ...prev,
      travelDates: {
        ...prev.travelDates,
        [type]: value
      }
    }));
  };

  const handleDurationChange = (value: [number, number]) => {
    setFilters(prev => ({
      ...prev,
      tripDuration: { min: value[0], max: value[1] }
    }));
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-4">
      <h3 className="text-lg font-semibold mb-4">Advanced Filters</h3>
      
      {/* Price Range */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">Price Range</label>
        <div className="flex items-center gap-4">
          <input
            type="range"
            min="0"
            max="10000"
            step="100"
            value={filters.priceRange.min}
            onChange={(e) => handlePriceChange([Number(e.target.value), filters.priceRange.max])}
            className="w-full"
          />
          <span className="text-sm text-gray-600">
            ${filters.priceRange.min} - ${filters.priceRange.max}
          </span>
        </div>
      </div>

      {/* Rating */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">Minimum Rating</label>
        <div className="flex gap-2">
          {[1, 2, 3, 4, 5].map((star) => (
            <button
              key={star}
              onClick={() => handleRatingChange(star)}
              className={`p-2 rounded ${
                filters.rating >= star ? 'bg-yellow-400' : 'bg-gray-200'
              }`}
            >
              ★
            </button>
          ))}
        </div>
      </div>

      {/* Amenities */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">Amenities</label>
        <div className="grid grid-cols-2 gap-2">
          {amenitiesList.map((amenity) => (
            <label key={amenity} className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={filters.amenities.includes(amenity)}
                onChange={() => handleAmenityToggle(amenity)}
                className="rounded text-blue-600"
              />
              <span className="text-sm">{amenity}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Travel Dates */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">Travel Dates</label>
        <div className="grid grid-cols-2 gap-4">
          <input
            type="date"
            value={filters.travelDates.start}
            onChange={(e) => handleDateChange('start', e.target.value)}
            className="border rounded p-2"
          />
          <input
            type="date"
            value={filters.travelDates.end}
            onChange={(e) => handleDateChange('end', e.target.value)}
            className="border rounded p-2"
          />
        </div>
      </div>

      {/* Trip Duration */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">
          Trip Duration (days)
        </label>
        <div className="flex items-center gap-4">
          <input
            type="range"
            min="1"
            max="30"
            value={filters.tripDuration.min}
            onChange={(e) => handleDurationChange([Number(e.target.value), filters.tripDuration.max])}
            className="w-full"
          />
          <span className="text-sm text-gray-600">
            {filters.tripDuration.min} - {filters.tripDuration.max} days
          </span>
        </div>
      </div>
    </div>
  );
};

export default AdvancedFilters;
