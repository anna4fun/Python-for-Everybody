import pandas as pd
import numpy as np


### Leetcode 175 Combine Two Tables
data = [[1, 'Wang', 'Allen'], [2, 'Alice', 'Bob']]
person = pd.DataFrame(data, columns=['personId', 'firstName', 'lastName']).astype({'personId':'Int64', 'firstName':'object', 'lastName':'object'})
data = [[1, 2, 'New York City', 'New York'], [2, 3, 'Leetcode', 'California']]
address = pd.DataFrame(data, columns=['addressId', 'personId', 'city', 'state']).astype({'addressId':'Int64', 'personId':'Int64', 'city':'object', 'state':'object'})

def combine_two_tables(person: pd.DataFrame, address: pd.DataFrame) -> pd.DataFrame:
    # 75162
    # merge will dedupe overlapping columns of 2 dataframes
    # Merge 1
    raw_df = pd.merge(person, address, on=['personId'], how='left')
    # Merge 2
    raw_df = person.merge(address, on=['personId'], how='left')
    raw_df = raw_df.fillna(value=np.nan)
    raw_df = raw_df[['firstName', 'lastName', 'city', 'state']]
    return raw_df


### Leetcode 181. Employees Earning More Than Their Managers
data = [[1, 'Joe', 70000, 3], [2, 'Henry', 80000, 4], [3, 'Sam', 60000, None], [4, 'Max', 90000, None]]
employee = pd.DataFrame(data, columns=['id', 'name', 'salary', 'managerId']).astype({'id':'Int64', 'name':'object', 'salary':'Int64', 'managerId':'Int64'})

def find_employees(employee: pd.DataFrame) -> pd.DataFrame:
    raw_df = employee.merge(employee, right_on='id', left_on='managerId', how='inner',
                            suffixes=('_e', '_m'))
    results_df = raw_df.loc[raw_df['salary_e'] > raw_df['salary_m']]
    results_df = results_df[['name_e']]
    results_df.columns = ['Employee']
    return results_df