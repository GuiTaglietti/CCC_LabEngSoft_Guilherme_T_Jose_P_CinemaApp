# Build
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile
COPY . .
# Se o frontend consome a API, exporte a URL durante o build (ou use .env do Vite):
# ENV VITE_API_BASE_URL=http://localhost:5055
RUN yarn build

# Runtime
FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
# SPA fallback opcional:
# RUN printf 'server { listen 80; server_name _; root /usr/share/nginx/html; location / { try_files $uri /index.html; } }' > /etc/nginx/conf.d/default.conf
EXPOSE 80
