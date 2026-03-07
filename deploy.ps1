# Todo Chatbot Minikube Deployment Script (PowerShell)
# Includes kubectl-ai and kagent AIOps integration

$ErrorActionPreference = "Stop"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Todo Chatbot - Minikube Deployment" -ForegroundColor Cyan
Write-Host "With kubectl-ai and kagent AIOps" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Phase 0: Prerequisites
Write-Host "Phase 0: Checking prerequisites..." -ForegroundColor Yellow
$commands = @("minikube", "kubectl", "helm", "docker")
foreach ($cmd in $commands) {
    if (!(Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Host "ERROR: $cmd not found. Please install it." -ForegroundColor Red
        exit 1
    }
}
Write-Host "✓ Core prerequisites OK" -ForegroundColor Green

# Check optional AIOps tools
$kubectlAiAvailable = $false
$kagentAvailable = $false

if (Get-Command "kubectl-ai" -ErrorAction SilentlyContinue) {
    $kubectlAiAvailable = $true
    Write-Host "✓ kubectl-ai found" -ForegroundColor Green
} else {
    Write-Host "⚠ kubectl-ai not found (optional)" -ForegroundColor DarkYellow
}

if (Get-Command "kagent" -ErrorAction SilentlyContinue) {
    $kagentAvailable = $true
    Write-Host "✓ kagent found" -ForegroundColor Green
} else {
    Write-Host "⚠ kagent not found (optional)" -ForegroundColor DarkYellow
}
Write-Host ""

# Phase 1: Minikube cluster
Write-Host "Phase 1: Starting Minikube cluster..." -ForegroundColor Yellow
$status = minikube status 2>&1 | Out-String
if ($status -match "Running") {
    Write-Host "✓ Minikube already running" -ForegroundColor Green
} else {
    minikube start --cpus=4 --memory=8192 --driver=docker
    Write-Host "✓ Minikube started" -ForegroundColor Green
}

minikube addons enable ingress
Write-Host "✓ Ingress enabled" -ForegroundColor Green
Write-Host ""

# Phase 2: Build Docker images
Write-Host "Phase 2: Building Docker images..." -ForegroundColor Yellow
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

Write-Host "Building backend image..."
docker build -t todo-backend:local ./backend

Write-Host "Building frontend image..."
docker build -t todo-frontend:local ./Frontend

Write-Host "✓ Images built" -ForegroundColor Green
Write-Host ""

# Phase 3: Deploy with Helm
Write-Host "Phase 3: Deploying with Helm..." -ForegroundColor Yellow
helm upgrade --install todo-chatbot ./helm/todo-chatbot `
  --namespace todo-chatbot `
  --create-namespace `
  --wait

Write-Host "✓ Helm deployment complete" -ForegroundColor Green
Write-Host ""

# Phase 4: Validation
Write-Host "Phase 4: Validating deployment..." -ForegroundColor Yellow
Write-Host "Waiting for pods to be ready..."
kubectl wait --for=condition=Ready pods --all -n todo-chatbot --timeout=300s
Write-Host "✓ All pods ready" -ForegroundColor Green
Write-Host ""

# Phase 5: kubectl-ai Integration
Write-Host "Phase 5: kubectl-ai AIOps Integration..." -ForegroundColor Yellow
if ($kubectlAiAvailable) {
    Write-Host "Running kubectl-ai deployment analysis..." -ForegroundColor Cyan
    
    # Apply kubectl-ai configuration
    if (Test-Path "kubectl-ai.yaml") {
        kubectl apply -f kubectl-ai.yaml 2>&1 | Out-Null
        Write-Host "✓ kubectl-ai configuration applied" -ForegroundColor Green
    }
    
    # Run AI-powered checks
    Write-Host "`nRunning AI-powered deployment checks:" -ForegroundColor Cyan
    kubectl-ai "analyze deployment health in namespace todo-chatbot" 2>&1 | Out-Host
    
    Write-Host "`n✓ kubectl-ai integration complete" -ForegroundColor Green
} else {
    Write-Host "⚠ kubectl-ai not installed. To install:" -ForegroundColor DarkYellow
    Write-Host "  kubectl krew install ai" -ForegroundColor White
    Write-Host "  Or visit: https://github.com/sozercan/kubectl-ai" -ForegroundColor White
}
Write-Host ""

# Phase 6: kagent Integration
Write-Host "Phase 6: kagent AIOps Integration..." -ForegroundColor Yellow
if ($kagentAvailable) {
    Write-Host "Deploying kagent controller..." -ForegroundColor Cyan
    
    # Apply kagent configuration
    if (Test-Path "kagent-config.yaml") {
        kubectl apply -f kagent-config.yaml 2>&1 | Out-Null
        Write-Host "✓ kagent configuration applied" -ForegroundColor Green
    }
    
    # Deploy kagent controller to cluster
    kubectl apply -f helm/todo-chatbot/templates/kagent-deployment.yaml 2>&1 | Out-Null
    Write-Host "✓ kagent controller deployed" -ForegroundColor Green
    
    # Wait for kagent to be ready
    Write-Host "Waiting for kagent controller..." -ForegroundColor Cyan
    kubectl wait --for=condition=Ready pod -l app=kagent-controller -n kagent-system --timeout=120s 2>&1 | Out-Null
    
    Write-Host "`nRunning kagent status..." -ForegroundColor Cyan
    kagent status -n todo-chatbot 2>&1 | Out-Host
    
    Write-Host "`n✓ kagent integration complete" -ForegroundColor Green
} else {
    Write-Host "⚠ kagent not installed. To install:" -ForegroundColor DarkYellow
    Write-Host "  helm repo add kagent https://kagent.github.io/charts" -ForegroundColor White
    Write-Host "  helm install kagent kagent/kagent -n kagent-system --create-namespace" -ForegroundColor White
    Write-Host "  Or visit: https://github.com/kagent-dev/kagent" -ForegroundColor White
}
Write-Host ""

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access the application:" -ForegroundColor Yellow
$minikubeIp = minikube ip
Write-Host "  1. Add to C:\Windows\System32\drivers\etc\hosts:" -ForegroundColor White
Write-Host "     $minikubeIp todo-chatbot.local" -ForegroundColor White
Write-Host ""
Write-Host "  2. Open browser: http://todo-chatbot.local" -ForegroundColor White
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "  kubectl get pods -n todo-chatbot           # View pods" -ForegroundColor White
Write-Host "  kubectl logs -n todo-chatbot <pod-name>    # View logs" -ForegroundColor White
Write-Host "  helm list -n todo-chatbot                  # List releases" -ForegroundColor White
Write-Host "  minikube dashboard                         # Open Kubernetes dashboard" -ForegroundColor White
Write-Host ""
