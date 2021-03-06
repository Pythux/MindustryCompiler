from setuptools import setup, find_packages
from importlib import import_module
from helper_setup import read_readme, activate_cmd_build, activate_cmd_publish, moveAtBuild


#################################################################


description = \
    'language that compile to Mindusty ASM, jump instruction can use references instead of line number, and more ...'
url = "https://github.com/Pythux/MindustryCompiler"
install_requires = ['PyBoa', 'ply']
classifiers = [
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    "Intended Audience :: Education",  # because it's fun !
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
]
license = 'GNU3',

entry_points = {
    'console_scripts': [
        'mindc = compiler.__main__:main'
    ]
}

#################################################################

moveAtBuild([('./code', './compiler/code')])
activate_cmd_build()  # can do: python setup.py build
activate_cmd_publish()  # can do: python setup.py publish
__init__ = import_module(find_packages()[0])
setup(
    name=__init__.__title__,
    version=__init__.__version__,
    author=__init__.__author__,
    # author_email='',
    description=description,
    long_description=read_readme(),  # Get the README file, can be .md, .rst, ...
    long_description_content_type="text/markdown",
    url=url,
    packages=find_packages(),
    package_data={find_packages()[0]: ['code/*', 'code/**/*', 'code/**/**/*']},
    classifiers=classifiers,
    install_requires=install_requires,  # external packages as dependencies,
    python_requires='>=3.6',
    license=license,
    entry_points=entry_points,
)

# install in dev mode:
# pip install --editable .
