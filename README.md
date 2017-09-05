# Kubernetes Test Image Loader
To run Kubernetes e2e tests, it is necessary to pull images which stores on Google Container Registry. However, it is impossible for us to pull gcr images in domestic China. This project aims to load all required images to a domestic registry on a foreign server, and load these images on a domestic server in China.

# Requirements
This tool requires a Python environment. Please check that `/usr/bin/python` does exist on your machine.
A Kubernetes git repository is required to get image names. Please place the Kubernetes repository in the file `$GOPATH/src/k8s.io/kubernetes`. It is recommended to set the desired Kubernetes version by using `git checkout v1.6.5`, run `git describe` to check the current version of the Kubernetes under the git repository. If the environment variable `GOPATH` does not exist, please add this variable to your environment.

## Upload Images to a Registry on a Foreign Server
Using `upload.py` to upload images to a registry on a foreign server. Run `./upload.py -h` to see more information.
To specify the registry, using `-r` flag. To set username and password, useing `-u` and `-p` flags separately. For instance, running `./upload.py -r daocloud.io -u huangjiuyuan -p password` to login to registry named `daocloud.io` with the username `huangjiuyuan` and password `password`. The image will be tagged as `daocloud.io/huangjiuyuan/my-image-name` and pushed to registry named `daocloud.io`.

# Load Images to a Domestic Server
Using `load.py` to load images to domestic server. Run `./load.py -h` to see more information.
To specify the registry, using `-r` flag. To set username and password, useing `-u` and `-p` flags separately. For instance, running `./load.py -r daocloud.io -u huangjiuyuan -p password` to login to registry named `daocloud.io` with the username `huangjiuyuan` and password `password`. The image named `daocloud.io/huangjiuyuan/my-image-name` willed be pulled and tagged back to its original name.
