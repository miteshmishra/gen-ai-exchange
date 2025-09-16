import React from 'react';
import { usePreferences } from '../context/PreferencesContext';
import { motion } from 'framer-motion';
import { toast } from 'react-hot-toast';
import { Globe, Hotel, Plane, Bell, CreditCard, Languages } from 'lucide-react';

interface PreferencesSectionProps {
  title: string;
  icon: React.ReactNode;
  children: React.ReactNode;
}

const PreferencesSection: React.FC<PreferencesSectionProps> = ({
  title,
  icon,
  children
}) => (
  <div className="bg-white rounded-lg shadow p-6 mb-6">
    <div className="flex items-center mb-4">
      <div className="p-2 bg-indigo-100 rounded-lg mr-3">
        {icon}
      </div>
      <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
    </div>
    {children}
  </div>
);

const UserPreferencesForm = () => {
  const { preferences, options, isLoading, updatePreferences } = usePreferences();

  if (isLoading || !preferences || !options) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  const handleInputChange = async (
    field: keyof typeof preferences,
    value: any
  ) => {
    try {
      await updatePreferences({ [field]: value });
    } catch (error) {
      toast.error('Failed to update preference');
    }
  };

  const handleMultiSelectChange = (
    field: keyof typeof preferences,
    value: string
  ) => {
    const currentValues = preferences[field] as string[];
    const newValues = currentValues.includes(value)
      ? currentValues.filter(v => v !== value)
      : [...currentValues, value];
    handleInputChange(field, newValues);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-4xl mx-auto py-8 px-4"
    >
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Travel Preferences</h1>

      <PreferencesSection title="Travel Style" icon={<Globe className="w-5 h-5 text-indigo-600" />}>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Preferred Travel Style
            </label>
            <select
              value={preferences.travel_style || ''}
              onChange={(e) => handleInputChange('travel_style', e.target.value)}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            >
              <option value="">Select a style</option>
              {options.travel_styles.map((style) => (
                <option key={style} value={style}>
                  {style.charAt(0).toUpperCase() + style.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Preferred Activities
            </label>
            <div className="grid grid-cols-2 gap-2">
              {options.activities.map((activity) => (
                <label key={activity} className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={preferences.preferred_activities.includes(activity)}
                    onChange={() => handleMultiSelectChange('preferred_activities', activity)}
                    className="rounded text-indigo-600 focus:ring-indigo-500"
                  />
                  <span className="text-sm text-gray-700">
                    {activity.split('_').map(word => 
                      word.charAt(0).toUpperCase() + word.slice(1)
                    ).join(' ')}
                  </span>
                </label>
              ))}
            </div>
          </div>
        </div>
      </PreferencesSection>

      <PreferencesSection title="Accommodation" icon={<Hotel className="w-5 h-5 text-indigo-600" />}>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Room Type
            </label>
            <select
              value={preferences.room_type || ''}
              onChange={(e) => handleInputChange('room_type', e.target.value)}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            >
              <option value="">Select room type</option>
              {options.room_types.map((type) => (
                <option key={type} value={type}>
                  {type.charAt(0).toUpperCase() + type.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Maximum Price per Night
            </label>
            <input
              type="number"
              value={preferences.max_price_per_night || ''}
              onChange={(e) => handleInputChange('max_price_per_night', Number(e.target.value))}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Must-have Amenities
            </label>
            <div className="grid grid-cols-2 gap-2">
              {options.amenities.map((amenity) => (
                <label key={amenity} className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={preferences.preferred_amenities.includes(amenity)}
                    onChange={() => handleMultiSelectChange('preferred_amenities', amenity)}
                    className="rounded text-indigo-600 focus:ring-indigo-500"
                  />
                  <span className="text-sm text-gray-700">
                    {amenity.split('_').map(word => 
                      word.charAt(0).toUpperCase() + word.slice(1)
                    ).join(' ')}
                  </span>
                </label>
              ))}
            </div>
          </div>
        </div>
      </PreferencesSection>

      <PreferencesSection title="Flight" icon={<Plane className="w-5 h-5 text-indigo-600" />}>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Seat Preference
            </label>
            <select
              value={preferences.seat_preference || ''}
              onChange={(e) => handleInputChange('seat_preference', e.target.value)}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            >
              <option value="">Select seat preference</option>
              {options.seat_preferences.map((pref) => (
                <option key={pref} value={pref}>
                  {pref.split('_').map(word => 
                    word.charAt(0).toUpperCase() + word.slice(1)
                  ).join(' ')}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Cabin Class
            </label>
            <select
              value={preferences.cabin_class || ''}
              onChange={(e) => handleInputChange('cabin_class', e.target.value)}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            >
              <option value="">Select cabin class</option>
              {options.cabin_classes.map((cabin) => (
                <option key={cabin} value={cabin}>
                  {cabin.split('_').map(word => 
                    word.charAt(0).toUpperCase() + word.slice(1)
                  ).join(' ')}
                </option>
              ))}
            </select>
          </div>
        </div>
      </PreferencesSection>

      <PreferencesSection title="Notifications" icon={<Bell className="w-5 h-5 text-indigo-600" />}>
        <div className="space-y-4">
          {[
            { key: 'email_notifications', label: 'Email Notifications' },
            { key: 'price_alerts', label: 'Price Alerts' },
            { key: 'deal_notifications', label: 'Deal Notifications' }
          ].map(({ key, label }) => (
            <label key={key} className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={preferences[key as keyof typeof preferences] as boolean}
                onChange={(e) => handleInputChange(key as keyof typeof preferences, e.target.checked)}
                className="rounded text-indigo-600 focus:ring-indigo-500"
              />
              <span className="text-sm text-gray-700">{label}</span>
            </label>
          ))}
        </div>
      </PreferencesSection>

      <PreferencesSection title="Regional" icon={<Globe className="w-5 h-5 text-indigo-600" />}>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Preferred Currency
            </label>
            <select
              value={preferences.preferred_currency}
              onChange={(e) => handleInputChange('preferred_currency', e.target.value)}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            >
              {options.currencies.map((currency) => (
                <option key={currency} value={currency}>
                  {currency}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Preferred Language
            </label>
            <select
              value={preferences.preferred_language}
              onChange={(e) => handleInputChange('preferred_language', e.target.value)}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            >
              {options.languages.map((lang) => (
                <option key={lang} value={lang}>
                  {lang.toUpperCase()}
                </option>
              ))}
            </select>
          </div>
        </div>
      </PreferencesSection>

      <PreferencesSection title="Accessibility" icon={<Languages className="w-5 h-5 text-indigo-600" />}>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Accessibility Requirements
          </label>
          <div className="grid grid-cols-2 gap-2">
            {options.accessibility_options.map((option) => (
              <label key={option} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={preferences.accessibility_needs.includes(option)}
                  onChange={() => handleMultiSelectChange('accessibility_needs', option)}
                  className="rounded text-indigo-600 focus:ring-indigo-500"
                />
                <span className="text-sm text-gray-700">
                  {option.split('_').map(word => 
                    word.charAt(0).toUpperCase() + word.slice(1)
                  ).join(' ')}
                </span>
              </label>
            ))}
          </div>
        </div>
      </PreferencesSection>
    </motion.div>
  );
};

export default UserPreferencesForm;
