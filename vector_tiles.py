import os
import geopandas as gpd
from shapely.geometry import Polygon
from osgeo import gdal, osr



gdal.UseExceptions()

directory = r"C:\Users\Christon Ledge\Documents\GIS projects\naga_solar\ortho\ortho_tiles"
output_dir = r"C:\Users\Christon Ledge\Documents\GIS projects\naga_solar\ortho\vector_tiles"
gdf_output_name = os.path.join(output_dir, 'vector_tiles.gpkg')

# Make sure output directory exists
os.makedirs(output_dir, exist_ok=True)

gdf_data = []

for filename in os.listdir(directory):

    if not filename.lower().endswith(".tif"):
        continue

    basename = os.path.splitext(filename)[0]

    input_path = os.path.join(directory, filename)
    output_name = os.path.join(output_dir, f"{basename}.gpkg")

    print(f"Processing: {filename}")

    bounds_dict = {}


    try:
        # Open raster
        src_ds = gdal.Open(input_path)

        geoTransform = src_ds.GetGeoTransform()
        proj = osr.SpatialReference(wkt=src_ds.GetProjection())
        scr_crs = proj.GetAttrValue('AUTHORITY',1)

        minx = geoTransform[0]
        maxy = geoTransform[3]
        maxx = minx + geoTransform[1] * src_ds.RasterXSize
        miny = maxy + geoTransform[5] * src_ds.RasterYSize
        
        src_ds = None

        upper_left = (minx, maxy)
        bottom_left = (minx, miny)
        upper_right = (maxx, maxy)
        bottom_right = (maxx, miny)

        coords = [upper_left,
          bottom_left,
          bottom_right,
          upper_right,]

        polygon = Polygon(coords)

        bounds_dict['Name'] = basename
        bounds_dict['CRS'] = scr_crs
        bounds_dict['geometry'] = polygon

        gdf_data.append(bounds_dict)

        if polygon is None:
            print("  FAILED to create footprint")
        else:
            print(f"  Created: {output_name}")


    except Exception as e:
        print(f"  ERROR: {e}")


gdf = gpd.GeoDataFrame(gdf_data, geometry="geometry", crs=scr_crs)
gdf.to_file(gdf_output_name, driver='GPKG')
