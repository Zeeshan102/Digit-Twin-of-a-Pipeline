import geopandas as gpd

QgsApplication.setPrefixPath("C:\OSGeo4W", True)  # Replace with your QGIS installation path
qgs = QgsApplication([], False)
qgs.initQgis()

# Replace these file paths with the actual paths to your shapefiles
link_file_path = "F:\Internship at DTNEC\QGIS Pipeline\Shapefile of rivers\data\WatercourseLink.shp"
area_of_interest_path = "F:\Internship at DTNEC\QGIS Pipeline\A.shp"  # Shapefile containing MultiLineString for pipeline route

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

# Group by the form
grouped_river_info = river_info.groupby("form").agg({'form': 'count'}).rename(columns={'form': 'number_of_crossing'})

# Resetting index to make "form" a column again
grouped_river_info = grouped_river_info.reset_index()

# Store the result in a CSV file without headers
result_csv_path = "F:\Internship at DTNEC\QGIS Pipeline\Excel automation\Excel files\Rivers_info.csv"
grouped_river_info.to_csv(result_csv_path, index=False, header=False)

# Print a confirmation message
print(f"Result has been saved to: {result_csv_path}")
qgs.exitQgis()
