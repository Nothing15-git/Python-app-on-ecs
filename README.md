# DevOps Demo App

Small Flask API used as the workload for the CI/CD, DevSecOps, Kubernetes and observability projects.

Endpoints: `/` · `/health` · `/api/items` · `/metrics` (Prometheus)

## Run locally
```
cd app && pip install -r requirements-dev.txt && pytest -q
docker build -t demo-app:local .
docker run --rm -p 8080:8080 demo-app:local
curl localhost:8080/health
```

## Pipeline
`.github/workflows/ci.yml`: lint -> test -> docker build (tag = commit SHA) -> Trivy scan.
Next steps: push to ECR via OIDC, deploy to Kubernetes, add Gitleaks + SonarQube.
