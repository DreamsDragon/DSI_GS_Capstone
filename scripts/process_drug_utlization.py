import pandas as pd

if __name__ == "__main__":
    from sys import argv
    from pathlib import Path
    df = pd.read_csv(Path(argv[1]))
    processed_df = df.groupby(["product_name","year","quarter"]).sum()["number_of_prescriptions"]
    processed_df.to_csv(Path(argv[2]))