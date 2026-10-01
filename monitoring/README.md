# Monitoring and Logging

The FastAPI application exposes Prometheus metrics at `/metrics`.

Recommended Minikube stack:
- Prometheus
- Grafana
- Loki
- Promtail

Example Helm commands after installing Helm:

```powershell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack
helm install loki grafana/loki-stack --set promtail.enabled=true
```

Then:
```powershell
kubectl get pods
kubectl get svc
```

Use Grafana to create dashboards for:
- HTTP request rate
- HTTP error rate
- Request latency
- CPU/memory
- Pod count
- Application logs

For a production project, use persistent storage for databases and monitoring data.
