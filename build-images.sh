#!/bin/bash
# Build Docker images using Minikube's Docker daemon

set -e

echo "Setting up Docker to use Minikube..."
eval $(minikube -p minikube docker-env)

echo "Building backend image..."
docker build -t todo-backend:local ./backend

echo "Building frontend image..."
docker build -t todo-frontend:local ./Frontend

echo "✓ All images built successfully!"
docker images | grep todo-
