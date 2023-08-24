from setuptools import setup, find_packages

setup(
    name='zarr2netcdf',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'xarray',
        'zarr',
        'netCDF4',
        'dask[complete]'
    ],
    entry_points={
        'console_scripts': [
            'zarr2netcdf=zarr2netcdf:main',
        ],
    },
)
