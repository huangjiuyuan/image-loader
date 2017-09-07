#!/usr/bin/python
import os
import logging
import subprocess
import sys
from util import filepaths
from util import images
from util import login

# Getting all file paths in target directory.
gopath = os.getenv('GOPATH')
directory = '/src/k8s.io/kubernetes/test/e2e'
filepaths = filepaths.get_filepaths(
    gopath + directory)
logging.basicConfig(level=logging.WARNING)
logging.info('Walking through directory {}'.format(directory))

success, registry, username, password = login.login()
if success != True:
    sys.exit(1)

# Getting Kubernetes version.
os.chdir(gopath + directory)
version = subprocess.check_output(['git', 'describe']).decode('utf-8').rstrip()
logging.info('The current version of Kubernetes is {}'.format(version))

# Getting all gcr images in the files.
gcr_images = images.get_gcr_images(filepaths)

# Pulling all daocloud images.
daocloud_images = images.get_daocloud_images(
    gcr_images, registry, username)
images.download_images(daocloud_images)

# Tagging daocloud images as gcr images.
for gcr_image in gcr_images:
    for daocloud_image in daocloud_images:
        if gcr_image.split('/')[-1] == daocloud_image.split('/')[-1]:
            logging.debug('Tagging image {} as {}'.format(
                daocloud_image, gcr_image))
            subprocess.call(['docker', 'tag', daocloud_image, gcr_image])
