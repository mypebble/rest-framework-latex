from setuptools import setup, find_packages

setup(
    name='rest-framework-latex',
    version='0.0.2',
    description="A LaTeX renderer for Django REST Framework",
    author="SF Software limited t/a Pebble",
    author_email="sysadmin@mypebble.co.uk",
    url="https://github.com/mypebble/rest-framework-latex",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
