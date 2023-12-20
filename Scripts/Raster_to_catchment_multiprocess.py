# Code to calculate percentages of soil type / landuse cathegory in each basin.
# Soil type or landuse cathegory is ment to be stored in tif file.
# Catchment should be in vectors (geopackage or shapefile).
# Code is counting with borders, where percentage of cell inside the polygon is calculated.
# Created by Vit Kovacka on 2023-12-20
# CAFL Aon Impact Forecasting project

# This version is running paralelly.

import rasterio
from rasterio.features import shapes
import geopandas as gpd
import os
import multiprocessing
import warnings

warnings.filterwarnings("ignore")
# Define inputs
raster_file = r"V:\Canada\Soil\Soil_perc_testing\testing_raster_Fraser.tif"
polygon_file = r"V:\Canada\Soil\Soil_perc_testing\testing_catch_Fraser.gpkg"
output_dir = r"V:\Canada\Soil\Soil_perc_testing\output"
num_cores = 48  # Set the number of cores you want to use

# Load the raster data
raster = rasterio.open(raster_file)
# print(raster.crs)
with rasterio.open(raster_file) as src:
    image = src.read(1)  # read the first band
    results = (
        {"properties": {"raster_val": v}, "geometry": s}
        for i, (s, v) in enumerate(shapes(image, transform=src.transform))
    )

# Load the polygon data
polygon_gdf = gpd.read_file(polygon_file)
# print(polygon_gdf.crs)


# Define the directory where the CSV files will be saved
# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Convert the results to a GeoDataFrame
raster_gdf = gpd.GeoDataFrame.from_features(list(results))
# print("Raster conversion done.")

# Get the total number of polygons
total_polygons = len(polygon_gdf)


def calculate_percentages(idx_row):
    idx, row = idx_row
    single_polygon = gpd.GeoDataFrame([row])
    single_polygon.set_crs(epsg=4326, inplace=True)  # Set the CRS to WGS84

    # Ensure the raster_gdf GeoDataFrame is also in WGS84
    raster_gdf.set_crs(epsg=4326, inplace=True)

    # Calculate the intersection of the raster polygons and the single polygon
    intersection = gpd.overlay(raster_gdf, single_polygon, how="intersection")

    # Calculate the area of each intersection
    intersection["area"] = intersection.geometry.area

    # Calculate the total area covered by each unique raster value
    total_areas = intersection.groupby("raster_val")["area"].sum()

    # Calculate the overall percentages
    total_area = total_areas.sum()
    overall_percentages = (total_areas / total_area) * 100

    # Save the percentages to a CSV file
    output_file = os.path.join(output_dir, f"{row['COMID']}_percentages.csv")
    overall_percentages.to_csv(output_file, header=True)

    return f"Calculated for polygon {idx+1} out of {total_polygons}"


if __name__ == "__main__":
    with multiprocessing.Pool(num_cores) as pool:
        results = pool.map(calculate_percentages, polygon_gdf.iterrows())
        for result in results:
            print(result)
