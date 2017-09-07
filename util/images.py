import re
import logging
import subprocess


def get_gcr_images(filepaths):
    """
    This function gets names of all gcr images used in the code in a provided
    directory tree.
    """

    gcr_images = set()
    image_pattern = re.compile('gcr.io[/a-zA-Z0-9_\-:.@]+[\'|\s]{0}')
    for fp in filepaths:
        for i, line in enumerate(open(fp)):
            for match in re.findall(image_pattern, line):
                gcr_images.add(match)
    return gcr_images


def get_daocloud_images(gcr_images, registry, username):
    """
    This function generates a daocloud image set from a gcr image set.
    """

    daocloud_images = set()
    for image in gcr_images:
        daocloud_image = '{}/{}/{}'.format(registry,
                                           username, image.split('/')[-1])
        daocloud_images.add(daocloud_image)
    return daocloud_images


def upload_daocloud_images(gcr_images, registry, username):
    """
    This function downloads all gcr images in an image set, tags the images
    with daocloud names and uploads all daocloud images to daocloud registry.
    """

    for image in gcr_images:
        logging.debug('Pulling image {}'.format(image))
        for i in range(0, 5):
            success = subprocess.call(['docker', 'pull', image])
            if success == 0:
                break
            if i == 4:
                logging.error('Failed on pulling image {}'.format(image))
        daocloud_image = '{}/{}/{}'.format(registry,
                                           username, image.split('/')[-1])
        logging.debug('Pushing image {}'.format(daocloud_image))
        subprocess.call(['docker', 'tag', image, daocloud_image])
        for i in range(0, 5):
            success = subprocess.call(['docker', 'push', daocloud_image])
            if success == 0:
                subprocess.call(['docker', 'rmi', daocloud_image, image])
                break
            if i == 4:
                logging.error('Failed on removing image {}'.format(image))


def download_images(images):
    """
    This function downloads all images in a image set.
    """

    for image in images:
        logging.debug('Pulling image {}'.format(image))
        for i in range(0, 3):
            success = subprocess.call(['docker', 'pull', image])
            if success == 0:
                break
            if i == 2:
                logging.error('Failed on pulling image {}'.format(image))
