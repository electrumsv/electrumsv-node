#!/usr/bin/env python3
import glob
import shutil
import subprocess
import sys
import os
from pathlib import Path
from distutils.dir_util import copy_tree

from setuptools import find_packages, setup

"""
# on a win32 machine
py -3.7-32 .\setup.py build bdist_wheel --plat-name win32
py -3.8-32 .\setup.py build bdist_wheel --plat-name win32
py -3.7 .\setup.py build bdist_wheel --plat-name win-amd64
py -3.8 .\setup.py build bdist_wheel --plat-name win-amd64
twine upload dist/*

# on a linux machine
py -3.7 .\setup.py build bdist_wheel --plat-name linux_x86_64

cd .\dist
py -3.7 -m pip install .\electrumsv_node-1.2.1-py3-none-win_amd64.whl --force
"""


with open('electrumsv_node/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('= ')[1].strip("'")
            break

bitcoin_version = '1.0.4'

if sys.platform == 'win32':
    subprocess.run(r".azure-pipelines\windows-build.bat")

    shutil.copy("MANIFEST_WIN32.in", "MANIFEST.in")

    package_bin_path = os.path.join("electrumsv_node", "bin")
    binaries_path = os.path.join("bitcoin-sv", "build", "src", "Release", "*.exe")
    for binary_path in glob.glob(binaries_path):
        shutil.copy(binary_path, package_bin_path)

elif sys.platform == 'linux':
    # Manylinux compilation is on Centos 6, and requires manual building of boost.
    # We would really want to have a pre-configured docker image with it present to make it
    # rather than faking it as we do locally.

    # subprocess.run(".azure-pipelines/linux-build.sh", shell=True)
    # if not os.path.exists("bitcoin-sv"):
    #     sys.exit("Failed to locate the Bitcoin SV build directory")

    # for artifact_name in ("bitcoind", "bitcoin-seeder", "bitcoin-cli", "bitcoin-tx",
    #         "bitcoin-miner", "LICENSE"):
    #     shutil.copy(f"bitcoin-sv/{artifact_name}", "electrumsv_node/bin/")

    # shutil.copy("MANIFEST_LINUX.in", "MANIFEST.in")

    shutil.copy("MANIFEST_LINUX.in", "MANIFEST.in")
    file_name = f"bitcoin-sv-{bitcoin_version}-x86_64-linux-gnu.tar.gz"
    subprocess.run(f"curl -L https://download.bitcoinsv.io/bitcoinsv/{bitcoin_version}/{file_name} > {file_name}", shell=True)
    subprocess.run(f"tar -xzf {file_name}", shell=True)
    linux_bitcoin = f"bitcoin-sv-{bitcoin_version}"
    copy_tree(linux_bitcoin, "electrumsv_node")
    shutil.rmtree(linux_bitcoin)

setup(
    name='electrumsv_node',
    version=version,
    description='ElectrumSV RegTest node',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    author='AustEcon',
    author_email='AustEcon0922@gmail.com',
    maintainer='AustEcon',
    maintainer_email='AustEcon0922@gmail.com',
    url='https://github.com/electrumsv/electrumsv-node',
    download_url='https://github.com/electrumsv/electrumsv-node/tarball/{}'.format(version),
    license='MIT',
    keywords=[
        'bitcoinsv',
        'bsv',
        'bitcoin sv',
        'cryptocurrency',
        'tools',
        'wallet',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    include_package_data=True,
    packages=find_packages(),
)