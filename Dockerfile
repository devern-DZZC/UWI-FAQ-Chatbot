# Step 1: Build the frontend
FROM node:20 AS frontend-build

WORKDIR /frontend
COPY frontend/ ./
RUN npm install
RUN npm run build  # assumes `npm run build` creates the dist folder

# Step 2: Build the backend
FROM python:3.12-slim

# Set workdir
WORKDIR /app
RUN apt-get update && apt-get install -y gcc build-essential && apt-get clean
# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY app/ ./app

# Copy FAISS index files
COPY faiss_store/ ./faiss_store

# Copy built frontend into backend's app directory (e.g., app/static or app/frontend)
COPY --from=frontend-build /frontend/dist ./app/static

# Expose port
EXPOSE 8000

# Start the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
