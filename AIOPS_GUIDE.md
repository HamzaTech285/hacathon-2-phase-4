# AIOps Integration Guide: kubectl-ai & kagent

## Overview

This guide explains the **kubectl-ai** and **kagent** integrations for Phase 4 of the Todo Chatbot hackathon. These AIOps (AI for IT Operations) tools provide intelligent automation for Kubernetes management.

---

## Table of Contents

1. [What are AIOps Tools?](#what-are-aiops-tools)
2. [kubectl-ai](#kubectl-ai)
3. [kagent](#kagent)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage Examples](#usage-examples)
7. [Phase 4 Compliance](#phase-4-compliance)

---

## What are AIOps Tools?

**AIOps (Artificial Intelligence for IT Operations)** tools use AI and machine learning to automate and enhance Kubernetes operations:

- **Automated Troubleshooting**: AI analyzes logs, events, and metrics to identify issues
- **Intelligent Recommendations**: Get optimization suggestions for resources, security, and performance
- **Natural Language Queries**: Ask questions in plain English instead of complex kubectl commands
- **Proactive Monitoring**: Detect anomalies and potential issues before they become critical

---

## kubectl-ai

### What is kubectl-ai?

**kubectl-ai** is a kubectl plugin that uses OpenAI's GPT models to generate Kubernetes manifests and answer questions about your cluster.

### Features

- **Natural Language to YAML**: Describe what you want, get Kubernetes manifests
- **Cluster Analysis**: Ask questions about your cluster state
- **Troubleshooting**: Get AI-powered diagnosis of issues
- **Best Practices**: Receive recommendations for improvements

### Pre-configured Commands

Your project includes `kubectl-ai.yaml` with these pre-configured commands:

| Command | Description |
|---------|-------------|
| `deploy-check` | Analyze deployment health |
| `troubleshoot-pods` | Diagnose failing pods |
| `security-audit` | Security best practices review |
| `optimize-resources` | Resource allocation optimization |
| `log-analysis` | Analyze application logs |
| `cost-estimate` | Estimate monthly deployment cost |

### Usage Examples

```bash
# Apply the kubectl-ai configuration
kubectl apply -f kubectl-ai.yaml

# Run AI-powered deployment analysis
kubectl-ai "analyze deployment health in namespace todo-chatbot"

# Troubleshoot failing pods
kubectl-ai "why are pods failing in todo-chatbot namespace"

# Security audit
kubectl-ai "audit security configuration for todo-chatbot"

# Resource optimization
kubectl-ai "optimize resource allocation for backend deployment"
```

---

## kagent

### What is kagent?

**kagent** is an AI-powered Kubernetes agent that runs inside your cluster and provides:

- **Autonomous Operations**: Self-healing, auto-scaling, automated fixes
- **Conversational Interface**: Chat with your cluster
- **Knowledge Base**: Documented runbooks and troubleshooting guides
- **Proactive Monitoring**: Continuous health checks and alerts

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    kagent-controller                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │   AI Agent  │  │   Tools     │  │   Knowledge     │  │
│  │  (GPT-4o)   │  │  (kubectl,  │  │     Base        │  │
│  │             │  │   logs,     │  │  (runbooks,     │  │
│  │             │  │  metrics)   │  │   guides)       │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              Todo Chatbot Namespace                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │ Frontend │  │ Backend  │  │ Postgres │               │
│  │          │  │   + MCP  │  │          │               │
│  └──────────┘  └──────────┘  └──────────┘               │
└─────────────────────────────────────────────────────────┘
```

### Capabilities

| Capability | Description |
|------------|-------------|
| Deployment Management | Monitor and manage deployments |
| Pod Management | View logs, restart pods, diagnose issues |
| Service Management | Analyze services and endpoints |
| Config Management | Review ConfigMaps and Secrets |
| Monitoring | Access metrics for CPU, memory, network |

### Pre-configured Tools

- **log-analyzer**: Summarize and analyze pod logs
- **health-checker**: Check deployment and pod health
- **resource-optimizer**: Suggest resource optimizations
- **security-scanner**: Scan for security vulnerabilities

### Auto-Heal Actions (Optional)

Configure automatic remediation:

```yaml
actions:
  - name: auto-heal
    enabled: true  # Set to true for production
    conditions:
      - pod.restartCount > 3
    action:
      type: restart
      target: pod
```

---

## Installation

### Install kubectl-ai

#### Option 1: Using krew (Recommended)

```bash
# Install krew (kubectl plugin manager)
curl -LO https://github.com/kubernetes-sigs/krew/releases/latest/download/krew.tar.gz
tar -xvf krew.tar.gz
./krew-darwin_amd64  # or krew-darwin_arm64, krew-linux_amd64, etc.

# Install kubectl-ai plugin
kubectl krew install ai
```

#### Option 2: Using pip

```bash
pip install kubectl-ai
```

#### Option 3: Using Docker

```bash
docker run -it --rm \
  -v ~/.kube:/root/.kube \
  ghcr.io/sozercan/kubectl-ai \
  "your query here"
```

### Install kagent

#### Option 1: Using Helm (Recommended)

```bash
# Add kagent Helm repository
helm repo add kagent https://kagent.github.io/charts
helm repo update

# Install kagent
helm install kagent kagent/kagent \
  -n kagent-system \
  --create-namespace \
  --set openai.apiKey=$OPENAI_API_KEY
```

#### Option 2: Using kubectl

```bash
# Apply kagent manifests
kubectl apply -f kagent-config.yaml
kubectl apply -f helm/todo-chatbot/templates/kagent-deployment.yaml
```

### Verify Installation

```bash
# Verify kubectl-ai
kubectl-ai --version

# Verify kagent
kubectl get pods -n kagent-system
kubectl get agents -n todo-chatbot
```

---

## Configuration

### Environment Variables

Set these environment variables before deployment:

```bash
# Required for both tools
export OPENAI_API_KEY="sk-your-api-key-here"

# Optional: Customize behavior
export KUBECTL_AI_MODEL="gpt-4"
export KAGENT_MODEL="gpt-4o-mini"
export KAGENT_LOG_LEVEL="info"
```

### kubectl-ai Configuration

Edit `kubectl-ai.yaml` to customize:

- **Assistant model**: Change AI model (gpt-4, gpt-3.5-turbo)
- **Pre-defined commands**: Add custom commands
- **Monitoring queries**: Add custom monitoring queries
- **Alerting rules**: Define custom alert conditions

### kagent Configuration

Edit `kagent-config.yaml` to customize:

- **Agent capabilities**: Enable/disable specific capabilities
- **Tools**: Configure available tools
- **Actions**: Set up auto-heal and auto-scale rules
- **Knowledge base**: Add custom documentation

---

## Usage Examples

### kubectl-ai Examples

```bash
# Check deployment health
kubectl-ai "show me the health of all deployments in todo-chatbot"

# Find failing pods
kubectl-ai "which pods are failing in the todo-chatbot namespace"

# Analyze logs
kubectl-ai "analyze logs of backend pod for errors"

# Security check
kubectl-ai "are there any security issues with my deployment"

# Resource optimization
kubectl-ai "suggest resource limits for the backend deployment"

# Cost estimation
kubectl-ai "estimate the monthly cost of this deployment"

# Generate manifest
kubectl-ai "create a network policy that allows traffic only from frontend to backend"
```

### kagent Examples

```bash
# Check agent status
kagent status -n todo-chatbot

# Chat with agent
kagent chat -n todo-chatbot "Why is the backend pod restarting?"

# Get recommendations
kagent recommend -n todo-chatbot

# Run health check
kagent health -n todo-chatbot

# View knowledge base
kagent kb list -n todo-chatbot
```

### Integration with Deploy Scripts

The deployment scripts automatically integrate with kubectl-ai and kagent:

```bash
# Deploy with AIOps (bash)
./deploy.sh

# Deploy with AIOps (PowerShell)
.\deploy.ps1
```

The scripts will:
1. Check if tools are installed
2. Apply configurations
3. Run AI-powered health checks
4. Provide installation instructions if not found

---

## Phase 4 Compliance

### Hackathon Requirements

| Requirement | Implementation | File |
|-------------|----------------|------|
| kubectl-ai integration | ✅ Pre-configured commands and deployment | `kubectl-ai.yaml` |
| kagent integration | ✅ Agent, UI, and KnowledgeBase CRDs | `kagent-config.yaml` |
| Kubernetes manifests | ✅ Controller deployment with RBAC | `helm/todo-chatbot/templates/kagent-deployment.yaml` |
| Deployment scripts | ✅ Updated deploy.sh and deploy.ps1 | `deploy.sh`, `deploy.ps1` |
| Documentation | ✅ This AIOps guide | `AIOPS_GUIDE.md` |

### AIOps Features Implemented

1. **kubectl-ai Configuration**
   - 6 pre-defined AI commands
   - Monitoring queries
   - Alerting rules
   - Security audit capabilities

2. **kagent Configuration**
   - Agent CRD with capabilities
   - Agent UI for chat interface
   - Knowledge base with runbooks
   - Auto-heal actions (configurable)

3. **Kubernetes Manifests**
   - kagent-controller Deployment
   - ServiceAccount and RBAC
   - ClusterRole and ClusterRoleBinding
   - Service for controller
   - Secrets for API keys

4. **Deployment Integration**
   - Automatic detection of tools
   - Configuration application
   - Health checks via AI
   - Installation instructions

---

## Troubleshooting

### kubectl-ai Issues

**Problem**: kubectl-ai command not found
```bash
# Verify installation
kubectl krew list | grep ai

# Reinstall if needed
kubectl krew install ai
```

**Problem**: API errors
```bash
# Check OPENAI_API_KEY is set
echo $OPENAI_API_KEY

# Test API key
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
```

### kagent Issues

**Problem**: kagent pods not starting
```bash
# Check pod status
kubectl get pods -n kagent-system

# View logs
kubectl logs -n kagent-system deploy/kagent-controller

# Check events
kubectl describe pod -n kagent-system -l app=kagent-controller
```

**Problem**: Agent not responding
```bash
# Verify API key secret
kubectl get secret kagent-secrets -n kagent-system -o yaml

# Check agent CRD
kubectl get agents -n todo-chatbot

# Review agent logs
kubectl logs -n kagent-system -l app=kagent-controller
```

---

## Best Practices

### Security

1. **Never commit API keys**: Use Kubernetes Secrets
2. **Limit RBAC permissions**: Use least-privilege access
3. **Enable authentication**: Configure auth for kagent UI
4. **Audit AI actions**: Review auto-heal actions before enabling

### Performance

1. **Set resource limits**: Prevent AI tools from consuming too many resources
2. **Cache responses**: Use ConfigMap for knowledge base
3. **Rate limit API calls**: Configure OpenAI rate limits
4. **Monitor usage**: Track OpenAI API usage and costs

### Operations

1. **Start with read-only**: Disable auto-heal initially
2. **Test in dev first**: Validate configurations before production
3. **Document custom commands**: Add to knowledge base
4. **Review recommendations**: AI suggestions may need validation

---

## Resources

- **kubectl-ai**: https://github.com/sozercan/kubectl-ai
- **kagent**: https://github.com/kagent-dev/kagent
- **OpenAI API**: https://platform.openai.com/docs
- **Kubernetes AI SIG**: https://github.com/kubernetes/community/tree/master/sig-ai

---

## Conclusion

With kubectl-ai and kagent integration, your Phase 4 deployment now includes:

✅ **AI-powered operations** - Natural language cluster management
✅ **Automated troubleshooting** - AI diagnosis of issues
✅ **Proactive monitoring** - Continuous health checks
✅ **Intelligent recommendations** - Optimization suggestions
✅ **Knowledge base** - Documented runbooks and guides

This completes the Phase 4 AIOps requirements for the hackathon!
