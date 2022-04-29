# Muss Docker Image

## Purpose

The purpose of this project is to setup easily an environment to run [muss](https://github.com/facebookresearch/muss).

## Docker Image

The image is publicly available on [DockerHub](https://hub.docker.com/repository/docker/cleyrop/muss-debug).

## Pre-requisite

To build this image you'll need at least to have git and docker installed on a linux box.

### Build

To build this image, once you've clone the code, just run :

```bash
docker build [--no-cache] -t cleyrop/muss-debug:latest
```

`[--no-cache]` option can be passed to force build without cache.

### Run

To run a container from this image

```bash
docker run --name muss-debug --rm -d --gpu all cleyrop/muss-debug:latest
```

### Exec

To execute a shell in the docker container (as root by default but could be changed)

```bash
docker exec -ti muss-debug bash
```

### Test

Once you are un the shell, try to execute an example

```bash
time python scripts/simplify.py scripts/examples.fr --model-name muss_fr_mined
```
