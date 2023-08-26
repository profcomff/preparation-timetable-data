from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="profcomff_parse_lib",
    version="2023.08.26",
    author="Sergey Zamyatin and Andrei Lukianov",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/preparation-timetable-data ",
    packages=find_packages(),
    install_requires=["requests", "pandas", "setuptools", "retrying", "beautifulsoup4"],
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
)
