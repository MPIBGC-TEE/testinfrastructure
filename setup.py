# vim:set ff=unix expandtab ts=4 sw=4:
from setuptools import setup, find_packages
def readme():
    with open('README.md') as f:
        return f.read()

setup(name='test_infrastructure',
        version='0.1',
        #test_suite="example_package.tests",#http://pythonhosted.org/setuptools/setuptools.html#test
        description='Infrastructure for IO-tests that need filesystem separation',
        long_description=readme(),#avoid duplication 
        author='Markus Müller',
        author_email='markus.mueller.1.g@googlemail.com',
        packages=find_packages(), #find all packages (multifile modules) recursively
        classifiers = [
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Education "
        ],
        include_package_data=True,
        zip_safe=False)

