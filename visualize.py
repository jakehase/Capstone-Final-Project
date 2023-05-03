import geopandas as gpd
import matplotlib.pyplot as plt


def visualize_shapefile(file_path, column=None):
    """
    Load a shapefile from a file and visualize it.

    Parameters:
    file_path (str): The path to the shapefile.
    column (str): The column to base the colors on.

    Returns:
    None
    """
    # Load the shapefile into a GeoDataFrame
    gdf = gpd.read_file(file_path)

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
