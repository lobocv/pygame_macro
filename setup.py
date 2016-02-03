
from distutils.core import setup
import importlib

__version__ = importlib.import_module('pygame_macro._version').__version__


setup(
    name='pygame_macro',
    packages=['pygame_macro'],
    version=__version__,
    description="Record and play-back pygame events by saving macros",
    author='Calvin Lobo',
    author_email='calvinvlobo@gmail.com',
    url='https://github.com/lobocv/pygame_macro',
    download_url='https://github.com/lobocv/pygame_macro/tarball/%s' % __version__,
    keywords=['pygame', 'event', 'gui', 'ui', 'test', 'testing', 'macro'],
    classifiers=[],
)