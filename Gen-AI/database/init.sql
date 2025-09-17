-- Create database schema
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS search_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    search_type VARCHAR(50),
    query JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    item_type VARCHAR(50),
    item_id VARCHAR(255),
    item_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    travel_style VARCHAR(100),
    preferred_activities VARCHAR(255)[],
    room_type VARCHAR(50),
    max_price_per_night NUMERIC(10, 2),
    preferred_amenities VARCHAR(255)[],
    seat_preference VARCHAR(50),
    cabin_class VARCHAR(50),
    email_notifications BOOLEAN DEFAULT true,
    price_alerts BOOLEAN DEFAULT true,
    deal_notifications BOOLEAN DEFAULT true,
    preferred_currency VARCHAR(10) DEFAULT 'USD',
    preferred_language VARCHAR(10) DEFAULT 'en',
    accessibility_needs VARCHAR(255)[]
);

-- Insert sample users
INSERT INTO users (email, full_name, hashed_password) VALUES
('john.doe@example.com', 'John Doe', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'), -- password: password123
('jane.smith@example.com', 'Jane Smith', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'), -- password: password123
('mike.wilson@example.com', 'Mike Wilson', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'); -- password: password123

-- Insert sample user preferences
INSERT INTO user_preferences (user_id, travel_style, preferred_activities, room_type, max_price_per_night, preferred_amenities, seat_preference, cabin_class) VALUES
(1, 'luxury', ARRAY['beach', 'cultural_events', 'fine_dining'], 'suite', 300.00, ARRAY['wifi', 'pool', 'spa'], 'window', 'business'),
(2, 'budget', ARRAY['hiking', 'local_cuisine', 'shopping'], 'double', 100.00, ARRAY['wifi', 'breakfast'], 'aisle', 'economy'),
(3, 'adventure', ARRAY['hiking', 'water_sports', 'wildlife'], 'single', 150.00, ARRAY['wifi', 'gym'], 'no_preference', 'economy');

-- Insert sample search history
INSERT INTO search_history (user_id, search_type, query) VALUES
(1, 'hotel', '{"destination": "Paris", "checkIn": "2024-03-15", "checkOut": "2024-03-20", "guests": 2}'),
(1, 'flight', '{"origin": "NYC", "destination": "CDG", "departureDate": "2024-03-15", "returnDate": "2024-03-20", "passengers": 2}'),
(2, 'hotel', '{"destination": "Bali", "checkIn": "2024-04-01", "checkOut": "2024-04-10", "guests": 1}'),
(3, 'experience', '{"destination": "Costa Rica", "activities": ["ziplining", "wildlife_tours"], "date": "2024-05-01"}');

-- Insert sample favorites
INSERT INTO favorites (user_id, item_type, item_id, item_data) VALUES
(1, 'hotel', 'paris-luxury-123', '{"name": "Luxury Paris Hotel", "rating": 4.8, "price": 250, "location": "Paris City Center"}'),
(1, 'flight', 'nyc-cdg-456', '{"airline": "Air France", "price": 650, "duration": "7h 30m", "departure": "JFK", "arrival": "CDG"}'),
(2, 'hotel', 'bali-budget-789', '{"name": "Bali Beach Resort", "rating": 4.2, "price": 80, "location": "Kuta Beach"}'),
(3, 'experience', 'costa-rica-zipline', '{"name": "Rainforest Zipline Adventure", "price": 75, "duration": "4 hours", "rating": 4.9}');

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_search_history_user_id ON search_history(user_id);
CREATE INDEX idx_favorites_user_id ON favorites(user_id);
CREATE INDEX idx_favorites_item_type ON favorites(item_type);
CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);