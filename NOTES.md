

https://docs.djangoproject.com/en/1.10/intro/reusable-apps/

http://www.revsys.com/blog/2014/nov/21/recommended-django-project-layout/

http://python-packaging.readthedocs.io/en/latest/dependencies.html

http://www.mkdocs.org/

before trying to package for pypi:

1. `pip install twine`
2. `pip install wheel`
3. `python setup.py sdist`
4. `python setup.py bdist_wheel`
