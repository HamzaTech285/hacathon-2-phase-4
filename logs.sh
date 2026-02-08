#!/bin/bash
# View logs for all Todo Chatbot pods

set -e

NAMESPACE="todo-chatbot"

echo "============================================"
echo "Todo Chatbot - Logs"
echo "============================================"
echo ""

echo "Available pods:"
kubectl get pods -n $NAMESPACE

echo ""
echo "Select component to view logs:"
echo "  1. Backend"
echo "  2. Frontend"
echo "  3. Postgres"
echo "  4. All"
read -p "Enter choice [1-4]: " choice

case $choice in
  1)
    POD=$(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}')
    kubectl logs -n $NAMESPACE $POD -f
    ;;
  2)
    POD=$(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/component=frontend -o jsonpath='{.items[0].metadata.name}')
    kubectl logs -n $NAMESPACE $POD -f
    ;;
  3)
    POD=$(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/component=postgres -o jsonpath='{.items[0].metadata.name}')
    kubectl logs -n $NAMESPACE $POD -f
    ;;
  4)
    kubectl logs -n $NAMESPACE --all-containers=true -f --prefix=true
    ;;
  *)
    echo "Invalid choice"
    exit 1
    ;;
esac
