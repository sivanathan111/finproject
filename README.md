# Five basic microservices

Five independent Python HTTP services for practicing Docker and, later, AWS deployment.
They use only Python's standard library. No packages, databases, or external services are required.

These are learning examples: each service returns its name, without business logic or communication between services.

| Service | Local port |
| --- | --- |
| users | 8001 |
| products | 8002 |
| orders | 8003 |
| payments | 8004 |
| notifications | 8005 |

Every service listens on port 8000 inside its container and provides:

- `GET /`: a JSON greeting with the service name.
- `GET /health`: a JSON health response.
- Other GET paths return HTTP 404.

## Build and run

Run these commands from the project root with Docker running:

```powershell
docker build -t users-service:local ./users-service
docker build -t products-service:local ./products-service
docker build -t orders-service:local ./orders-service
docker build -t payments-service:local ./payments-service
docker build -t notifications-service:local ./notifications-service

docker run -d --name users-service -p 8001:8000 users-service:local
docker run -d --name products-service -p 8002:8000 products-service:local
docker run -d --name orders-service -p 8003:8000 orders-service:local
docker run -d --name payments-service -p 8004:8000 payments-service:local
docker run -d --name notifications-service -p 8005:8000 notifications-service:local
```

Open http://localhost:8001 through http://localhost:8005 in your browser.
For a health check, open http://localhost:8001/health.

To run one service directly without Docker:

```powershell
python ./users-service/app.py
```

Then open http://localhost:8000. Stop it with Ctrl+C.

## Stop and remove the containers

```powershell
docker rm -f users-service products-service orders-service payments-service notifications-service
```

Each Docker build uses its own service directory as the build context.
The first Terraform lesson is in [terraform/README.md](terraform/README.md).
The Kubernetes application chart and deployment steps are in [helm/README.md](helm/README.md).
The [GitHub Actions workflow](.github/workflows/build-images.yml) builds, checks,
and publishes all five images to GHCR on pushes to `main`. It does not deploy to EKS yet.
