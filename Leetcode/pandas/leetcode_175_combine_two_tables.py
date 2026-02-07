import pandas as pd
import numpy as np

# input
data = [[1, 'Wang', 'Allen'], [2, 'Alice', 'Bob']]
person = pd.DataFrame(data, columns=['personId', 'firstName', 'lastName']).astype({'personId':'Int64', 'firstName':'object', 'lastName':'object'})
data = [[1, 2, 'New York City', 'New York'], [2, 3, 'Leetcode', 'California']]
address = pd.DataFrame(data, columns=['addressId', 'personId', 'city', 'state']).astype({'addressId':'Int64', 'personId':'Int64', 'city':'object', 'state':'object'})

def combine_two_tables(person: pd.DataFrame, address: pd.DataFrame) -> pd.DataFrame:
    # merge will dedupe overlapping columns of 2 dataframes
    raw_df = pd.merge(person, address, on=['personId'], how='left')
    raw_df = raw_df.fillna(value=np.nan)
    raw_df = raw_df[['firstName', 'lastName', 'city', 'state']]
    return raw_df