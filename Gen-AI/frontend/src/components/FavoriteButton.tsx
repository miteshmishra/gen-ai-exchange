import React from 'react';
import { Heart } from 'lucide-react';
import { useFavorites } from '../context/FavoritesContext';
import { useAuth } from '../context/AuthContext';
import { toast } from 'react-hot-toast';

interface FavoriteButtonProps {
  itemType: string;
  itemId: string;
  itemData: any;
  className?: string;
}

const FavoriteButton: React.FC<FavoriteButtonProps> = ({
  itemType,
  itemId,
  itemData,
  className = ''
}) => {
  const { isAuthenticated } = useAuth();
  const { isFavorite, addFavorite, removeFavorite } = useFavorites();
  const isFav = isFavorite(itemType, itemId);

  const handleClick = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    if (!isAuthenticated) {
      toast.error('Please log in to save favorites');
      return;
    }

    try {
      if (isFav) {
        await removeFavorite(itemType, itemId);
      } else {
        await addFavorite(itemType, itemId, itemData);
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

  return (
    <button
      onClick={handleClick}
      className={`
        p-2 rounded-full transition-all duration-200
        ${isFav 
          ? 'bg-red-100 text-red-500 hover:bg-red-200' 
          : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
        }
        ${className}
      `}
      title={isFav ? 'Remove from favorites' : 'Add to favorites'}
    >
      <Heart
        className={`w-5 h-5 ${isFav ? 'fill-current' : ''}`}
      />
    </button>
  );
};

export default FavoriteButton;
