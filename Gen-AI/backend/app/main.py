from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, search, analytics, ai, favorites, preferences
from .core.config import settings
from .db.session import init_db

# Initialize the database
init_db()

app = FastAPI(
    title="Travel Hub API",
    description="""
    Travel Hub API provides a comprehensive backend for the travel planning application.
    Features include:
    * 🔐 User Authentication and Authorization
    * 🔍 Travel Search and Recommendations
    * 📊 Analytics and User Insights
    * 🤖 AI-Powered Features
    * ⭐ User Favorites Management
    * ⚙️ User Preferences
    """,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

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
