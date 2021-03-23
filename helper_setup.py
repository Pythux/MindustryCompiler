"""
    some helper function for setup.py file
    use: copy it alongside setup.py and in the setup.py file:
    from helper_setup import read_readme, activate_cmd_build, activate_cmd_publish
"""
import sys
import os
import shutil
from setuptools import find_packages
from importlib import import_module


def read(*paths):
    with open(*paths, 'r') as f:
        return f.read()


def read_readme():
    """will read the README.* file, it can be any extention"""
    return read(next(filter(lambda f: 'README.' in f, os.listdir('.'))))


def activate_cmd_publish():
    """
        need to be run in setup.py to take action,
        if `python setup.py publish`: will build / upload / clean
    """
    if sys.argv[-1] == 'publish':
        publish()
        sys.exit()


def activate_cmd_build():
    """
        need to be run in setup.py to take action,
        if `python setup.py build`: will build
    """
    if sys.argv[-1] == 'build':
        wheel()
        sys.exit()


def wheel():
    clean_dirs()
    check_installed_tools()
    build_wheel()


def publish():
    wheel()
    upload_wheel()
    clean_dirs()
    print_git_tag_info()


def check_installed_tools():
    if os.system('pip freeze | grep twine > /dev/null'):
        print('twine not installed.\n\tUse `pip install twine`')
        sys.exit()


def build_wheel():
    print('\nbuilding ...')
    os.system('python setup.py bdist_wheel > /dev/null')  # omit sdist, build only the wheel


def upload_wheel():
    print('\nuploading ...')
    os.system('twine upload dist/*')  # upload the package to PyPI


def is_ext(ext):
    ext = ext[1:] if ext[0] == '.' else ext

    def with_file(file):
        splited = file.split('.')
        return len(splited) > 1 and splited[-1] == ext
    return with_file


def get_files_ext(ext):
    return filter(is_ext(ext), os.listdir('.'))


def clean_dirs():
    for dir in ['dist', 'build']:
        shutil.rmtree(dir, ignore_errors=True)
    for egg in get_files_ext('.egg-info'):
        shutil.rmtree(egg)


def print_git_tag_info():
    __init__ = import_module(find_packages()[0])
    print('\nYou probably want to also tag the version now:')
    print("  git tag -a v{0} -m 'release {0}'".format(__init__.__version__))
    print('  git push --tags')
