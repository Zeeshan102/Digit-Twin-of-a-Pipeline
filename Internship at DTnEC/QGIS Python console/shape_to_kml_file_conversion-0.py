import geopandas as gpd

# Replace 'your_shapefile.shp' with the actual path to your shapefile
shapefile_path = "F:\Internship at DTNEC\QGIS Pipeline\A.shp"

# Read the shapefile into a GeoDataFrame
gdf = gpd.read_file(shapefile_path)

# Ensure that the 'KML' driver is supported
gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'


# Replace 'output.kml' with the desired full path and name for the KML file
kml_file_path = 'F:\Internship at DTNEC\QGIS Pipeline\output.kml'

# Specify the correct CRS (EPSG:32630) when saving to KML
gdf.to_file(kml_file_path, driver='KML', crs='EPSG:32630')

print(f'Conversion completed. KML file saved at: {kml_file_path}')
