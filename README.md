# README for `zarr2netcdf`

## Description

`zarr2netcdf` is a utility that facilitates the conversion of `.zarr` stores to `.netcdf` files. This can be convenient for moving files over `scp`. It uses [xarray](https://github.com/pydata/xarray) and [dask](https://github.com/dask/dask) to handle the conversion. With optional flags, you can customize the output path and disable `dask` processing if needed. 

## Features

- Convert `.zarr` stores to `.netcdf` format.
- Efficient handling of large datasets using `dask`.
- Optional progress bar for tracking the conversion process (only when `dask` is enabled).
- Command-line interface and utility for easy integration into workflows.

## Installation

You can install zarr2netcdf.py as a command line tool using:

```bash
pip install .
```

Requirements are `xarray zarr netCDF4 dask[complete]`.

## Usage

To convert a `.zarr` store to a `.netcdf` file:

```bash
zarr2netcdf path_to_your_file.zarr
```

### Optional Arguments:

- **Specify Output Path**:
  Use the `--output` or `-o` flag to specify a custom path for the output `.netcdf` file:

  ```bash
  zarr2netcdf path_to_your_file.zarr --output path_to_output_file.netcdf
  ```

  If not provided, the output will have the same name as the input with a `.netcdf` extension.

- **Disable Dask Parallelization**:
  Use the `--disable_dask` or `-n` flag to disable `dask` parallelization and the progress bar:

  ```bash
  zarr2netcdf path_to_your_file.zarr --disable_dask
  ```
