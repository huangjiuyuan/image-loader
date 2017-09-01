import os
import logging
import subprocess
from util import filepaths
from util import images

# Getting all file paths in target directory.
gopath = os.getenv('GOPATH')
directory = '/src/k8s.io/kubernetes/test/e2e'
filepaths = filepaths.get_filepaths(
    gopath + directory)
logging.basicConfig(level=logging.DEBUG)
logging.info('Walking through directory {}'.format(directory))

# Getting Kubernetes version.
os.chdir(gopath + directory)
version = subprocess.check_output(['git', 'describe']).decode('utf-8').rstrip()
logging.info('The current version of Kubernetes is {}'.format(version))

# Getting all gcr images in the files.
gcr_images = images.get_gcr_images(filepaths)

# Logging to daocloud registry.
# logging.debug('Logging to daocloud registry')
# subprocess.call(['docker', 'login', 'daocloud.io',
#                  '-u', 'wathehack', '-p', 'dangerous'])

# Pulling images from gcr, tagging the image and pushing to daocloud registry.
images.upload_daocloud_images(gcr_images)
