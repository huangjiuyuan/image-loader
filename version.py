#!/usr/bin/python
import logging
import re
import os
import subprocess


logging.debug('Setting the target k8s version')
kver = os.getenv('KVER')
version_pattern = re.compile('v[0-9]+.[0-9]+.[0-9]+')
fname = 'Makefile'
with open(fname) as f:
    tmp = fname + '.tmp'
    out = open(tmp, 'w')
    for line in f:
        out.write(re.sub(version_pattern, kver, line))
    out.close()
    os.rename(tmp, fname)
subprocess.call(['make', 'all'])
