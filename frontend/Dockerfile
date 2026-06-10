FROM node:22-slim
WORKDIR /app
COPY package*.json ./
# Native dependencies ke liye build-essential zaroori hai
RUN apt-get update && apt-get install -y build-essential
RUN npm install
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]