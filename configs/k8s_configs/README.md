# Deployment in K8s instructions
* Have proper FQDN hostname, so that k3s picks it automatically.
```
<hostname>.kalyanch.com
```
* Install k3s and setup kubectl in dev
```sh
curl -sfL https://get.k3s.io | sh -
cat /etc/rancher/k3s/k3s.yaml

# COPY the contents to "$HOME/.kube/config" and
# CHANGE the server to "https://<hostname>.kalyanch.com:6443"
# Check kubectl
kubectl get pods -A
```
* Medvoyage Deployments
```sh
# Deploy namespace.yaml
kubectl apply -f namespace.yaml

# To revert
kubectl delete -f namespace.yaml

# Add any secrets to the namespace for other deployments
kubectl create secret generic cloudflared-token \
  --from-literal=TUNNEL_TOKEN="<cloudflared token>" \
  -n medvoyage

# Deploy MySQL with appropriate DB configuration
kubectl apply -f mysql.yaml

# Deploy Main MedVoyage App
kubectl apply -f django.yaml

# Now Deploy Nginx to serve static files and
# as proxy infront of our Django Webapp
kubectl apply -f nginx.yaml

# Now Deploy and Setup Cloudflared tunnel
kubectl apply -f cloudflared.yaml
```
* Extra
```sh
# For private registry and pulling medvoyage image
docker run -d -p 5000:5000 --restart=always --name registry registry:2

# Tag and Push
docker tag medvoyage:latest private.registry:5000/medvoyage:latest
docker push private.registry:5000/medvoyage:latest

# Modify Docker daemon to accept insecure registries for our private registry
vi /etc/docker/daemon.json
{
  "insecure-registries": ["private.registry:5000"]
}

systemctl restart docker

# Couldn't figure-out the same at k3s side since it fails with HTTP registries
# alternate is, login and pull and set image pull policy never
k3s ctr image pull --plain-http private.registry:5000/medvoyage:latest

# For checking the registry entries.
curl -X GET http://private.registry:5000/v2/_catalog
curl -X GET http://private.registry:5000/v2/medvoyage/tags/list
```
