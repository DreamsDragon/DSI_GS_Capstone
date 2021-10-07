import pandas as pd
from utils import process_columns,describe_data

if __name__ == "__main__":
    from sys import argv
    from pathlib import Path
    df = pd.read_csv(Path(argv[1]))
    processed_df = df.groupby(["product_name","year","quarter"]).sum()["number_of_prescriptions"]
    processed_df = processed_df.reset_index()
    processed_df = process_columns(processed_df,["product_name"])
    processed_df.to_csv(Path(argv[2]),index=False)
    describe_data(processed_df,"drug utilization",argv[3])