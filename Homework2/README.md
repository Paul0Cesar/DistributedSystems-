# Distributed Systems - Homework 2 :computer:

### Use virtual enviroment:

To enable virtual env ,if you not have virtualenv,use this comand for install :

```shell
 pip install virtualenv
```

And for enable use this :

```shell
 virtualenv env
 . env/bin/activate
```

### Install Dependecies : 

```shell
pip install -r requirements.txt
```

### Running the Apache Spark: 

```shell
docker-compose up -d
```

Afther running, you can check here :  http://your-server-ip:8080

### Running the Kafka: 

enter in kafka path and run this command:

```shell
docker-compose up -d
```

Afther running, you can check here :  http://your-server-ip:19000


> **Warning:** 
> For running Apache Spark, you need install : [Docker Compose](https://docs.docker.com/compose/install/linux/)


> **Note:** 
> For more details about the image used in docker compose: [bitnami/spark](https://hub.docker.com/r/bitnami/spark/)
