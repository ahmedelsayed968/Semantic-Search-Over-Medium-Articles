import yaml
from datasets import DatasetDict,load_dataset
from huggingface_hub import hf_hub_download
import pandas as pd
def load_data_configuration(path):
    with open(path,mode="r") as file:
        config = yaml.safe_load(file)
    return config

def romove_cols(dataset,config):
    desired_cols = config['dataset']['desired_cols']

    for idx,data in enumerate(dataset):
        cols_to_remove = [col for col in data.column_names if col not in desired_cols]
        dataset[idx] = dataset[idx].remove_columns(cols_to_remove)
    return dataset
    
def convert_to_dataset_dict(dataset,config):
    data = DatasetDict()
    for split,subset in zip(config['dataset']['splits'],dataset):
        data[split] = subset
    return data

def load_dataset_from_hub(config)->DatasetDict:
    
    dataset = pd.read_csv(hf_hub_download(repo_id=config['dataset']['repo_id'],
                                          filename=config['dataset']['file_name'],
                                          repo_type=config['dataset']['repo_type']))
    
    return dataset

    