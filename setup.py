
import glob
import shutil
import subprocess
import sys
import os

from setuptools import find_packages, setup
from setuptools.command.install import install
from setuptools.dist import Distribution

# The primary purpose of this packaging and it's compilation is that it should be invoked in the
# CI to produce binary wheels on Windows, Linux and MacOS.

"""
twine upload dist/*

# on a linux machine (this won't work unless we change the script to be)
py -3.7 ./setup.py build bdist_wheel --plat-name linux_x86_64

cd .\\dist
py -3.7 -m pip install .\\electrumsv_node-1.2.1-py3-none-win_amd64.whl --force
"""


with open('electrumsv_node/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('= ')[1].strip("'")
            break

bitcoin_version = '1.0.4'
target_names = ("bitcoind", "bitcoin-seeder", "bitcoin-cli", "bitcoin-tx", "bitcoin-miner")


def _resolve_bsv_build_path() -> str:
    build_path = os.environ.get("BSV_BUILD_PATH")
    if build_path is None:
        build_path = "bitcoin-sv"
    return build_path

BSV_BUILD_PATH = _resolve_bsv_build_path()


if sys.platform == 'darwin':
    if not os.path.exists(BSV_BUILD_PATH):
        subprocess.run(f"contrib/build/macos-build.sh {BSV_BUILD_PATH}", shell=True)

    # Bundle the executables that were just built with the node.
    package_bin_path = os.path.join("electrumsv_node", "bin")
    for target_name in target_names:
        artifact_path = os.path.join(BSV_BUILD_PATH, "src", target_name)
        shutil.copy(artifact_path, package_bin_path)

elif sys.platform == 'win32':
    if not os.path.exists(BSV_BUILD_PATH):
        subprocess.run(f"contrib\\build\\windows-build.bat {BSV_BUILD_PATH}", shell=True)

    # Bundle the executables that were just built with the node.
    package_bin_path = os.path.join("electrumsv_node", "bin")
    binaries_path = os.path.join(BSV_BUILD_PATH, "build", "src", "Release", "*.exe")
    for binary_path in glob.glob(binaries_path):
        shutil.copy(binary_path, package_bin_path)

elif sys.platform == 'linux':
    # Manylinux compilation is on Centos 6, and requires manual building of boost.
    # We would really want to have a pre-configured docker image with it present to make it
    # rather than faking it as we do locally.

    if not os.path.exists(BSV_BUILD_PATH):
        subprocess.run(f"contrib/build/linux-build.sh {BSV_BUILD_PATH}", shell=True)
    if not os.path.exists(BSV_BUILD_PATH):
        sys.exit("Failed to locate the Bitcoin SV build directory")

    for target_name in target_names:
        artifact_path = os.path.join(BSV_BUILD_PATH, "src", target_name)
        subprocess.run(f"strip {artifact_path}", shell=True)
        shutil.copy(artifact_path, "electrumsv_node/bin/")


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""
    def is_pure(self):
        return False

    def has_ext_modules(self):
        return True

# See https://github.com/google/or-tools/issues/616 and https://github.com/bigartm/bigartm/issues/840
class InstallPlatlib(install):
    def finalize_options(self):
        install.finalize_options(self)
        self.install_lib = self.install_platlib

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
    license='Open BSV',
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
    package_data={
        "": [
            "bin/*",
        ],
    },
    distclass=BinaryDistribution,
    cmdclass={
        'install': InstallPlatlib,
    }
)
