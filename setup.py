from setuptools import setup, find_packages
import pdfgen


setup(
    name="django-pdfgen",
    version=pdfgen.__version__,
    url='https://github.com/citylive/django-pdfgen',
    license='BSD',
    description="Generation of PDF documents",
    long_description=open('README.rst', 'r').read(),
    author='Jef Geskens, City Live nv',
    packages=find_packages('.'),
    #package_dir={'': 'templates/*'},
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
