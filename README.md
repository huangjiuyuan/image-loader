# Kubernetes Test Image Loader

To run Kubernetes e2e tests, it is necessary to pull images which stores on Google Container Registry. However, it is impossible for us to pull gcr images in domestic China. This project aims to load all required images to a domestic registry on a foreign server, and load these images on a domestic server in China.

## Requirements

This tool requires a Python environment. Please check that `/usr/bin/python` does exist on your machine. If the environment variable `GOPATH` does not exist, please add this variable to your environment with

```
export GOPATH=YOUR_GOPATH
```

A Kubernetes git repository is required to get image names. Please place the Kubernetes repository in the file `$GOPATH/src/k8s.io/kubernetes`. To set up a Kubernetes repository, run

```
mkdir -p $GOPATH/src/k8s.io
cd $GOPATH/src/k8s.io
git clone https://github.com/kubernetes/kubernetes
cd kubernetes
```

It is recommended to set the desired Kubernetes version by using

```
git checkout v1.6.5
```

To check the current version of the Kubernetes under the git repository, run

```
git describe
```

## Upload Images to a Registry on a Foreign Server

Under this project root, using `upload.py` to upload images to a registry on a foreign server. To see more information, run

```
./upload.py -h
```

To specify the registry, using `-r` flag. To set username and password, useing `-u` and `-p` flags separately. For instance, to login to registry named `daocloud.io` with the username `huangjiuyuan` and password `password`, run

```
./upload.py -r daocloud.io -u huangjiuyuan -p password
```

The image will be tagged as `daocloud.io/huangjiuyuan/IMAGE_NAME` and pushed to registry named `daocloud.io`.

## Load Images to a Domestic Server

Under this project root, using `load.py` to load images to domestic server. To see more information, run

```
./load.py -h
```

To specify the registry, using `-r` flag. To set username and password, useing `-u` and `-p` flags separately. For instance, to login to registry named `daocloud.io` with the username `huangjiuyuan` and password `password`, run

```
./load.py -r daocloud.io -u huangjiuyuan -p password
```

The image named `daocloud.io/huangjiuyuan/IMAGE_NAME` willed be pulled and tagged back to its original name.

## Build Conformance Test Image

This project uses [kube-conformance](https://github.com/heptio/kube-conformance) as a tool to build the testing image. To build an intermediate testing image, run

```
docker build -t conformance-builder -f Dockerfile.conformance .
```

To build the conformance testing image, run

```
docker run -e KVER=v1.6.5 -v /var/run/docker.sock:/var/run/docker.sock conformance-builder
```

The default version of Kubernetes testing image is `v1.6.5`. Set the `KVER` environment variable by `-e` flag in the above command to specify the target version. After running the above command, a testing image named `gcr.io/heptio-images/kube-conformance` will be successfully built.
