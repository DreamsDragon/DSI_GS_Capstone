import pandas as pd
from utils import process_columns,describe_data
from re import sub

if __name__ == "__main__":
    from sys import argv
    from pathlib import Path
    du_data_path = Path(argv[1]) # Path of the drug utilization csv
    du_product_path = Path(argv[2]) # Path to ndc product csv
    output_path = Path(argv[3]) # Output directory
    df = pd.read_csv(du_data_path,dtype= str) # Read du data
    df["two_level_ndc"] = df["labeler_code"].astype(str) +"-"+ df["product_code"].astype(str) # Createm two level ndc as its only one available in product ndc map
    product_df = pd.read_csv(du_product_path,encoding='cp1252') # Read prodct ndc map
    product_df = product_df[product_df["MARKETINGCATEGORYNAME"] == "NDA"] # Remove BLAs and only take NDA
    #product_df.PRODUCTNDC = product_df.PRODUCTNDC.map(lambda x:sub(r'\W+', '', x))
    product_ndc_to_nda_map = dict(zip(product_df.PRODUCTNDC, product_df.APPLICATIONNUMBER)) # Create a map of NDA to level two NDC
    processed_df = df.groupby(["product_name","year","quarter","ndc","two_level_ndc"]).sum()["number_of_prescriptions"] # Group by number of prescriptions
    processed_df = processed_df.reset_index() # Reset index
    processed_df['nda']= processed_df['two_level_ndc'].map(product_ndc_to_nda_map) # Add nda to processed column
    processed_df.dropna(inplace=True) # Drop NA rows
    processed_df = process_columns(processed_df,["product_name"]) # Process the columns
    processed_df.to_csv(Path(output_path,"processed_du_data.csv"),index=False) #Output file
    describe_data(processed_df,"drug utilization",output_path) # Output summary of output file