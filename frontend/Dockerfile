# Use Node.js as the base image
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json into the working directory
COPY frontend/package.json frontend/package-lock.json ./

# Install npm dependencies
RUN npm install

# Copy the rest of the frontend application code
COPY frontend/ ./

# Build the Vite project for production
RUN npm run build

# Expose port 3000 for Vite's development server
EXPOSE 5173

# Command to run the Vite development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
