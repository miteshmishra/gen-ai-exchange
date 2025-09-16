import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';
import { toast } from 'react-hot-toast';

interface Favorite {
  id: number;
  item_type: string;
  item_id: string;
  item_data: any;
  created_at: string;
}

interface FavoritesContextType {
  favorites: Favorite[];
  isLoading: boolean;
  addFavorite: (itemType: string, itemId: string, itemData: any) => Promise<void>;
  removeFavorite: (itemType: string, itemId: string) => Promise<void>;
  isFavorite: (itemType: string, itemId: string) => boolean;
  getFavoritesByType: (itemType: string) => Favorite[];
}

const FavoritesContext = createContext<FavoritesContextType | undefined>(undefined);

export const FavoritesProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [favorites, setFavorites] = useState<Favorite[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { isAuthenticated, token } = useAuth();

  const fetchFavorites = async () => {
    if (!isAuthenticated || !token) {
      setFavorites([]);
      setIsLoading(false);
      return;
    }

    try {
      const response = await axios.get('http://localhost:8000/api/favorites', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setFavorites(response.data.favorites);
    } catch (error) {
      console.error('Error fetching favorites:', error);
      toast.error('Failed to load favorites');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchFavorites();
  }, [isAuthenticated, token]);

  const addFavorite = async (itemType: string, itemId: string, itemData: any) => {
    if (!isAuthenticated) {
      toast.error('Please log in to add favorites');
      return;
    }

    try {
      await axios.post(
        `http://localhost:8000/api/favorites/${itemType}/${itemId}`,
        { item_data: itemData },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      toast.success('Added to favorites');
      fetchFavorites();
    } catch (error: any) {
      console.error('Error adding favorite:', error);
      toast.error(error.response?.data?.detail || 'Failed to add to favorites');
    }
  };

  const removeFavorite = async (itemType: string, itemId: string) => {
    if (!isAuthenticated) return;

    try {
      await axios.delete(
        `http://localhost:8000/api/favorites/${itemType}/${itemId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      toast.success('Removed from favorites');
      setFavorites(favorites.filter(
        f => !(f.item_type === itemType && f.item_id === itemId)
      ));
    } catch (error) {
      console.error('Error removing favorite:', error);
      toast.error('Failed to remove from favorites');
    }
  };

  const isFavorite = (itemType: string, itemId: string): boolean => {
    return favorites.some(
      f => f.item_type === itemType && f.item_id === itemId
    );
  };

  const getFavoritesByType = (itemType: string): Favorite[] => {
    return favorites.filter(f => f.item_type === itemType);
  };

  return (
    <FavoritesContext.Provider
      value={{
        favorites,
        isLoading,
        addFavorite,
        removeFavorite,
        isFavorite,
        getFavoritesByType,
      }}
    >
      {children}
    </FavoritesContext.Provider>
  );
};

export const useFavorites = () => {
  const context = useContext(FavoritesContext);
  if (context === undefined) {
    throw new Error('useFavorites must be used within a FavoritesProvider');
  }
  return context;
};
