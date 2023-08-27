import xarray as xr
import os
import dask
from dask.diagnostics import ProgressBar
import argparse


def zarr_to_netcdf(zarr_path, output_path=None, use_dask=False, verbose=False):
    """
    Convert a .zarr store to a .netcdf file.

    Parameters
    ----------
    zarr_path : str
        Path to the .zarr store.
    output_path : str, optional
        Path to save the output .netcdf file. If not provided, the output will have the same name as the input with a .netcdf extension.
    use_dask : bool, optional
        Use dask parallelization. Enables progress bar.
    verbose : bool, optional
        Print progress messages.
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
        output_path = os.path.splitext(zarr_path)[0] + '.netcdf'

    # Save the xarray dataset as a .netcdf file with progress bar
    if use_dask:
        with ProgressBar():
            ds.to_netcdf(output_path, compute=True)
    else:
        ds.to_netcdf(output_path)

    if verbose:
        print(f"Converted {zarr_path} to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert a .zarr store to a .netcdf file.")
    parser.add_argument("zarr_path", help="Path to the .zarr store.")
    parser.add_argument(
        "--output", "-o", help="Path to save the output .netcdf file. If not provided, the output will have the same name as the input with a .netcdf extension.", default=None)
    parser.add_argument("--use_dask", "-d", help="Use dask parallelization. Enables progress bar.", action="store_true")
    parser.add_argument("--verbose", "-v", help="Print progress messages.", action="store_true")
    args = parser.parse_args()
    zarr_to_netcdf(args.zarr_path, args.output, disable_dask=args.disable_dask, verbose=args.verbose)


if __name__ == "__main__":
    main()
