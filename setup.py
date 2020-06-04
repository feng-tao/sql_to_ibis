from distutils.core import setup
from setuptools import find_packages
import os
from pathlib import Path

from versioneer import get_cmdclass, get_version

CODE_DIRECTORY = Path(__file__).parent


def read_file(filename):
    """Source the contents of a file"""
    with open(
        os.path.join(os.path.dirname(__file__), filename), encoding="utf-8"
    ) as file:
        return file.read()


setup(
    name="sql_to_ibis",
    version=get_version(),
    cmdclass=get_cmdclass(),
    packages=find_packages(),
    long_description="Coming soon...",
    maintainer="Zach Brookler",
    maintainer_email="zachb1996@yahoo.com",
    description="A package for converting sql into ibis expressions",
    python_requires=">=3.6.1",
    install_requires=["lark-parser==0.8.1", "ibis"],
    project_urls={
        "Source Code": "https://github.com/zbrookle/sql_to_ibis",
        "Documentation": "https://github.com/zbrookle/sql_to_ibis",
        "Bug Tracker": "https://github.com/zbrookle/sql_to_ibis/issues"
    },
    url="https://github.com/zbrookle/sql_to_ibis",
    download_url="https://github.com/zbrookle/sql_to_ibis/archive/master.zip",
    keywords=["pandas", "data", "dataframe", "sql", "ibis"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    long_description_content_type="text/markdown",
    include_package_data=True
)
