FROM node:24-alpine

WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install dependencies inside the Linux container
RUN npm ci

# Copy application source
COPY . .

EXPOSE 5173

# Run Vite directly through Node.
# This avoids the generated .bin/vite shell wrapper.
CMD ["node", "node_modules/vite/bin/vite.js", "--host", "0.0.0.0"]
