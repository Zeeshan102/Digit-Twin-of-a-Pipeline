import geopandas as gpd
import rasterio
from shapely.geometry import MultiLineString, Point
from rasterio.transform import from_origin
import pandas as pd

# Function to convert decimal degrees to DMS format
def dd_to_dms(degrees):
    d = int(degrees)
    m = int((degrees - d) * 60)
    s = (degrees - d - m/60) * 3600
    return d, m, s

# Load multilinestring shapefile
shapefile_path = 'F:\Internship at DTNEC\QGIS Pipeline\A.shp'
gdf = gpd.read_file(shapefile_path)

# Load raster layer
raster_path = 'F:\Internship at DTNEC\QGIS Pipeline\A.tif'
with rasterio.open(raster_path) as src:
    raster_values = src.read(1)

# Extract values along the multilinestring
num_points = 100
values_list = []

for index, row in gdf.iterrows():
    multiline = row['geometry']
    total_length = multiline.length
    step_size = total_length / num_points

    for i in range(num_points):
        distance = i * step_size
        point = multiline.interpolate(distance)
        lon, lat = point.x, point.y
        lon_dms = dd_to_dms(lon)
        lat_dms = dd_to_dms(lat)
        raster_value = raster_values[src.index(lon, lat)]

        values_list.append({
            'Longitude_DMS': lon_dms,
            'Latitude_DMS': lat_dms,
            'Raster_Value': raster_value
        })

# Create a DataFrame from the extracted values
df = pd.DataFrame(values_list)

# Save DataFrame to Excel file
excel_output_path = 'F:\Internship at DTNEC\QGIS Pipeline\Parameters_data.xlsx'
df.to_excel(excel_output_path, index=False)

print(f"Excel file with extracted values saved at: {excel_output_path}")
