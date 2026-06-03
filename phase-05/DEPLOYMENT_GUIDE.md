# Development and Production Deployment Guide: Digital FTE Factory

This guide covers both the local development workflow and the automated production deployment for the **Digital FTE Factory SaaS**.

---

## 1. Local Development & Testing
Use these steps to test the application locally before deploying to production.

### A. Docker Compose (Production-like environment)
Verify the production build locally:
```bash
# Navigate to deployment folder
cd phase-05/deployment

# Start production-ready containers
docker-compose -f docker-compose.prod.yml up --build
```

### B. Minikube / Kubectl Deployment (Local Kubernetes)
Use Minikube to simulate production Kubernetes deployment on your machine.

1.  **Start Minikube:**
    ```bash
    minikube start
    ```

2.  **Create Secrets:**
    Kubernetes needs your environment variables as a `Secret` object.
    ```bash
    kubectl create secret generic frontend-secrets 
      --from-literal=NEXT_PUBLIC_API_URL="http://localhost:8000" 
      --from-literal=NEXT_PUBLIC_SUPABASE_URL="https://your-project.supabase.co" 
      --from-literal=NEXT_PUBLIC_SUPABASE_ANON_KEY="your-anon-key"
    ```

3.  **Deploy Application:**
    Apply the manifests in the `k8s/` directory.
    ```bash
    kubectl apply -f k8s/frontend-deployment.yaml
    ```

4.  **Access App:**
    ```bash
    minikube service frontend-service
    ```

---

## 2. Automated Production Deployment (CI/CD)
The project is configured to automatically build and push the frontend image to Docker Hub whenever changes are pushed to the `main` branch.

### Prerequisites:
- **Docker Hub Account:** (e.g., `mussaratshamsheer`).
- **GitHub Secrets:** Add these to your repo (**Settings > Secrets and variables > Actions**):
  - `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` (Read/Write/Delete), `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`.

### Triggering a Build:
Simply push your changes to the `main` branch:
```bash
git add .
git commit -m "Your commit message"
git push origin main
```
GitHub Actions will build and push the image to `DOCKERHUB_USERNAME/frontend:latest`.

---

## 3. Useful CLI Commands for Management
```bash
# Check pod status
kubectl get pods

# View logs for the frontend# Minikube Deployment Guide (Windows + PowerShell)

## Overview

This guide covers:

1. Installing Minikube
2. Starting a Kubernetes cluster
3. Deploying a Docker image
4. Exposing the application
5. Accessing the application
6. Stopping Minikube

---

# Prerequisites

Install the following:

* Docker Desktop
* kubectl
* Minikube

Verify installations:

```powershell
docker --version
kubectl version --client
minikube version
```

---

# Step 1: Start Minikube

Start a local Kubernetes cluster using Docker as the driver:

```powershell
minikube start --driver=docker
```

Verify status:

```powershell
minikube status
```

Expected:

```text
host: Running
kubelet: Running
apiserver: Running
```

---

# Step 2: Verify Kubernetes Cluster

Check cluster information:

```powershell
kubectl cluster-info
```

Check nodes:

```powershell
kubectl get nodes
```

Expected:

```text
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane
```

---

# Step 3: Deploy Docker Image

Deploy an image from Docker Hub:

```powershell
kubectl create deployment frontend --image=mussaratshamsheer/frontend:latest
```

Verify deployment:

```powershell
kubectl get deployments
```

Expected:

```text
NAME       READY   UP-TO-DATE   AVAILABLE
frontend   1/1     1            1
```

---

# Step 4: Verify Pod

Check running pods:

```powershell
kubectl get pods
```

Expected:

```text
NAME                        READY   STATUS
frontend-xxxxxxxxxx-xxxxx   1/1     Running
```

---

# Step 5: Expose Deployment

Create a Kubernetes service:

```powershell
kubectl expose deployment frontend --type=NodePort --port=80 --target-port=3000
```

Verify service:

```powershell
kubectl get services
```

Expected:

```text
NAME         TYPE       CLUSTER-IP      PORT(S)
frontend     NodePort   10.x.x.x        80:xxxxx/TCP
```

---

# Step 6: Get Application URL

Retrieve the URL:

```powershell
minikube service frontend --url
```

Example:

```text
http://172.24.68.240:32650
```

Open in browser:

```powershell
start http://172.24.68.240:32650
```

Or:

```powershell
minikube service frontend
```

---

# Monitoring Commands

View deployments:

```powershell
kubectl get deployments
```

View pods:

```powershell
kubectl get pods
```

View services:

```powershell
kubectl get services
```

View logs:

```powershell
kubectl logs deployment/frontend
```

Describe deployment:

```powershell
kubectl describe deployment frontend
```

Describe pod:

```powershell
kubectl describe pod <pod-name>
```

---

# Updating Docker Image

After pushing a new image to Docker Hub:

```powershell
kubectl rollout restart deployment/frontend
```

Check rollout status:

```powershell
kubectl rollout status deployment/frontend
```

---

# Delete Deployment

Delete deployment:

```powershell
kubectl delete deployment frontend
```

Delete service:

```powershell
kubectl delete service frontend
```

---

# Stop Minikube

Stop the cluster:

```powershell
minikube stop
```

Verify:

```powershell
minikube status
```

Expected:

```text
host: Stopped
```

---

# Start Again Later

When you want to continue:

```powershell
minikube start
```

Verify:

```powershell
kubectl get nodes
kubectl get deployments
kubectl get pods
```

Your deployment and service will still exist unless you deleted them.

---

# Complete Workflow

```text
Docker Image
      ↓
Minikube Start
      ↓
Kubernetes Deployment
      ↓
Pod Running
      ↓
Service Creation
      ↓
Minikube URL
      ↓
Application Accessible
      ↓
Minikube Stop
```

kubectl logs -l app=frontend

# Restart deployment (to pull latest image)
kubectl rollout restart deployment frontend

# Delete deployment
kubectl delete -f k8s/frontend-deployment.yaml
```
