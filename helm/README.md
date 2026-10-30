# Deploy the five services with Helm

This chart creates five Deployments and five internal ClusterIP Services. Each
Deployment runs one pod using a GHCR image and checks `/health` before marking
the pod ready. No load balancer, Ingress, or extra controller is created yet.

## Before deploying

1. Verify `kubectl get nodes` shows Ready workers and system pods are healthy.
2. Install the Helm CLI if `helm version` is not available.
3. Build and publish all five images to GHCR. This chart initially expects public
   images; private images need an image-pull secret wired into the pod template.

The owner is configured as `sivanathan111`. The expected image names are:

```text
ghcr.io/sivanathan111/users-service:latest
ghcr.io/sivanathan111/products-service:latest
ghcr.io/sivanathan111/orders-service:latest
ghcr.io/sivanathan111/payments-service:latest
ghcr.io/sivanathan111/notifications-service:latest
```

The images must actually exist and be publicly pullable before installation.
The GitHub Actions workflow builds, checks, and publishes them when pushed to
`main`. It uses the automatic `GITHUB_TOKEN`; no AWS or personal token is needed.
After first publication, change each GHCR package's visibility to Public under
your GitHub profile > Packages > package > Package settings. A public repository
does not automatically make its images public. No registry credentials belong
in this chart or its values file.

## Preview without deploying

From the project root after setting the owner:

```powershell
helm lint ./helm/finproject
helm template finproject ./helm/finproject
```

## Install after images are published

```powershell
helm upgrade --install finproject ./helm/finproject --namespace finproject --create-namespace --wait --timeout 5m
kubectl get deployments,pods,services -n finproject
```

Use the same release name and namespace on later upgrades. This command creates
application resources on your existing workers, not another EKS cluster.

For later deployments use the full commit SHA tag from a successful workflow:

```powershell
helm upgrade --install finproject ./helm/finproject --namespace finproject --create-namespace --set-string imageTag=FULL_COMMIT_SHA --wait --timeout 5m
```

Replace `FULL_COMMIT_SHA` with the actual SHA. Updating the tag changes the pod
template and triggers a rollout. Re-pushing `latest` alone does not restart
existing pods. After all five builds succeed, the workflow commits the built
commit SHA to `imageTag` in this values file. The configured Argo CD Application
watches `helm/finproject` on `main` and automatically syncs that change to EKS.
Chart-only changes do not trigger image builds because the workflow filters paths.
Once Argo CD owns the application, use Git changes for upgrades rather than
running manual Helm upgrades against the same resources.

## Test locally through the Kubernetes connection

```powershell
kubectl port-forward -n finproject service/finproject-users 8001:8000
```

Keep the command running and open http://localhost:8001 in your browser. Stop
forwarding with Ctrl+C. This is local testing; it does not expose the app publicly.

To remove only these application resources:

```powershell
helm uninstall finproject --namespace finproject
```

This does not remove EKS or other AWS infrastructure and does not stop their billing.
