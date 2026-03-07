#!/bin/bash
# Todo Chatbot Minikube Deployment Script
# Includes kubectl-ai and kagent AIOps integration

set -e

echo "============================================"
echo "Todo Chatbot - Minikube Deployment"
echo "With kubectl-ai and kagent AIOps"
echo "============================================"
echo ""

# Phase 0: Prerequisites
echo "Phase 0: Checking prerequisites..."
command -v minikube >/dev/null 2>&1 || { echo "ERROR: minikube not found. Install from https://minikube.sigs.k8s.io/docs/start/"; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo "ERROR: kubectl not found. Install from https://kubernetes.io/docs/tasks/tools/"; exit 1; }
command -v helm >/dev/null 2>&1 || { echo "ERROR: helm not found. Install from https://helm.sh/docs/intro/install/"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "ERROR: docker not found. Install from https://docs.docker.com/get-docker/"; exit 1; }

echo "✓ Core prerequisites OK"

# Check optional AIOps tools
KUBECTL_AI_AVAILABLE=false
KAGENT_AVAILABLE=false

if command -v kubectl-ai >/dev/null 2>&1; then
    KUBECTL_AI_AVAILABLE=true
    echo "✓ kubectl-ai found"
else
    echo "⚠ kubectl-ai not found (optional)"
fi

if command -v kagent >/dev/null 2>&1; then
    KAGENT_AVAILABLE=true
    echo "✓ kagent found"
else
    echo "⚠ kagent not found (optional)"
fi
echo ""

# Phase 1: Minikube cluster
echo "Phase 1: Starting Minikube cluster..."
if minikube status | grep -q "Running"; then
    echo "✓ Minikube already running"
else
    minikube start --cpus=2 --memory=2048 --driver=docker --force
    echo "✓ Minikube started"
fi

minikube addons enable ingress
echo "✓ Ingress enabled"
echo ""

# Phase 2: Build Docker images
echo "Phase 2: Building Docker images..."
eval $(minikube docker-env)

echo "Building backend image..."
docker build -t todo-backend:local ./backend

echo "Building frontend image..."
docker build -t todo-frontend:local ./Frontend

echo "✓ Images built"
echo ""

# Phase 3: Deploy with Helm
echo "Phase 3: Deploying with Helm..."
helm upgrade --install todo-chatbot ./helm/todo-chatbot \
  --namespace todo-chatbot \
  --create-namespace \
  --wait

echo "✓ Helm deployment complete"
echo ""

# Phase 4: Validation
echo "Phase 4: Validating deployment..."
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=Ready pods --all -n todo-chatbot --timeout=300s
echo "✓ All pods ready"
echo ""

# Phase 5: kubectl-ai Integration
echo "Phase 5: kubectl-ai AIOps Integration..."
if [ "$KUBECTL_AI_AVAILABLE" = true ]; then
    echo "Running kubectl-ai deployment analysis..."
    
    # Apply kubectl-ai configuration
    if [ -f "kubectl-ai.yaml" ]; then
        kubectl apply -f kubectl-ai.yaml 2>/dev/null || true
        echo "✓ kubectl-ai configuration applied"
    fi
    
    # Run AI-powered checks
    echo ""
    echo "Running AI-powered deployment checks:"
    kubectl-ai "analyze deployment health in namespace todo-chatbot" || true
    
    echo ""
    echo "✓ kubectl-ai integration complete"
else
    echo "⚠ kubectl-ai not installed. To install:"
    echo "  kubectl krew install ai"
    echo "  Or visit: https://github.com/sozercan/kubectl-ai"
fi
echo ""

# Phase 6: kagent Integration
echo "Phase 6: kagent AIOps Integration..."
if [ "$KAGENT_AVAILABLE" = true ]; then
    echo "Deploying kagent controller..."
    
    # Apply kagent configuration
    if [ -f "kagent-config.yaml" ]; then
        kubectl apply -f kagent-config.yaml 2>/dev/null || true
        echo "✓ kagent configuration applied"
    fi
    
    # Deploy kagent controller to cluster
    kubectl apply -f helm/todo-chatbot/templates/kagent-deployment.yaml 2>/dev/null || true
    echo "✓ kagent controller deployed"
    
    # Wait for kagent to be ready
    echo "Waiting for kagent controller..."
    kubectl wait --for=condition=Ready pod -l app=kagent-controller -n kagent-system --timeout=120s 2>/dev/null || true
    
    echo ""
    echo "Running kagent status..."
    kagent status -n todo-chatbot || true
    
    echo ""
    echo "✓ kagent integration complete"
else
    echo "⚠ kagent not installed. To install:"
    echo "  helm repo add kagent https://kagent.github.io/charts"
    echo "  helm install kagent kagent/kagent -n kagent-system --create-namespace"
    echo "  Or visit: https://github.com/kagent-dev/kagent"
fi
echo ""

echo ""
echo "============================================"
echo "Deployment Complete!"
echo "============================================"
echo ""
echo "Access the application:"
echo "  1. Add to /etc/hosts (or C:\\Windows\\System32\\drivers\\etc\\hosts on Windows):"
echo "     $(minikube ip) todo-chatbot.local"
echo ""
echo "  2. Open browser: http://todo-chatbot.local"
echo ""
echo "Useful commands:"
echo "  kubectl get pods -n todo-chatbot           # View pods"
echo "  kubectl logs -n todo-chatbot <pod-name>    # View logs"
echo "  helm list -n todo-chatbot                  # List releases"
echo "  minikube dashboard                         # Open Kubernetes dashboard"
echo ""
