import React from 'react';
import { motion } from 'framer-motion';

interface AIImprovementBadgeProps {
  changeId: string;
  featureKey: string;
  timestamp: string;
  onRevert: () => void;
  onFeedback: (helpful: boolean) => void;
}

export const AIImprovementBadge: React.FC<AIImprovementBadgeProps> = ({
  changeId,
  featureKey,
  timestamp,
  onRevert,
  onFeedback,
}) => {
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <div className="relative inline-block">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-blue-50 border border-blue-200 rounded-md p-2 cursor-pointer"
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="flex items-center space-x-2">
          <svg
            className="w-4 h-4 text-blue-500"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 10V3L4 14h7v7l9-11h-7z"
            />
          </svg>
          <span className="text-sm text-blue-700">AI improved this section!</span>
        </div>
      </motion.div>

      {isOpen && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="absolute z-10 mt-2 w-72 bg-white rounded-lg shadow-lg border border-gray-200 p-4"
        >
          <h3 className="font-medium text-gray-900">AI Improvement Details</h3>
          <p className="text-sm text-gray-600 mt-1">
            This {featureKey} was improved by our AI assistant on{' '}
            {new Date(timestamp).toLocaleDateString()}
          </p>
          
          <div className="mt-3 space-y-2">
            <p className="text-sm text-gray-700">Was this improvement helpful?</p>
            <div className="flex space-x-2">
              <button
                onClick={() => onFeedback(true)}
                className="px-3 py-1 text-sm bg-green-50 text-green-700 rounded-md hover:bg-green-100"
              >
                Yes
              </button>
              <button
                onClick={() => onFeedback(false)}
                className="px-3 py-1 text-sm bg-red-50 text-red-700 rounded-md hover:bg-red-100"
              >
                No
              </button>
            </div>
          </div>

          <div className="mt-3 pt-3 border-t border-gray-200">
            <button
              onClick={onRevert}
              className="text-sm text-gray-600 hover:text-gray-900 flex items-center"
            >
              <svg
                className="w-4 h-4 mr-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6"
                />
              </svg>
              Revert this change
            </button>
          </div>
        </motion.div>
      )}
    </div>
  );
};
