import os


def get_filepaths(directory):
    """
    This function will generate the file names in a directory tree by walking
    the tree either top-down or bottom-up. For each directory in the tree
    rooted at directory top, including top itself, it yields a 3-tuple:
    dirpath, dirnames, filenames.
    """

    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths
