#!/bin/bash
# Todo Chatbot Minikube Teardown Script

set -e

echo "============================================"
echo "Todo Chatbot - Teardown"
echo "============================================"
echo ""

# Uninstall Helm release
echo "Uninstalling Helm release..."
helm uninstall todo-chatbot -n todo-chatbot || true

echo "Deleting namespace..."
kubectl delete namespace todo-chatbot || true

echo ""
echo "✓ Teardown complete"
echo ""
echo "To stop Minikube:"
echo "  minikube stop"
echo ""
echo "To delete Minikube cluster:"
echo "  minikube delete"
echo ""
