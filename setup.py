from setuptools import setup, find_packages

from malias import __version__

setup(
    name = "malias",
    version = __version__,
    author = 'Stuart Fable',
    author_email = 'stuart.fable@gmail.com',
    license = 'MIT',
    keywords = 'malias system alias',
    description = '',
    url = 'https://github.com/sfable/malias',
    download_url = 'https://github.com/sfable/malias/archive/master.zip',
    packages = find_packages(),
    install_requires = ['docopt'],
    zip_safe = True,
    entry_points = {
        'console_scripts': ['malias=malias.cli:main']
    },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ]
)
