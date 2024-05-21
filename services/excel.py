import pandas as pd

def read_names_from_excel(file_path, sheet_name, first_name_column, last_name_column, middle_name_column=None):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    if middle_name_column:
        names = df.apply(lambda x: f"{x[first_name_column]} {x[middle_name_column]} {x[last_name_column]}" if pd.notnull(x[middle_name_column]) else f"{x[first_name_column]} {x[last_name_column]}", axis=1).tolist()
    else:
        names = df.apply(lambda x: f"{x[first_name_column]} {x[last_name_column]}", axis=1).tolist()
    return names
