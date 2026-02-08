#!/bin/bash
# Rebuild Docker images for Minikube

set -e

echo "Rebuilding Docker images..."
eval $(minikube docker-env)

echo "Building backend..."
docker build -t todo-backend:local ./backend

echo "Building frontend..."
docker build -t todo-frontend:local ./Frontend

echo ""
echo "✓ Images rebuilt"
echo ""
echo "To deploy changes:"
echo "  kubectl rollout restart deployment -n todo-chatbot"
echo ""
