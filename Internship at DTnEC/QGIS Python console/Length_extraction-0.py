import pandas as pd

# Path to the shapefile
shape_file = 'F:\Internship at DTNEC\QGIS Pipeline\A.shp'

# Add the vector layer to the QGIS project
layer = iface.addVectorLayer(shape_file, 'LineLayer', 'ogr')
# Check if the layer is valid
if not layer:
    print("Error: Unable to load the layer.")
else:
    # Set the CRS to the desired one (e.g., UTM Zone 33N)
    crs = QgsCoordinateReferenceSystem('EPSG:32633')  # Change to the desired EPSG code
    layer.setCrs(crs)

    # Create an empty list to store the results
    results = []

    # Iterate through each feature in the layer
    for feature in layer.getFeatures():
        # Access the geometry of the line feature
        geometry = feature.geometry()

        # Calculate the length of the line feature in meters
        length = geometry.length()

        # Append the result to the list
        results.append({'FeatureID': feature.id(), 'Length': length})

    # Convert the list to a pandas DataFrame
    df = pd.DataFrame(results)

    # Specify the path to the Excel file
    excel_output_path = 'F:\Internship at DTNEC\QGIS Pipeline\Parameter_file.xlsx'

    # Export the DataFrame to Excel
    df.to_excel(excel_output_path, index=False)

    print(f"Length values exported to {excel_output_path}")