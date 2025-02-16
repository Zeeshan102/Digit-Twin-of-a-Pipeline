import sys

sys.path.append('C:\\OSGeo4W\\apps\\qgis-ltr\\plugins')

from qgis.core import *

# Initialize QGIS application
QgsApplication.setPrefixPath("C:\OSGeo4W", True)  # Replace with your QGIS installation path
QgsApplication.initQgis()

# Specify the path to your CSV file
csv_file_path = 'F:/Internship at DTNEC/QGIS Pipeline/Excel automation/Excel files/Coordinates1.csv'

# Specify the path where you want to save the point shapefile
point_shapefile_path = 'F:\Internship at DTNEC\QGIS Pipeline\Excel automation\Excel files\Output of CSV File\Point_Shapefile.shp'

# Specify the path where you want to save the path shapefile
path_shapefile_path = 'F:\Internship at DTNEC\QGIS Pipeline\Excel automation\Excel files\Output of CSV File\Path_Shapefile.shp'

# Step 1: Create a point shapefile from the CSV file
processing.run("native:createpointslayerfromtable", {
    'INPUT': csv_file_path,
    'XFIELD': 'Longitude',
    'YFIELD': 'Latitude',
    'ZFIELD': '',
    'MFIELD': '',
    'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
    'OUTPUT': point_shapefile_path
})

print(f"Point shapefile saved to {point_shapefile_path} successfully!")

# Step 2: Convert points to a path
processing.run("native:pointstopath", {
    'INPUT': point_shapefile_path,
    'CLOSE_PATH': False,
    'ORDER_EXPRESSION': '',
    'NATURAL_SORT': False,
    'GROUP_EXPRESSION': '',
    'OUTPUT': path_shapefile_path
})

print(f"Path shapefile saved to {path_shapefile_path} successfully!")
# Finalize QGIS application
QgsApplication.exitQgis()