import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { Search, MapPin, Calendar, Users, DollarSign } from 'lucide-react';
import { toast } from 'react-hot-toast';
import { useTelemetry } from '../hooks/useTelemetry';
import { AIImprovementBadge } from './AIImprovementBadge';


interface SearchFormData {
  type: 'flight' | 'hotel' | 'train' | 'experience';
  origin: string;
  destination: string;
  dateFrom: string;
  dateTo?: string;
  passengers: number;
  budgetMin?: number;
  budgetMax?: number;
}

const SearchForm: React.FC = () => {
  const navigate = useNavigate();
  const { register, handleSubmit, watch, formState: { errors } } = useForm<SearchFormData>({
    defaultValues: {
      type: 'flight',
      passengers: 1,
    },
  });
  const searchType = watch('type');
  
  // Telemetry tracking
  const { trackEvent, startTask, completeTask, trackClick } = useTelemetry({
    component: 'SearchForm',
    taskId: 'search',
  });
  
  // A/B testing variant
  const [activeExperiment, setActiveExperiment] = useState<{
    id: string;
    featureKey: string;
    variant: any;
  } | null>(null);
  
  // AI improvements
  const [aiImprovement, setAiImprovement] = useState<{
    changeId: string;
    featureKey: string;
    timestamp: string;
  } | null>(null);
  
  // Load A/B test variant and AI improvements (currently disabled)
  useEffect(() => {
    // These features are not yet implemented in the backend
    console.log('A/B testing and AI improvements are not yet implemented');
  }, []);

  const onSubmit = async (data: SearchFormData) => {
    if (!data.origin || !data.destination) {
      toast.error('Please enter both origin and destination');
      trackEvent('validation_error', { error: 'missing_fields' });
      return;
    }
    
    // Start tracking the search task
    startTask();
    
    try {
      let searchResult;
      const searchAPI = (await import('../services/api')).searchAPI;
      
      // Track search parameters
      trackEvent('search_initiated', {
        type: data.type,
        experimentId: activeExperiment?.id,
        variantId: activeExperiment?.variant?.id,
      });
      
      switch (data.type) {
        case 'hotel':
          searchResult = await searchAPI.searchHotels(data);
          break;
        case 'flight':
          searchResult = await searchAPI.searchFlights(data);
          break;
        case 'experience':
          searchResult = await searchAPI.searchExperiences(data);
          break;
        default:
          trackEvent('error', { type: 'invalid_search_type' });
          throw new Error('Invalid search type');
      }
      
      navigate('/results', { 
        state: { 
          searchData: data, 
          results: searchResult.data 
        } 
      });
    } catch (error) {
      console.error('Search error:', error);
      toast.error('Failed to fetch search results. Please try again.');
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-4xl mx-auto bg-white rounded-2xl shadow-xl p-8"
    >
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">
          Find Your Perfect Trip
        </h1>
        <p className="text-gray-600">Search flights, hotels, and experiences all in one place</p>
      </div>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Search Type Tabs */}
        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
          {(['flight', 'hotel', 'train', 'experience'] as const).map(type => (
            <label key={type} className="flex-1">
              <input
                type="radio"
                value={type}
                {...register('type')}
                className="sr-only"
              />
              <div
                className={`text-center py-3 px-4 rounded-md cursor-pointer transition-all ${watch('type') === type ? 'bg-white text-indigo-600 shadow-sm font-semibold' : 'text-gray-600 hover:text-gray-800'}`}
              >
                {type.charAt(0).toUpperCase() + type.slice(1)}
              </div>
            </label>
          ))}
        </div>
        {/* Location Fields */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="relative">
            <MapPin className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder={searchType === 'hotel' ? 'City or hotel name' : 'From where?'}
              {...register('origin', { required: 'Origin is required' })}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-50"
            />
            {errors.origin && (
              <p className="text-red-500 text-sm mt-1">{errors.origin.message}</p>
            )}
          </div>
          <div className="relative">
            <MapPin className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder={searchType === 'hotel' ? 'Check-in location' : 'To where?'}
              {...register('destination', { required: 'Destination is required' })}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-50"
            />
            {errors.destination && (
              <p className="text-red-500 text-sm mt-1">{errors.destination.message}</p>
            )}
          </div>
        </div>
        {/* Date and Passengers */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="relative">
            <Calendar className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
            <input
              type="date"
              {...register('dateFrom', { required: 'Departure date is required' })}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-50"
            />
            {errors.dateFrom && (
              <p className="text-red-500 text-sm mt-1">{errors.dateFrom.message}</p>
            )}
          </div>
          {searchType === 'hotel' && (
            <div className="relative">
              <Calendar className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
              <input
                type="date"
                placeholder="Check-out"
                {...register('dateTo')}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-50"
              />
            </div>
          )}
          <div className="relative">
            <Users className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
            <select
              {...register('passengers')}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-50"
            >
              {[1,2,3,4,5,6,7,8].map(num => (
                <option key={num} value={num}>{num} {num === 1 ? 'Passenger' : 'Passengers'}</option>
              ))}
            </select>
          </div>
        </div>
        {/* Budget Range */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="relative">
            <DollarSign className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
            <input
              type="number"
              placeholder="Min budget"
              {...register('budgetMin')}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-50"
            />
          </div>
          <div className="relative">
            <DollarSign className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
            <input
              type="number"
              placeholder="Max budget"
              {...register('budgetMax')}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-50"
            />
          </div>
        </div>
        <motion.button
          type="submit"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold py-4 px-8 rounded-lg flex items-center justify-center gap-2"
        >
          <Search className="h-5 w-5" />
          <span>Search {searchType}s</span>
        </motion.button>
      </form>
    </motion.div>
  );
};

export default SearchForm;
