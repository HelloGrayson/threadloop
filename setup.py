from setuptools import setup, find_packages

install_requires = ['tornado']

# if python < 3, we need futures backport
try:
    import concurrent.futures  # noqa
except ImportError:
    install_requires.append('futures')

setup(
    name='threadloop',
    version='1.0.0',
    author='Grayson Koonce',
    author_email='breerly@gmail.com',
    description='Tornado IOLoop Backed Concurrent Futures',
    license='MIT',
    url='https://github.com/breerly/threadloop',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
