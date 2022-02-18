from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Python Image Tools package'
LONG_DESCRIPTION = 'long description'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="imagetools",
    version="0.1.0",
    description=DESCRIPTION,
    author="Rennan Marujo",
    author_email="<rennanmarujo@gmail.com>",
    url="https://github.com/marujore/image-tools",
    packages=find_packages(include=["imagetools"]),
    install_requires=[
        'colorama>=0.4.4',
        'matplotlib>=3.5.1',
        'mpl-scatter-density>=0.7',
        'numpy>=1.22.2',
        'rasterio>=1.2.10',
        'scipy==1.8.0',
        'Shapely>=1.8.0'
    ],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Linux :: Ubuntu",
        "Operating System :: Microsoft :: Windows",
    ]
)