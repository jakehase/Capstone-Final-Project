import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


# Read CSV file
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df


# Read Shapefile
def read_shapefile(file_path):
    gdf = gpd.read_file(file_path)
    return gdf


# Clean missing values in a DataFrame
def clean_missing_values(df, method='drop', fill_value=None):
    if method == 'drop':
        df_cleaned = df.dropna()
    elif method == 'fill':
        df_cleaned = df.fillna(fill_value)
    else:
        raise ValueError("Invalid method. Use either 'drop' or 'fill'.")

    return df_cleaned


# Filter DataFrame based on a specific column value
def filter_data(df, column, value):
    df_filtered = df[df[column] == value]
    return df_filtered


# Convert a DataFrame with latitude and longitude columns to a GeoDataFrame
def convert_to_geodataframe(df, lat_col, lon_col, crs='EPSG:4326'):
    geometry = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
    gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)
    return gdf


# Reproject a GeoDataFrame to a new coordinate reference system
def reproject_geodataframe(gdf, target_crs):
    gdf_reprojected = gdf.to_crs(target_crs)
    return gdf_reprojected


def reorder_columns(df, column_order):
    # Reorder the DataFrame columns
    df_reordered = df[column_order]
    return df_reordered
