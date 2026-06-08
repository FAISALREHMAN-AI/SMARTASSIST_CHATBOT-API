# Using Debian-slim instead of alpine to completely bypass musl-libc native binding issues with Rolldown/Vite
FROM node:22-slim

# Container workspace setup
WORKDIR /app

# Dependencies configuration files copy
COPY package*.json ./

# Clean npm cache and install fresh packages
RUN npm cache clean --force && npm install

# Saara source code inject karenge
COPY . .

# Port expose (Vite)
EXPOSE 5173

# Frontend development server command with container mapping host
CMD ["npm", "run", "dev", "--", "--host"]