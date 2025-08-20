from fastapi import FastAPI
from .core.config import settings
from .core.init_db import connect_to_mongo, close_mongo_connection
from .routes import user_routes, email_routes, auth_routes
from .routes import email_routes_new

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

# Add event handlers
@app.on_event("startup")
async def startup_event():
    """Connect to database on startup"""
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    await close_mongo_connection()

# Include routers
app.include_router(auth_routes.router, prefix=settings.API_PREFIX)
app.include_router(user_routes.router, prefix=settings.API_PREFIX)
app.include_router(email_routes.router, prefix=settings.API_PREFIX)
app.include_router(email_routes_new.router, prefix=settings.API_PREFIX)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to the Recruitment Portal API",
        "version": settings.APP_VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment monitoring"""
    return {
        "status": "healthy", 
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }
    
