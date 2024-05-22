import xarray as xr
import os
import dask
from dask.diagnostics import ProgressBar
import argparse


def zarr_to_netcdf(zarr_path, output_path=None, use_dask=False, verbose=False, encoding=False, encoding_level=3):
    """
    Convert a .zarr store to a netCDF (.nc) file.

    Parameters
    ----------
    zarr_path : str
        Path to the .zarr store.
    output_path : str, optional
        Path to save the output .nc file. If not provided, the output will have the same name as the input with a .nc extension.
    use_dask : bool, optional
        Use dask parallelization. Enables progress bar.
    verbose : bool, optional
        Print progress messages.
    encoding : bool, optional
        Compress the output file using zlib.
    encoding_level : int, optional
        Compression level for the output file.
    """
    # Check if the provided path exists
    if not os.path.exists(zarr_path):
        raise FileNotFoundError(f"The provided path {zarr_path} does not exist.")
    
    # Check if the provided path has a .zarr extension
    if not zarr_path.endswith('.zarr'):
        raise ValueError("The provided path does not have a .zarr extension.")

    if verbose:
        print(f"Converting {zarr_path} to .netcdf")
    # Load the .zarr store into an xarray dataset
    if use_dask:
        ds = xr.open_zarr(zarr_path, chunks='auto')
    else:
        ds = xr.open_zarr(zarr_path, chunks=None)

    # If no output path is provided, use the default naming
    if output_path is None:
        output_path = os.path.splitext(zarr_path)[0] + '.nc'

    encoding_dict = None
    if encoding:
        encoding_dict = {key: {"zlib": True, "complevel": encoding_level} for key in ds.data_vars}

    # Save the xarray dataset as a netCDF (.nc) file with progress bar
    if use_dask:
        with ProgressBar():
            ds.to_netcdf(output_path, compute=True, encoding=encoding_dict)
    else:
        ds.to_netcdf(output_path, encoding=encoding_dict)

    if verbose:
        print(f"Converted {zarr_path} to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert a .zarr store to a netCDF (.nc) file.")
    parser.add_argument("zarr_path", help="Path to the .zarr store.")
    parser.add_argument(
        "--output", "-o", help="Path to save the output netCDF file. If not provided, the output will have the same name as the input with a .nc extension.", default=None)
    parser.add_argument("--use_dask", "-d", help="Use dask parallelization. Enables progress bar.", action="store_true")
    parser.add_argument("--verbose", "-v", help="Print progress messages.", action="store_true")
    parser.add_argument("--encoding", "-e", action="store_true", help="Compress the output file using zlib.")
    parser.add_argument("--encoding_level", "-l", type=int, default=3, help="Compression level for the output file.")
    args = parser.parse_args()
    zarr_to_netcdf(args.zarr_path, args.output, use_dask=args.use_dask, verbose=args.verbose, encoding=args.encoding, encoding_level=args.encoding_level)


if __name__ == "__main__":
    main()
