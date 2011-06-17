from setuptools import setup, find_packages

setup(
    name="django-pdfgen",
    version="1.0.0",
    url='https://github.com/citylive/django-pdfgen',
    license='BSD',
    description="Generation of PDF documents using reportlab",
    long_description=open('README', 'r').read(),
    author='City Live NV',
    packages=find_packages('src'),
    package_data={'utilities': [
                    'templates/*.html', 'templates/*/*.html', 'templates/*/*/*.html'
                ], },
    zip_safe=False, # Don't create egg files, Django cannot find templates in egg files.
    include_package_data=True,
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)

