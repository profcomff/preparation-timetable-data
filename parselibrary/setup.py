from setuptools import setup, find_packages

requirements = []

setup(
    name="parselibrary",
    version="0.0.1",
    description="Package for parsing",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
