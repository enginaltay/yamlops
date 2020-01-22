#!/bin/bash

docker login --username=$UNAME --password=$PASSWORD


docker service rm task-api_tasks
docker service create \
    --name task-api_tasks \
    --network traefik \
    --constraint=node.role==worker \
    --replicas 3 \
    --restart-condition="on-failure" \
    --update-delay 10s \
    --label traefik.backend=tasks \
    --label traefik.frontend.rule=PathPrefix:/api/v1.0/tasks \
    --label traefik.port=5000 \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-west-1 \
    --log-opt awslogs-group=swarm-awslogs \
    --log-opt tag='{{ with split .Name ":" }}{{join . "-"}}{{end}}-{{.ID}}' \
    --with-registry-auth \
    <image_here>
