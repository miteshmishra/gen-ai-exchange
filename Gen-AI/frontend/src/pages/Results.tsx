import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { MapPin, Star, Wifi, Waves, Coffee, SlidersHorizontal } from 'lucide-react';
import { useTelemetry } from '../hooks/useTelemetry';
import { AIImprovementBadge } from '../components/AIImprovementBadge';
import AdvancedFilters from '../components/AdvancedFilters';
import SortResults from '../components/SortResults';
import FavoriteButton from '../components/FavoriteButton';

const Results: React.FC = () => {
  const location = useLocation();
  const { searchData, results } = location.state || {};
  const [loading, setLoading] = useState(true);
  const [aiSuggestions, setAiSuggestions] = useState(null);
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    const loadAISuggestions = async () => {
      try {
        const aiAPI = (await import('../services/api')).aiAPI;
        const response = await aiAPI.getTravelSuggestions({
          destination: searchData?.destination,
          interests: ['sightseeing', 'culture', 'food'],
          budget: searchData?.budgetMax || 1000,
          duration: 3 // default duration
        });
        setAiSuggestions(response.data);
      } catch (error) {
        console.error('AI suggestions error:', error);
      } finally {
        setLoading(false);
      }
    };

    if (searchData?.destination) {
      loadAISuggestions();
    }
  }, [searchData]);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <div className="relative min-h-screen">
      <div className="fixed top-4 left-4 z-50 flex items-center gap-4">
        {/* Filters Toggle Button */}
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="p-3 bg-white rounded-full shadow-lg hover:bg-gray-50"
          title="Toggle Filters"
        >
          <SlidersHorizontal className="h-5 w-5" />
        </button>
        
        {/* Sort Results Component */}
        <SortResults />
      </div>

      {/* Filters Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 transform ${
          showFilters ? 'translate-x-0' : '-translate-x-full'
        } w-80 bg-white shadow-lg transition-transform duration-300 ease-in-out z-40 overflow-y-auto`}
      >
        <div className="p-4">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Filters</h2>
            <button
              onClick={() => setShowFilters(false)}
              className="p-2 hover:bg-gray-100 rounded-full"
            >
              ✕
            </button>
          </div>
          <AdvancedFilters />
        </div>
      </div>

      {/* Main Content */}
      <div className={`min-h-screen transition-all duration-300 ${showFilters ? 'ml-80' : 'ml-0'}`}>
        <div className="container mx-auto px-4 py-8">
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
            </div>
          ) : (
            <motion.div
              variants={containerVariants}
              initial="hidden"
              animate="visible"
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
            >
              {results?.map((result: any, index: number) => (
                <motion.div
                  key={result.id || index}
                  variants={itemVariants}
                  className="bg-white rounded-lg shadow-md overflow-hidden"
                >
                  <div className="relative h-48">
                    <img
                      src={result.image}
                      alt={result.name}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {result.name}
                      </h3>
                      <div className="flex items-center">
                        <Star className="h-4 w-4 text-yellow-400 fill-current" />
                        <span className="ml-1 text-sm text-gray-600">
                          {result.rating}
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center text-gray-600 mb-2">
                      <MapPin className="h-4 w-4 mr-1" />
                      <span className="text-sm">{result.location}</span>
                    </div>

                    <div className="flex flex-wrap gap-2 mb-3">
                      {result.amenities?.map((amenity: string) => (
                        <span
                          key={amenity}
                          className="inline-flex items-center px-2 py-1 text-xs font-medium text-gray-600 bg-gray-100 rounded"
                        >
                          {amenity === 'WiFi' && <Wifi className="h-3 w-3 mr-1" />}
                          {amenity === 'Pool' && <Waves className="h-3 w-3 mr-1" />}
                          {amenity === 'Restaurant' && (
                            <Coffee className="h-3 w-3 mr-1" />
                          )}
                          {amenity}
                        </span>
                      ))}
                    </div>

                    <div className="flex justify-between items-center pt-3">
                      <span className="text-2xl font-bold text-indigo-600">
                        ${result.price}
                        <span className="text-sm font-normal text-gray-600">
                          /night
                        </span>
                      </span>
                      <div className="flex items-center gap-2">
                        <FavoriteButton
                          itemType="hotel"
                          itemId={result.id}
                          itemData={result}
                        />
                        <button className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded hover:bg-indigo-700 transition-colors">
                          View Details
                        </button>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Results;
