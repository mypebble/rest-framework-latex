from setuptools import setup, find_packages

setup(
    name='rest-framework-latex',
    version='0.1.0',
    description="A LaTeX renderer for Django REST Framework",
    author="Pebble",
    author_email="sysadmin@mypebble.co.uk",
    url="https://github.com/mypebble/rest-framework-latex",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django', 'djangorestframework', 'six',
    ]
)
