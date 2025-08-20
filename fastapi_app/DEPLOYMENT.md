# Recruitment Portal Backend - Deployment Guide

## Quick Deploy to Render

### Option 1: Using render.yaml (Recommended)
1. Push your code to GitHub
2. Connect your GitHub repository to Render
3. Render will automatically detect the `render.yaml` file and deploy
4. Set these environment variables in Render dashboard:
   - `MONGODB_URL`: Your MongoDB connection string
   - `SECRET_KEY`: A secure secret key for JWT tokens

### Option 2: Manual Render Setup
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the following:
   - **Environment**: Docker
   - **Dockerfile Path**: `./Dockerfile`
   - **Docker Context**: `.`
   - **Build Command**: (leave empty - Docker will handle it)
   - **Start Command**: (leave empty - Docker will handle it)

### Environment Variables Required on Render:
```
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/database
SECRET_KEY=your-super-secret-key-here
ENVIRONMENT=production
PORT=8000 (Render sets this automatically)
```

## Local Development

### Using Docker Compose
```bash
# Clone the repository
git clone <your-repo-url>
cd fastapi_app

# Start the application with MongoDB
docker-compose up --build

# The API will be available at http://localhost:8000
```

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables or create .env file
export MONGODB_URL="your-mongodb-connection-string"
export SECRET_KEY="your-secret-key"

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Testing the Deployment

Once deployed, test these endpoints:
- `GET /` - Health check
- `GET /api/users` - List users
- `GET /api/emails` - List emails

## Production Notes

1. **Security**: Make sure to set a strong `SECRET_KEY` in production
2. **Database**: Use MongoDB Atlas or another hosted MongoDB service
3. **Monitoring**: Consider adding logging and monitoring services
4. **Scaling**: Render can auto-scale based on traffic

## Troubleshooting

- Check Render logs if deployment fails
- Ensure all environment variables are set correctly
- Verify MongoDB connection string is accessible from Render's servers
- Check that all required dependencies are in requirements.txt
