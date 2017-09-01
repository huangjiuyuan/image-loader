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


def get_daocloud_images(gcr_images):
    """
    This function generates a daocloud image set from a gcr image set.
    """

    daocloud_images = set()
    for image in gcr_images:
        daocloud_image = 'registry.cn-hangzhou.aliyuncs.com/ylck/' + \
            image.split('/')[-1]
        daocloud_images.add(daocloud_image)
    return daocloud_images


def upload_daocloud_images(gcr_images):
    """
    This function downloads all gcr images in an image set, tags the images
    with daocloud names and uploads all daocloud images to daocloud registry.
    """

    for image in gcr_images:
        try:
            logging.debug('Pulling image {}'.format(image))
            subprocess.call(['docker', 'pull', image])
            daocloud_image = 'registry.cn-hangzhou.aliyuncs.com/ylck/' + \
                image.split('/')[-1]
            logging.debug('Pushing image {}'.format(daocloud_image))
            subprocess.call(['docker', 'tag', image, daocloud_image])
            subprocess.call(['docker', 'push', daocloud_image])
        except Exception as e:
            logging.error(e)
            raise e


def download_images(images):
    """
    This function downloads all images in a image set.
    """

    for image in images:
        try:
            logging.debug('Pulling image {}'.format(image))
            subprocess.call(['docker', 'pull', image])
        except Exception as e:
            logging.error(e)
            raise e
