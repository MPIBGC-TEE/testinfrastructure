#!/usr/bin/env python3
# vim:set ff=unix expandtab ts=4 sw=4 fileencoding=utf-8:

from setuptools import setup, find_packages
def readme():
    with open('README.md') as f:
        return f.read()

def non_src_requirements():
    with open("requirements.non_src") as f:
        return [l.strip() for l in f.readlines()]

setup(name='testinfrastructure',
        version='0.1',
        #test_suite="example_package.tests",#http://pythonhosted.org/setuptools/setuptools.html#test
        description='Infrastructure for IO-tests that need filesystem separation',
        long_description=readme(),#avoid duplication 
        author='Markus Müller',
        author_email='markus.mueller.1.g@googlemail.com',
        packages=find_packages('src'), #find all packages (multifile modules) recursively
        package_dir={'': 'src'},
        classifiers = [
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Education "
        ],
        entry_points={
        'console_scripts': [
                'test_notebooks = testinfrastructure.test_notebooks:test_notebooks_cmd'
                ]
        },
        include_package_data=True,
        zip_safe=False,
        install_requires=[ ] + non_src_requirements()
)
