import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { LogIn, LogOut, User, Home, Search, BarChart } from 'lucide-react';

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const isAuthenticated = false; // Replace with actual auth state

  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="flex items-center cursor-pointer"
            onClick={() => navigate('/')}
          >
            <span className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 text-transparent bg-clip-text">
              Travel Hub
            </span>
          </motion.div>

          <div className="flex items-center space-x-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              className="p-2 text-gray-600 hover:text-indigo-600"
              onClick={() => navigate('/')}
            >
              <Home className="h-5 w-5" />
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.05 }}
              className="p-2 text-gray-600 hover:text-indigo-600"
              onClick={() => navigate('/results')}
            >
              <Search className="h-5 w-5" />
            </motion.button>

            {isAuthenticated && (
              <>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  className="p-2 text-gray-600 hover:text-indigo-600"
                  onClick={() => navigate('/analytics')}
                >
                  <BarChart className="h-5 w-5" />
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  className="p-2 text-gray-600 hover:text-indigo-600"
                  onClick={() => navigate('/profile')}
                >
                  <User className="h-5 w-5" />
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  className="flex items-center px-4 py-2 text-sm font-medium text-white bg-red-500 rounded-lg hover:bg-red-600"
                >
                  <LogOut className="h-4 w-4 mr-2" />
                  Logout
                </motion.button>
              </>
            )}

            {!isAuthenticated && (
              <motion.button
                whileHover={{ scale: 1.05 }}
                className="flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700"
                onClick={() => navigate('/login')}
              >
                <LogIn className="h-4 w-4 mr-2" />
                Login
              </motion.button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
