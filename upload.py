import re
import os
import logging
import subprocess
import stat
from util import filepaths

# Getting all file paths in target directory.
gopath = os.getenv('GOPATH')
directory = '/src/k8s.io/kubernetes/test/e2e'
file_paths = filepaths.get_filepaths(
    gopath + directory)
logging.basicConfig(level=logging.DEBUG)
logging.info('Walking through directory {}'.format(directory))

# Getting Kubernetes version.
os.chdir(gopath + directory)
version = subprocess.check_output(['git', 'describe']).decode('utf-8').rstrip()
logging.info('The current version of Kubernetes is {}'.format(version))

# Getting all gcr images in the files.
image_set = set()
image_pattern = re.compile('gcr.io[/a-zA-Z0-9_\-:.@]+[\'|\s]{0}')
for fp in file_paths:
    for i, line in enumerate(open(fp)):
        for match in re.findall(image_pattern, line):
            image_set.add(match)

# Logging to daocloud registry.
logging.debug('Logging to daocloud registry')
subprocess.call(['docker', 'login', 'daocloud.io',
                 '-u', 'wathehack', '-p', 'dangerous'])

# Pulling images from gcr, tagging the image and pushing to daocloud registry.
for image in image_set:
    logging.debug('Pulling image {}'.format(image))
    subprocess.call(['docker', 'pull', image])
    daocloud_image = 'daocloud.io/daocloud/' + image.split('/')[-1]
    logging.debug('Pushing image {}'.format(daocloud_image))
    subprocess.call(['docker', 'tag', image, daocloud_image])
    subprocess.call(['docker', 'push', daocloud_image])
