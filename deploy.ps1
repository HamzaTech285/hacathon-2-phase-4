# Todo Chatbot Minikube Deployment Script (PowerShell)

$ErrorActionPreference = "Stop"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Todo Chatbot - Minikube Deployment" -ForegroundColor Cyan
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
Write-Host "✓ Prerequisites OK" -ForegroundColor Green
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

if (Get-Command kubectl-ai -ErrorAction SilentlyContinue) {
    Write-Host "Running kubectl-ai checks..." -ForegroundColor Yellow
    kubectl-ai "list pods in namespace todo-chatbot" | Out-Host
} else {
    Write-Host "kubectl-ai not found (optional)." -ForegroundColor DarkYellow
}

if (Get-Command kagent -ErrorAction SilentlyContinue) {
    Write-Host "Running kagent status..." -ForegroundColor Yellow
    kagent status -n todo-chatbot | Out-Host
} else {
    Write-Host "kagent not found (optional)." -ForegroundColor DarkYellow
}

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
