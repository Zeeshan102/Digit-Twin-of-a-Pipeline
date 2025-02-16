import sys
import geopandas as gpd
from shapely.geometry import MultiLineString

def main():
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python script.py <node_file_path> <link_file_path> <area_of_interest_path>")
        sys.exit(1)

    # Extract file paths from command line arguments
    link_file_path = sys.argv[1]
    area_of_interest_path = sys.argv[2]

    # Load shapefiles into GeoDataFrames
    links = gpd.read_file(link_file_path).to_crs(epsg=27700)  # OSGB36 / British National Grid
    area_of_interest = gpd.read_file(area_of_interest_path).set_crs(epsg=32630)  # WGS 84 / UTM zone 30N

    # Ensure that the Coordinate Reference Systems (CRS) match for proper spatial operations
    links = links.to_crs(epsg=32630)  # WGS 84 / UTM zone 30N

    # Get the MultiLineString geometry from the area of interest
    pipeline_route = area_of_interest.geometry.iloc[0]

    # Filter the rivers that intersect with the pipeline route
    intersecting_rivers = links[links.intersects(pipeline_route)]

    # Extract information from the "form" column of intersecting rivers
    river_info = intersecting_rivers[["form"]]

    # Group by the form and calculate the count and sum of lengths
    grouped_river_info = river_info.groupby("form").agg({'form': 'count'}).rename(columns={'form': 'number_of_crossing'})

    # Resetting index to make "form" a column again
    grouped_river_info = grouped_river_info.reset_index()

    # Store the result in a CSV file
    result_csv_path = "F:\Internship at DTNEC\QGIS Pipeline\Excel automation\Excel files\Rivers_info.csv"
    grouped_river_info.to_csv(result_csv_path, index=False, header=False)

    # Print a confirmation message
    print(f"Result has been saved to: {result_csv_path}")

if __name__ == "__main__":
    main()
