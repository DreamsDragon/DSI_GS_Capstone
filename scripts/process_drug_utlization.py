from numpy import product
import pandas as pd
from utils import process_columns, describe_data
from re import sub

if __name__ == "__main__":
    from sys import argv
    from pathlib import Path

    du_data_path = Path(argv[1])  # Path of the drug utilization csv
    du_product_path = Path(argv[2])  # Path to ndc product csv
    output_path = Path(argv[3])  # Output directory
    df = pd.read_csv(du_data_path, dtype=str)  # Read du data
    df = df[
        [
            "product_name",
            "labeler_code",
            "product_code",
            "year",
            "quarter",
            "ndc",
            "number_of_prescriptions",
        ]
    ]
    df.fillna(0, inplace=True)
    df.number_of_prescriptions = df.number_of_prescriptions.str.strip()
    df["number_of_prescriptions"] = df["number_of_prescriptions"].astype("float")
    product_df = pd.read_csv(du_product_path, encoding="cp1252")  # Read prodct ndc map
    product_df = product_df[
        product_df["MARKETINGCATEGORYNAME"] == "NDA"
    ]  # Remove BLAs and only take NDA
    product_labeler_dict = product_df["PRODUCTNDC"].str.split("-", n=1, expand=True)
    product_df["labeler_code"] = product_labeler_dict[0].str.lstrip("0")
    product_df["product_code"] = product_labeler_dict[1].str.lstrip("0")
    df["product_code"] = df["product_code"].str.lstrip("0")
    df["labeler_code"] = df["labeler_code"].str.lstrip("0")
    product_df = product_df[
        ["labeler_code", "product_code", "PRODUCTNDC", "APPLICATIONNUMBER"]
    ]
    processed_df = pd.merge(df, product_df, on=["labeler_code", "product_code"])
    processed_df.rename({"APPLICATIONNUMBER": "nda"})
    print(processed_df.head(10))
    """
    product_ndc_to_nda_map = dict(zip(product_df.PRODUCTNDC, product_df.APPLICATIONNUMBER)) # Create a map of NDA to level two NDC
    processed_df = df.groupby(["product_name","year","quarter","ndc","two_level_ndc"]).sum()["number_of_prescriptions"] # Group by number of prescriptions
    processed_df = processed_df.reset_index() # Reset index
    processed_df['nda']= processed_df['two_level_ndc'].map(product_ndc_to_nda_map) # Add nda to processed column
    processed_df.dropna(inplace=True) # Drop NA rows
    processed_df = process_columns(processed_df,["product_name"]) # Process the columns
    processed_df.to_csv(Path(output_path,"processed_du_data.csv"),index=False) #Output file
    describe_data(processed_df,"drug utilization",output_path) # Output summary of output file
    """
    processed_df.to_csv(
        Path(output_path, "processed_du_data.csv"), index=False
    )  # Output file
    describe_data(
        processed_df, "drug utilization", output_path
    )  # Output summary of output file
