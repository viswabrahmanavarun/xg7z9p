#!/usr/bin/env bash
set -euo pipefail

# ---------- Backend ---------- #
echo "🔧 Building backend Docker image..."
docker build -t registry.heroku.com/${HEROKU_APP_NAME}/web ./backend

echo "🔐 Logging in to Heroku Container Registry..."
echo "${HEROKU_API_KEY}" | docker login --username=_ --password-stdin registry.heroku.com

echo "🚀 Pushing backend image to Heroku..."
docker push registry.heroku.com/${HEROKU_APP_NAME}/web

echo "📦 Releasing backend on Heroku..."
heroku container:release web --app "${HEROKU_APP_NAME}"

# ---------- Frontend ---------- #
echo "🔧 Installing Vercel CLI..."
npm i -g vercel

echo "🚀 Deploying frontend to Vercel..."
vercel --prod --confirm \
  --token "${VERCEL_TOKEN}" \
  --org "${VERCEL_ORG_ID}" \
  --project "${VERCEL_PROJECT_ID}"
