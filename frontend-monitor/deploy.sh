#!/bin/bash

echo "🚀 Starting Nuxt build..."
pnpm install
pnpm  build

if [ $? -ne 0 ]; then
  echo "❌ Build failed!"
  exit 1
fi

echo "✅ Build successful. Deploying to /var/www/html/monitor..."
sudo rm -rf /var/www/html/monitor/*
sudo cp -r .output/public/* /var/www/html/monitor/

echo "🎉 Nuxt frontend deployed successfully!"
