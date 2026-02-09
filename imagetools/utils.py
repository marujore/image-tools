import hashlib
import os

import rasterio
from rasterio.transform import Affine
from rasterio.enums import Resampling
from rasterio.io import MemoryFile
from rasterio.warp import reproject, calculate_default_transform
from rasterio.windows import Window
from shapely.geometry import box


def reproject_img(src, ref):
    transform, width, height = calculate_default_transform(
        src.crs, ref.crs, src.width, src.height, *src.bounds, resolution=ref.transform[0])
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': ref.crs,
        'transform': transform,
        'width': width,
        'height': height
    })
    print(kwargs)
    memfile = MemoryFile()
    intermed_dataset = memfile.open(
        driver='GTiff',
        height=kwargs['height'],
        width=kwargs['width'],
        count=kwargs['count'],
        dtype=kwargs['dtype'],
        crs=kwargs['crs'],
        transform=kwargs['transform'],
        nodata=kwargs['nodata']
    )
    reproject(
        source=rasterio.band(intermed_dataset, 1),
        destination=rasterio.band(intermed_dataset, 1),
        src_transform=intermed_dataset.transform,
        src_crs=intermed_dataset.crs,
        dst_transform=transform,
        dst_crs=ref.crs,
        dst_resolution=transform[0],
        resampling=Resampling.nearest)
    # print(intermed_dataset.crs, ref.crs)
    return intermed_dataset


def raster_intersection(raster1, raster2):
    # Check if data on same crs, if different must reproject
    if raster1.crs != raster2.crs:
        raster2 = reproject_img(raster2, raster1)

    bb_raster1 = box(raster1.bounds[0], raster1.bounds[1], raster1.bounds[2], raster1.bounds[3])
    bb_raster2 = box(raster2.bounds[0], raster2.bounds[1], raster2.bounds[2], raster2.bounds[3])

    xminr1, yminr1, xmaxr1, ymaxr1 = raster1.bounds
    xminr2, yminr2, xmaxr2, ymaxr2 = raster2.bounds

    intersection = bb_raster1.intersection(bb_raster2)
    transform = Affine(raster1.res[0], 0.0, intersection.bounds[0], 0.0, -raster1.res[1], intersection.bounds[3])

    p1y = intersection.bounds[3] - raster1.res[1]/2
    p1x = intersection.bounds[0] + raster1.res[0]/2
    p2y = intersection.bounds[1] + raster1.res[1]/2
    p2x = intersection.bounds[2] - raster1.res[0]/2
    # Row index raster1
    row1r1 = int((ymaxr1 - p1y)/raster1.res[1])
    # Row index raster2
    row1r2 = int((ymaxr2 - p1y)/raster2.res[1])
    # Column index raster1
    col1r1 = int((p1x - xminr1)/raster1.res[0])
    # Column index raster2
    col1r2 = int((p1x - xminr2)/raster1.res[0])

    # Row index raster1
    row2r1 = int((ymaxr1 - p2y)/raster1.res[1])
    # Row index raster2
    row2r2 = int((ymaxr2 - p2y)/raster2.res[1])
    # Column index raster1
    col2r1 = int((p2x - xminr1)/raster1.res[0])
    # Column index raster2
    col2r2 = int((p2x - xminr2)/raster1.res[0])

    width1 = col2r1 - col1r1 + 1
    width2 = col2r2 - col1r2 + 1
    height1 = row2r1 - row1r1 + 1
    height2 = row2r2 - row1r2 + 1

    arr_raster1 = raster1.read(1, window=Window(col1r1, row1r1, width1, height1))
    arr_raster2 = raster2.read(1, window=Window(col1r2, row1r2, width2, height2))

    return arr_raster1, arr_raster2


def get_file_size(path: str) -> int:
    """
    Retorna o tamanho do arquivo em bytes.
    """
    return os.path.getsize(path)


def get_sha256_checksum(path: str, chunk_size: int = 8192) -> str:
    """
    Calcula o checksum SHA-256 de um arquivo.
    """
    sha256 = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            sha256.update(chunk)

    return sha256.hexdigest()
