from pathlib import Path
from helper import load_data_configuration,load_dataset_from_hub
from sklearn.model_selection import train_test_split
import pandas as pd
import os
def split_dataframe(dataframe):
    seed = 42
    train,test = train_test_split(dataframe,test_size=0.2,random_state=seed)
    return {"train":train,"test":test}
    
def save_dataframe(df:pd.DataFrame,path,filename):
    try:
        file_to_save = os.path.join(path,filename)
        df.to_csv(file_to_save)
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    config_file = Path("src/config.yml")
    data_path = Path("data")
    dict_config = load_data_configuration(config_file)
    dataset = load_dataset_from_hub(dict_config)
    data_dict = split_dataframe(dataset)
    for split,data in data_dict.items():
        filename = split+".csv"
        res = save_dataframe(data,data_path,filename)