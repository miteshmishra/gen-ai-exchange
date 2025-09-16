import React from 'react';
import SearchForm from '../components/SearchForm';
import { motion } from 'framer-motion';

const Home: React.FC = () => {
  return (
    <div className="space-y-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-4"
      >
        <h1 className="text-5xl font-bold text-gray-800">
          Discover Your Next Adventure
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Find and book flights, hotels, and unique experiences worldwide. Let us help you create unforgettable memories.
        </p>
      </motion.div>

      <SearchForm />

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12"
      >
        {[
          {
            title: 'AI-Powered Recommendations',
            description: 'Get personalized travel suggestions based on your preferences and past experiences.',
            icon: '🤖',
          },
          {
            title: 'Real-Time Updates',
            description: 'Stay informed with instant notifications about price changes and availability.',
            icon: '⚡',
          },
          {
            title: 'Best Price Guarantee',
            description: 'Find the best deals with our price comparison and monitoring system.',
            icon: '💰',
          },
        ].map((feature, index) => (
          <motion.div
            key={index}
            whileHover={{ scale: 1.05 }}
            className="bg-white p-6 rounded-xl shadow-md"
          >
            <div className="text-4xl mb-4">{feature.icon}</div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              {feature.title}
            </h3>
            <p className="text-gray-600">{feature.description}</p>
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
};

export default Home;
