from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, search, analytics, ai, favorites, preferences
from .core.config import settings
from .db.session import init_db

app = FastAPI(title="Travel Hub API")

# Initialize database
init_db()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI Features"])
app.include_router(favorites.router, prefix="/api/favorites", tags=["Favorites"])
app.include_router(preferences.router, prefix="/api/preferences", tags=["Preferences"])

@app.get("/")
async def root():
    return {"message": "Welcome to Travel Hub API"}
