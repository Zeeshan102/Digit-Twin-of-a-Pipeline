import os
import sys
import geopandas as gpd
import pandas as pd

def process_shapefiles(road_shapefile_directory, area_of_interest_path):
    # Load shapefiles into GeoDataFrames
    area_of_interest = gpd.read_file(area_of_interest_path).set_crs(epsg=32630)  # WGS 84 / UTM zone 30N

    # Create an empty GeoDataFrame to store the intersecting roads
    intersecting_roads = gpd.GeoDataFrame()

    # Iterate through the files in the road_shapefile_directory
    for filename in os.listdir(road_shapefile_directory):
        if filename.endswith(".shp"):  # Check if the file is a shapefile
            road_shapefile_path = os.path.join(road_shapefile_directory, filename)

            # Load the shapefile into a GeoDataFrame
            road_data = gpd.read_file(road_shapefile_path).to_crs(epsg=32630)  # WGS 84 / UTM zone 30N

            # Get the MultiLineString geometry from the area of interest
            pipeline_route = area_of_interest.geometry.iloc[0]

            # Filter the roads that intersect with the pipeline route
            roads_intersection = road_data[road_data.intersects(pipeline_route)]

            # Concatenate the intersecting roads to the overall GeoDataFrame
            intersecting_roads = pd.concat([intersecting_roads, roads_intersection])

    # Extract information from the "class" column of intersecting roads
    roads_info = intersecting_roads[["class"]]

    # Group by the class
    grouped_roads_info = roads_info.groupby("class").size().reset_index(name='number_of_crossing')

    result_csv_path = "F:\Internship at DTNEC\QGIS Pipeline\Excel automation\Excel files\Roads_info.csv"

    # Store the result in a CSV file
    grouped_roads_info.to_csv(result_csv_path, index=False, header=False)

    # Print a confirmation message
    print(f"Result has been saved to: {result_csv_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <road_shapefile_directory> <area_of_interest_path> <result_csv_path>")
        sys.exit(1)

    road_shapefile_directory = sys.argv[1]
    area_of_interest_path = sys.argv[2] 

    process_shapefiles(road_shapefile_directory, area_of_interest_path)
