from setuptools import setup, find_packages
from eudplib import __version__

setup(
    name="eudplib",
    version=__version__,
    packages=find_packages(),
    package_data={
        '': ['*.dll', '*.lst'],
    },

    # metadata for upload to PyPI
    author="Trgk",
    author_email="whyask37@naver.com",
    description="EUD Trigger generator",
    license="MIT license",
    keywords="starcraft basictrigger eud",
    url="http://blog.naver.com/whyask37/",  # project home page, if any
)
