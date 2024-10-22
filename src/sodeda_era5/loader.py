import xarray as xr

class ARCO_ERA5:
    def __init__(self, subset="arco-era5") -> None:
        available_subsets = ["weatherbench2","arco-era5"]
        if subset not in available_subsets:
            raise RuntimeError(f"`subset` can only be one of {','.join(available_subsets)}")
        
        if subset == "weatherbench2":
            self.ds = xr.open_zarr(
                "gs://weatherbench2/datasets/era5/1959-2023_01_10-wb13-6h-1440x721_with_derived_variables.zarr"
            )
        elif subset == "arco-era5":
            self.ds = xr.open_zarr(
                'gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3',
                chunks=None,
                storage_options=dict(token='anon'),
            )

    def scope(self):
        scope = {}
        coords = self.ds.coords
        for coord in coords:
            scope[coord] = {
                "start": coords[coord].min().values,
                "end": coords[coord].max().values,
            }
        scope["latitude"] = {"start": 90, "end": -90}
        scope["level"] = coords["level"].values
        scope["variable"] = list(self.ds.variables.keys())
        return scope

    def __call__(self, **deskriptor):
        variables = deskriptor["variable"]
        if variables is None:
            raise RuntimeError(
                "No `variable` found, please provide one or multiple variables"
            )
        if not isinstance(deskriptor["variable"], list):
            variables = [variables]

        subsets = []
        for variable in variables:
            slicer = to_slicer(deskriptor, exclude="variable")
            selected_datatarray = self.ds[variable]

            for coord in list(slicer.keys()):
                if coord not in selected_datatarray.coords:
                    slicer.pop(coord)

            selected_data = selected_datatarray.sel(slicer)

            subsets += [selected_data]

        # dataset = xr.combine_by_coords(subsets)

        if not isinstance(deskriptor["variable"], list):
            return subsets[0]

        return subsets

def to_slicer(deskriptor, **kwargs):
    deskriptor_dict = deskriptor
    slicer = {}
    for key in deskriptor_dict:
        if isinstance(deskriptor_dict[key], dict):
            ni = {"start": None, "end": None, "step": None}
            ni.update(deskriptor_dict[key])
            slicer[key] = slice(ni["start"], ni["end"], ni["step"])
        else:
            slicer[key] = deskriptor_dict[key]
    return slicer
