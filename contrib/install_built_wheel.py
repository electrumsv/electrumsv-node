import os
import subprocess
import sys
from pathlib import Path


def main():
    MODULE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
    if len(sys.argv) > 1:
        wheeldir_name = sys.argv[1]
        WHEELHOUSE_DIR = MODULE_DIR.parent.joinpath(wheeldir_name)
    else:
        WHEELHOUSE_DIR = MODULE_DIR.parent.joinpath("dist")

    with open(MODULE_DIR.parent.joinpath('electrumsv_node/__init__.py'), 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                version = line.strip().split('= ')[1].strip("'")
                break

    py_version = None
    if sys.version_info.major == 3 and sys.version_info.minor == 8:
        py_version = 'cp38-cp38'
    elif sys.version_info.major == 3 and sys.version_info.minor == 9:
        py_version = 'cp39-cp39'
    elif sys.version_info.major == 3 and sys.version_info.minor == 10:
        py_version = 'cp310-cp310'
    elif sys.version_info.major == 3 and sys.version_info.minor == 11:
        py_version = 'cp311-cp311'

    wheel_path = None
    if sys.platform == 'linux': # electrumsv_node-0.0.23-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
        wheel_path = WHEELHOUSE_DIR.joinpath(
            f"electrumsv_node-{version}-{py_version}-manylinux_2_17_x86_64.manylinux2014_x86_64.whl")
    if sys.platform == 'darwin':
        wheel_path = WHEELHOUSE_DIR.joinpath(
            f"electrumsv_node-{version}-{py_version}-macosx_10_9_x86_64.whl")
    if sys.platform == 'win32':
        wheel_path = WHEELHOUSE_DIR.joinpath(
            f"electrumsv_node-{version}-{py_version}-win_amd64.whl")

    subprocess.run(f"{sys.executable} -m pip install --force --no-cache {str(wheel_path)} --user",
                   shell=True, check=True)


main()
