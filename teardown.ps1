# Todo Chatbot Minikube Teardown Script (PowerShell)

$ErrorActionPreference = "Continue"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Todo Chatbot - Teardown" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Uninstall Helm release
Write-Host "Uninstalling Helm release..." -ForegroundColor Yellow
helm uninstall todo-chatbot -n todo-chatbot

Write-Host "Deleting namespace..." -ForegroundColor Yellow
kubectl delete namespace todo-chatbot

Write-Host ""
Write-Host "✓ Teardown complete" -ForegroundColor Green
Write-Host ""
Write-Host "To stop Minikube:" -ForegroundColor Yellow
Write-Host "  minikube stop" -ForegroundColor White
Write-Host ""
Write-Host "To delete Minikube cluster:" -ForegroundColor Yellow
Write-Host "  minikube delete" -ForegroundColor White
Write-Host ""
