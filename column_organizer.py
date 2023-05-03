from data_processing import read_csv, reorder_columns

def organize_columns(file_path):
    # Define the column order
    column_order = ["Departure Date", "Supplier", "Lot", "Contract", "Net Weight", "Number of Sacks"]

    # Read the CSV file into a DataFrame
    df = read_csv(file_path)

    # Reorder the DataFrame columns
    df_reordered = reorder_columns(df, column_order)

    return df_reordered
