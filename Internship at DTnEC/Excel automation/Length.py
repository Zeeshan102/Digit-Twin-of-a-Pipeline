from qgis.core import QgsApplication, QgsVectorLayer, QgsCoordinateReferenceSystem

# Set the path to your shapefile
shapefile_path = "F:\Internship at DTNEC\QGIS Pipeline\A.shp"

# Initialize QGIS application
QgsApplication.setPrefixPath("C:\Users\Public\Desktop\QGIS 3.32.2", True)  # Set the path to your QGIS installation
qgs = QgsApplication([], False)
qgs.initQgis()

# Load the shapefile as a vector layer
layer = QgsVectorLayer(shapefile_path, "my_shapefile", "ogr")

# Check if the layer loaded successfully
if not layer.isValid():
    print("Error loading the shapefile.")
else:
    # Iterate through each feature in the layer
    for feature in layer.getFeatures():
        # Access the geometry of the line feature
        geometry = feature.geometry()

        # Calculate the length of the line feature in meters with two decimal digits
        length = round(geometry.length(), 2)

        # Print the length
        print(f"Length of Line Feature {feature.id()}: {length} meters")

        # Write the length to a text file
        output_file_path = "F:\Internship at DTNEC\QGIS Pipeline\Length_value.txt"
        with open(output_file_path, 'w') as output_file:
            output_file.write(str(length))

# Exit QGIS application
qgs.exitQgis()
