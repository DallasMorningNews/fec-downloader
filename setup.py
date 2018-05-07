from setuptools import setup

setup(
    name='fecdownloader',
    version='0.1.1',
    description='Bulk downloader for FEC data.',
    url='http://github.com/DallasMorningNews/fec-downloader',
    author='Andrew Chavez',
    author_email='adchavez@gmail.com',
    license='MIT',
    packages=['fecdownloader'],
    install_requires=[
        'cement',
        'requests'
    ],
    entry_points={
        'console_scripts': ['fec=fecdownloader.cli:main'],
    },
    zip_safe=False
)
