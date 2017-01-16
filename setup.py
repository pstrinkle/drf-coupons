import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(name='drf-coupons',
      version='1.0',
      packages=find_packages(),
      include_package_data=True,
      description='A django-rest-framework application that provides many varieties of coupons',
      long_description=README,
      url='https://github.com/pstrinkle/drf-coupons',
      author='Patrick Trinkle',
      author_email='patrick@1shoe.net',
      license='Apache 2.0',
      install_requires=[
          'djangorestframework',
          'django-filter',
      ],
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ])
