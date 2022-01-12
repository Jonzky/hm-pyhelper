from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='forked_hm-diag',
    version='0.13.0',
    author="Jon",
    author_email="JonZakay@aol.com",
    description="Helium Python Helper",
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jonzky/hm-pyhelper",
    install_requires=[
        'requests>=2.26.0',
        'jsonrpcclient==3.3.6',
        'retry==0.9.2'
    ],
    project_urls={
        "Bug Tracker": "https://github.com/jonzky/hm-pyhelper/issues",
    },
    packages=find_packages(),
    include_package_data=True
)
