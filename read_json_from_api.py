import requests
from dataclasses import dataclass
import pandas as pd

@dataclass
class Person:
    userId: str 
    id: str 
    title: str
    completed: str 

def read_json_from_api():
    resp = requests.get(url="https://jsonplaceholder.typicode.com/todos/1",verify=False)
    return resp.json()
if __name__ =="__main__":
    dict_obj = dict(read_json_from_api())
    person_obj = Person(**dict_obj)
    df = pd.DataFrame([dict_obj])
    df['name_len'] = df['title'].str.len()
    res_df = df.query("name_len > 2 ")
    print(res_df.head())

