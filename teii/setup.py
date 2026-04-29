""" Setup script """


import os

from setuptools import find_packages, setup

_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_PATH = os.path.relpath(os.path.join(_DIR))


def read(path):
    """ Dump a file relative to this program's directory into a string. """
    with open(os.path.join(SRC_PATH, path)) as f:
        return f.read()


setup(
    name="teii",                                            # nombre del paquete
    version=f"{os.environ.get('GITHUB_RUN_NUMBER', 0)}",    # versión del paquete
    # descripción del paquete en TestPyPi
    description="Tecnologías Específicas en Ingeniería Informática",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    author="TEII",
    author_email="juanf@um.es,lfmaimo@um.es,pedroe@um.es",
    classifiers=[                                           # info para búsqueda en TestPyPi
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    keywords=["teii"],
    packages=find_packages(exclude=['tests', 'tests.*']),   # excluye tests de .whl
    install_requires=read("requirements.txt"),              # depende de pandas y requests
    python_requires=">=3.11,<3.14",                         # solo Python 3.11, 3.12 y 3.13
)
