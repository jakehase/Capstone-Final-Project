import geopandas as gpd
import matplotlib.pyplot as plt

def visualize_shapefile(gdf, column=None):
    """
    Visualize a GeoDataFrame.

    Parameters:
    gdf (GeoDataFrame): The GeoDataFrame to visualize.
    column (str): The column to base the colors on.

    Returns:
    None
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # If a column is provided, color the geometries based on the values in that column.
    # Otherwise, color all geometries the same.
    if column:
        gdf.plot(column=column, ax=ax, legend=True, legend_kwds={'bbox_to_anchor': (1, 1)})
    else:
        gdf.plot(ax=ax)

    ax.set_title("Map Visualization", fontsize=20)
    ax.set_axis_off()

    plt.show()

if __name__ == "__main__":
    # Load a shapefile into a GeoDataFrame
    gdf = gpd.read_file('path_to_your_shapefile.shp')

    # Visualize the GeoDataFrame
    visualize_shapefile(gdf, column='category')
