#!/usr/bin/env python3
import shutil
import subprocess
import sys
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

bitcoin_version = '1.0.2'

if sys.platform == 'win32':
    shutil.copy("MANIFEST_WIN32.in", "MANIFEST.in")
    win32_bitcoin = Path("win32_bin")
    package_bin = Path("electrumsv_node").joinpath("bin")
    copy_tree(win32_bitcoin.__str__(), package_bin.__str__())


elif sys.platform == 'linux':
    shutil.copy("MANIFEST_LINUX.in", "MANIFEST.in")
    subprocess.run(f"wget https://download.bitcoinsv.io/bitcoinsv/{bitcoin_version}/bitcoin-sv-{bitcoin_version}-x86_64-linux-gnu.tar.gz", shell=True)
    subprocess.run(f"tar -xzf bitcoin-sv-{bitcoin_version}-x86_64-linux-gnu.tar.gz", shell=True)
    linux_bitcoin = Path(f"bitcoin-sv-{bitcoin_version}")
    copy_tree(linux_bitcoin.__str__(), "electrumsv_node")
    shutil.rmtree(linux_bitcoin.__str__())

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