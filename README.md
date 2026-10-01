# Online Food Ordering System – CI/CD & Kubernetes

A complete starter DevOps project for an online food-ordering application.

## Features
- Restaurant CRUD
- Menu item CRUD
- Order creation and status management
- SQLite for local development
- PostgreSQL-ready configuration
- FastAPI Swagger documentation
- Pytest automated tests
- Docker containerization
- Jenkins CI/CD pipeline
- Semantic-style Docker image versioning
- Kubernetes Deployment, Service, ConfigMap, Secret, Ingress and HPA
- Prometheus metrics
- Structured application logging
- Trivy, Bandit and pip-audit security checks
- Optional SonarQube integration

## Run locally

### Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:
http://127.0.0.1:8000/docs

### Run tests
```powershell
pytest -v
```

### Docker
```powershell
docker build -t food-ordering:1.0.0 .
docker run --rm -p 8000:8000 food-ordering:1.0.0
```

## Kubernetes with Minikube

Make sure metrics-server is enabled for HPA:
```powershell
minikube addons enable metrics-server
minikube addons enable ingress
```

Build image:
```powershell
docker build -t food-ordering:1.0.0 .
```

For Minikube Docker driver, build inside Minikube's Docker environment:
```powershell
minikube docker-env
```
Then apply:
```powershell
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/ingress.yaml
```

Check:
```powershell
kubectl -n food-ordering get all
kubectl -n food-ordering get hpa
```

## API examples

Create restaurant:
```http
POST /api/restaurants
Content-Type: application/json

{
  "name": "Mumbai Spice",
  "address": "Andheri, Mumbai",
  "phone": "9876543210",
  "status": "OPEN"
}
```

Create menu item:
```http
POST /api/menu
Content-Type: application/json

{
  "restaurant_id": 1,
  "name": "Paneer Tikka",
  "description": "Grilled cottage cheese",
  "price": 220,
  "category": "Starter",
  "availability": true
}
```

Create order:
```http
POST /api/orders
Content-Type: application/json

{
  "restaurant_id": 1,
  "customer_name": "Rahul",
  "items": [
    {"menu_item_id": 1, "quantity": 2}
  ]
}
```

## CI/CD

Jenkins pipeline stages:
1. Checkout
2. Install dependencies
3. Unit tests
4. Bandit security scan
5. pip-audit dependency scan
6. Docker build
7. Trivy filesystem/image scan
8. Docker push
9. Kubernetes deployment
10. Rollout verification

Configure Docker Hub credentials in Jenkins as:
- ID: `dockerhub-creds`
- Username/password credential

Set these Jenkins environment variables as needed:
- `DOCKER_REGISTRY_USER`
- `IMAGE_NAME`
- `KUBE_NAMESPACE`

Do not commit real credentials. The Kubernetes Secret in this demo contains placeholder values only; replace them for real deployments.

## Monitoring

Prometheus metrics are exposed at:
```text
/metrics
```

The application includes request count, request latency and standard Python/process metrics.

For a full monitoring stack, install kube-prometheus-stack and Loki separately in the cluster.

## Project structure

```text
food-ordering-system/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routes/
├── tests/
├── k8s/
├── monitoring/
├── Dockerfile
├── Jenkinsfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```
