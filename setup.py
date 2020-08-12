
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


BSV_BUILD_PATH = os.environ.get("BSV_BUILD_PATH", "bitcoin-sv")
BSV_BUILD_ARTIFACTS_PATH = os.environ.get("BSV_BUILD_ARTIFACTS_PATH", "bitcoin-sv-results")
BSV_GIT_URI = os.environ.get("BSV_GIT_URI", "https://github.com/electrumsv/bitcoin-sv")
BSV_GIT_BRANCH = os.environ.get("BSV_GIT_BRANCH", "bugfix/cmake-windows-build")

PACKAGE_BIN_PATH = os.path.join("electrumsv_node", "bin")


def _copy_build_artifacts_to_package() -> None:
    shutil.rmtree(PACKAGE_BIN_PATH)
    os.mkdir(PACKAGE_BIN_PATH)

    for target_name in os.listdir(BSV_BUILD_ARTIFACTS_PATH):
        target_path = os.path.join(BSV_BUILD_ARTIFACTS_PATH, target_name)
        if os.path.islink(target_path):
            continue
        if os.path.isfile(target_path):
            shutil.copy(target_path, PACKAGE_BIN_PATH)
        elif os.path.isdir(target_path):
            shutil.copytree(target_path, os.path.join(PACKAGE_BIN_PATH, target_name))


if sys.platform == 'darwin':
    if not os.path.exists(BSV_BUILD_ARTIFACTS_PATH):
        subprocess.run(
            f"contrib/build/macos-build.sh {BSV_BUILD_PATH} {BSV_GIT_URI} {BSV_GIT_BRANCH}",
            shell=True)
        if not os.path.exists(BSV_BUILD_PATH):
            sys.exit("Failed to locate the Bitcoin SV build directory")

        ARTIFACT_PATHS = (
            os.path.join("src", "bitcoind"),
            os.path.join("src", "bitcoin-seeder"),
            os.path.join("src", "bitcoin-cli"),
            os.path.join("src", "bitcoin-tx"),
            os.path.join("src", "bitcoin-miner"),
        )

        os.mkdir(BSV_BUILD_ARTIFACTS_PATH)
        for artifact_path in ARTIFACT_PATHS:
            shutil.copy(os.path.join(BSV_BUILD_PATH, artifact_path), BSV_BUILD_ARTIFACTS_PATH)

    _copy_build_artifacts_to_package()

elif sys.platform == 'win32':
    if not os.path.exists(BSV_BUILD_ARTIFACTS_PATH):
        subprocess.run(
            f"contrib\\build\\windows-build.bat {BSV_BUILD_PATH} {BSV_GIT_URI} {BSV_GIT_BRANCH}",
            shell=True)
        if not os.path.exists(BSV_BUILD_PATH):
            sys.exit("Failed to locate the Bitcoin SV build directory")

        BUILD_SUBPATH = os.path.join(BSV_BUILD_PATH, "build", "src", "Release")
        ARTIFACT_PATHS = (
            os.path.join(BUILD_SUBPATH, "bitcoind.exe"),
            os.path.join(BUILD_SUBPATH, "bitcoin-cli.exe"),
            os.path.join(BUILD_SUBPATH, "bitcoin-tx.exe"),
            os.path.join(BUILD_SUBPATH, "bitcoin-miner.exe"),
        )

        os.mkdir(BSV_BUILD_ARTIFACTS_PATH)
        for artifact_path in ARTIFACT_PATHS:
            shutil.copy(os.path.join(BSV_BUILD_PATH, artifact_path), BSV_BUILD_ARTIFACTS_PATH)

    _copy_build_artifacts_to_package()

elif sys.platform == 'linux':
    # Manylinux compilation is on Centos 6, and requires manual building of boost.
    # We would really want to have a pre-configured docker image with it present to make it
    # rather than faking it as we do locally.

    if not os.path.exists(BSV_BUILD_ARTIFACTS_PATH):
        subprocess.run(
            f"contrib/build/linux-build.sh {BSV_BUILD_PATH} {BSV_GIT_URI} {BSV_GIT_BRANCH}",
            shell=True)
        if not os.path.exists(BSV_BUILD_PATH):
            sys.exit("Failed to locate the Bitcoin SV build directory")

        ARTIFACT_PATHS = (
            os.path.join("src", "bitcoind"),
            os.path.join("src", "bitcoin-seeder"),
            os.path.join("src", "bitcoin-cli"),
            os.path.join("src", "bitcoin-tx"),
            os.path.join("src", "bitcoin-miner"),
        )

        os.mkdir(BSV_BUILD_ARTIFACTS_PATH)
        for artifact_path in ARTIFACT_PATHS:
            shutil.copy(os.path.join(BSV_BUILD_PATH, artifact_path), BSV_BUILD_ARTIFACTS_PATH)

    _copy_build_artifacts_to_package()


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
        'License :: Open BSV',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: POSIX :: Linux',
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
    install_requires=[
        'requests',
    ],
    distclass=BinaryDistribution,
    cmdclass={
        'install': InstallPlatlib,
    }
)
