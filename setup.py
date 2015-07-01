from setuptools import setup, find_packages

setup(
    name='threadloop',
    version='0.1.0',
    author='Grayson Koonce',
    author_email='breerly@gmail.com',
    description='Tornado IOLoop Backed Concurrent Futures',
    license='MIT',
    url='https://github.com/breerly/threadloop',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'tornado',
        'futures'
    ]
)
