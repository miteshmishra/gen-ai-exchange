import React from 'react';
import { motion } from 'framer-motion';
import { User, Mail, Settings } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import UserPreferencesForm from '../components/UserPreferencesForm';

const Profile: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="max-w-7xl mx-auto space-y-8 px-4 sm:px-6 lg:px-8">
      {/* Profile Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white rounded-xl shadow-md overflow-hidden"
      >
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-8 py-12">
          <div className="flex items-center space-x-4">
            <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center">
              <User className="w-12 h-12 text-indigo-600" />
            </div>
            <div className="text-white">
              <h1 className="text-3xl font-bold">{user?.full_name}</h1>
              <div className="flex items-center mt-2">
                <Mail className="w-4 h-4 mr-2" />
                <span>{user?.email}</span>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Preferences Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white rounded-xl shadow-md overflow-hidden"
      >
        <div className="p-8">
          <div className="flex items-center mb-6">
            <Settings className="w-6 h-6 text-indigo-600 mr-3" />
            <h2 className="text-2xl font-semibold text-gray-900">Travel Preferences</h2>
          </div>
          <UserPreferencesForm />
        </div>
      </motion.div>
    </div>
  );
};

export default Profile;
