from __future__ import print_function
from os.path import dirname, abspath, join
import redisy
from setuptools import setup, find_packages


setup(
    name='redisy',
    version=redisy.__version__,
    description='A higher-level python native object api based on redisy-py',
    long_description=open('./README.rst').read(),
    maintainer='yytdfc',
    maintainer_email='fuchen@foxmail.com',
    keywords=['redis', 'api'],
    url='https://github.com/yytdfc/redisy',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=['redis'],
    setup_requires=['redis'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
