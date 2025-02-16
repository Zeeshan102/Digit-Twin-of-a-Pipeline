import sys
from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsProject,
    QgsWkbTypes,
    QgsCoordinateTransform,
    QgsPointXY,
    QgsCoordinateReferenceSystem,
)

# Function to set CRS for the layer
def set_crs(layer, crs):
    layer.setCrs(crs)
    if not layer.isValid():
        print(f"Error: Unable to set CRS for the layer.")
        # Handle the error appropriately

def main(shapefile_path, raster_path):
    # Initialize QGIS application
    QgsApplication.setPrefixPath("C:\\Program Files\\QGIS 3.28.15", True)  # Replace with your QGIS installation path
    qgs = QgsApplication([], False)
    qgs.initQgis()

    # Set the desired CRS (EPSG 32630)
    desired_crs = QgsCoordinateReferenceSystem('EPSG:32630')

    # Load the shapefile and raster layers
    vector_layer = QgsVectorLayer(shapefile_path, "VectorLayer", "ogr")
    set_crs(vector_layer, desired_crs)
    raster_layer = QgsRasterLayer(raster_path, "RasterLayer")
    set_crs(raster_layer, desired_crs)

    # Check if both layers loaded successfully
    if not vector_layer.isValid() or vector_layer.geometryType() != QgsWkbTypes.LineGeometry or not raster_layer.isValid():
        print("Error: Please add a valid line shapefile and raster layer to the layers panel.")
    else:
        # Create an empty list to store the results
        results = []

        # Get the coordinate transform for raster layer
        raster_crs = raster_layer.crs()
        transform = QgsCoordinateTransform(vector_layer.crs(), raster_crs, QgsProject.instance())

        # Iterate through each feature in the vector layer
        for feature in vector_layer.getFeatures():
            # Access the geometry of the line feature
            geometry = feature.geometry()

            # Calculate the length of the MultiLineString with up to 2 decimal places
            length = round(geometry.length(), 2)

            # Check if the geometry is MultiLineString
            if geometry.isMultipart():
                # Iterate through each part of the MultiLineString
                for part in geometry.asMultiPolyline():
                    # Extract the starting and ending points from each part
                    start_point = part[0]
                    end_point = part[-1]

                    # Transform the starting and ending points to raster layer CRS
                    start_point_transformed = transform.transform(start_point.x(), start_point.y())
                    end_point_transformed = transform.transform(end_point.x(), end_point.y())

                    # Extract elevation values at the starting and ending points
                    start_elevation = raster_layer.dataProvider().sample(QgsPointXY(start_point_transformed), 1)[0]
                    end_elevation = raster_layer.dataProvider().sample(QgsPointXY(end_point_transformed), 1)[0]

                    # Append the results to the list
                    results.append((
                        length,
                        start_point_transformed.x(),
                        start_point_transformed.y(),
                        end_point_transformed.x(),
                        end_point_transformed.y(),
                        start_elevation,
                        end_elevation,
                ))
            else:
                # Extract the starting and ending points directly
                start_point = geometry.asPolyline()[0]
                end_point = geometry.asPolyline()[-1]

                # Transform the starting and ending points to raster layer CRS
                start_point_transformed = transform.transform(start_point.x(), start_point.y())
                end_point_transformed = transform.transform(end_point.x(), end_point.y())

                # Extract elevation values at the starting and ending points
                start_elevation = raster_layer.dataProvider().sample(QgsPointXY(start_point_transformed), 1)[0]
                end_elevation = raster_layer.dataProvider().sample(QgsPointXY(end_point_transformed), 1)[0]

                # Append the results to the list
                results.append((
                    length,
                    start_point_transformed.x(),
                    start_point_transformed.y(),
                    end_point_transformed.x(),
                    end_point_transformed.y(),
                    start_elevation,
                    end_elevation,
                ))

    # Specify the path to the text file
    text_output_path = 'F:/Internship at DTNEC/QGIS Pipeline/Excel automation/Excel files/Length_Coordinates_Elevation_shapefile.txt'

    # Write the results to the text file
    with open(text_output_path, "w") as file:
        for values in results:
            for value in values:
                file.write(str(value) + "\n")  # Write each value on a separate line

    print(f"Length, Coordinates, and Elevation values appended to {text_output_path}")


    # Finalize QGIS application
    qgs.exitQgis()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <shapefile_path> <raster_path>")
        sys.exit(1)
    shapefile_path = sys.argv[1]
    raster_path = sys.argv[2]
    main(shapefile_path, raster_path)
