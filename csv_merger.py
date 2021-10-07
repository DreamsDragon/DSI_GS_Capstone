import pandas as pd

class CSVMerger():
    def __call__(self,file_list:dict):
        final_data = None

        for fnames,fcols in file_list.items():
            final_data = pd.read_csv(fnames[0])
            try:
                final_data[fcols[0]] = final_data[fcols[0]].str.upper()
                print("Number of unique values in {0} of {1} is: {2}".format(fcols[0],fnames[0],final_data[fcols[0]].nunique()))
            except:
                pass
            for i,col_name in enumerate(fcols[1:]):
                other_data = pd.read_csv(fnames[i+1])
                try:
                    other_data[col_name] =  other_data[col_name].str.upper()
                    print("Number of unique values in {0} of {1} is: {2}".format(col_name,fnames[i+1],other_data[col_name].nunique()))
                except:
                    pass

                final_data = pd.merge(final_data,other_data,left_on=fcols[i],right_on=col_name)
        return final_data

if __name__ == "__main__":
    


    file_list = {("./data/full_processed_du.csv","./data/FAERS_Summary.csv","./data/clean_data.csv"):("product_name","drugnameclean","Drug Name")}
    merger = CSVMerger()

    final_pd = merger(file_list)
    print(final_pd.shape)
    print(final_pd.head(10))
    print(final_pd.product_name.nunique())
    