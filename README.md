# Mind Clearer

## Introduction
This project is a personal diary web application. I built it using Flask, Nginx, and MongoDB inside of Docker containers.


## Notes

### MongoDB

#### Shell Commands

- To connect to Mongo cluster
`mongo "mongodb+srv://sandbox.1a2hq.mongodb.net/<cluster_name>" --username <username>`

- Show current cluster/db
`db`

- Show databases
`show dbs`

- Use a database
`use <db_name>`

- Show collections
`show collections`

- Query a collection
`db.<collection_name>.find({"field":"value"})`

- Get number of documents that match a given query
`db.<collection_name>.find({"field":"value"}).count()`

- Return query in more legible format
`db.<collection_name>.find({"field":"value"}).pretty()`

- Get a random document (to get a sense of the structure of the data)
`db.<collection_name>.findOne()`

- Insert a document in a collection
`db.<collection_name>.insert_one({"field":"value"})`

- Insert multiple documents in a collection
`db.<collection_name>.insert_many([{"field":"value"}, {"field":"value"}])`

- To clear the command line
`clc`

### Docker 

#### Commands

##### General

- To build a new image
`docker build --tag [image_name] [PATH/TO/DIR/OF/DOCKERFILE (usually '.' if running command from that directory)]`

- To run an image
`docker run -p [local_port]:[docker_port] --name [desired_process_name] -d [image_name]`

- Start a process
`docker start [process_name]`

- Stop a process
`docker stop [process_name]`

- List images
`docker images`

- List running processes
`docker ps`

- List all processes
`docker ps -a`

- Remove container (or process)
`docker rm [container_id]`

- Remove image
`docker rmi [image]`


##### DockerHub

- Tag an image (making copy)
`docker tag [image] [desired_tag_name(docker_username/repo_name:tag_name)]`

- Push image to repo
`docker push [docker_username/repo_name:tag_name]`

- Pull image from repo
`docker pull [docker_username/repo_name:tag_name]`


##### Docker-compose

- Run application with docker-compose.yml file
`docker-compose up -d`

- Stop application with docker-compose.yml file
`docker-compose down`