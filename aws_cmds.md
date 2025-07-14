# AWS CMDS

- ```aws ecr create-repository --repository-name flask-backend --region us-west-2```
    - Create an ECR (container registry) repository

- ```aws ecr get-login-password --region us-west-2 docker login --username AWS --password-stdin XXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com```
    - Logging local Docker CLI into AWS ECR to push and pull images

- ```docker tag flask-backend:latest XXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/flask-backend:latest```
    - Tag docker image

- ```docker push XXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/flask-backend:latest```
    - Push docker image to AWS ECR