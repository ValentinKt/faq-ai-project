# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Install dependencies (production only)
COPY package.json package-lock.json ./
RUN npm ci --production

# Copy and build app
COPY . .
RUN npm run build

# Production stage
FROM nginx:1.25-alpine

# Copy build output
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 80