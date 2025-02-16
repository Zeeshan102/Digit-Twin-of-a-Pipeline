import sys
from qgis.core import *

# Initialize QGIS application
QgsApplication.setPrefixPath('C:/OSGeo4W', True)  # Replace with your QGIS installation path
qgs = QgsApplication([], False)
qgs.initQgis()

sys.path.append('C:/OSGeo4W/apps/qgis-ltr/python/plugins')
from processing.core.Processing import Processing
Processing.initialize()
from processing.tools import *
import processing

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file_path>")

    else:
        # Get CSV file, point shapefile, and path shapefile paths from command line arguments
        csv_file_path = sys.argv[1]

        #Paths to point_shapefile and path_shapefiles
        point_shapefile_path = 'F:\Internship at DTNEC\QGIS Pipeline\Excel automation\Excel files\Output of CSV File\Point_Shapefile.shp'
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
        qgs.exitQgis()