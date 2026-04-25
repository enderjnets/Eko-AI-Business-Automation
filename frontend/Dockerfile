FROM node:20-alpine

WORKDIR /app

# Accept API URL at build time (required for NEXT_PUBLIC_* env vars)
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source
COPY . .

# Build
RUN npm run build

# Start
EXPOSE 3000
CMD ["npm", "start"]
