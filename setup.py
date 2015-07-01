from setuptools import setup, find_packages

install_requires = ['tornado']

# if python < 3, we need futures backport
try:
    import concurrent.futures  # noqa
except ImportError:
    install_requires.append('futures')

setup(
    name='threadloop',
    version='0.2.0',
    author='Grayson Koonce',
    author_email='breerly@gmail.com',
    description='Tornado IOLoop Backed Concurrent Futures',
    license='MIT',
    url='https://github.com/breerly/threadloop',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires
)
