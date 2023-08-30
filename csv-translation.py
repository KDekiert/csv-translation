import pandas as pd
import numpy as np
import time
from googletrans import Translator # I used googletrans-4.0.0rc1
translator = Translator(service_urls=[
          'translate.google.com',
          'translate.google.co.kr',
        ])
translator.raise_Exception=True # avoids the raise expection error

# tell the script where the file is and what column to translate

path = '/Users/konstantin/Library/Mobile Documents/com~apple~CloudDocs/Downloads/Shape_as_table.csv'
column = 'envilmpact'





# starts timer
start_time = time.time()

# read the csv file
df = pd.read_csv(path)

# descriptives
print(df[column].head())
print(df[column].info())
print(df[column].describe())

# drop NaN values
# number of empty cells in the column but converted to a string
print("Number of empty cells in this column: " + str(df[column].isnull().sum()))

#dropped_values = df[df[column].isnull()][column]
#print(dropped_values)
df.dropna(subset=[column], inplace=True)
print("Number of empty cells in this column: " + str(df[column].isnull().sum()))

# Split the values in the column to avoid missing spaces in the translation
for index, row in df.iterrows():
    thai_words = row['envilmpact'].split()  # Split the value into individual words
    modified_value = ', '.join(thai_words)
    df.at[index, column] = modified_value

# Get unique values to save time
unique_values = df[column].unique()
# print the number of unique values and estimate the time the script will run
print("The numer of unique values is: ", len(unique_values), "the script will run for approx.: ", len(unique_values)*0.3/60, "minutes")

# Translate the unique values
translations = {}
for key in unique_values:
    value = translator.translate(key, src='th', dest='en').text
    value_with_spacing = value + ", "  # Add space after translation
    # delete the last comma and space
    value_with_spacing = value_with_spacing[:-2]
    translations[key] = value_with_spacing
    # print(key, ' -> ', value)
    time.sleep(0.3) # avoids the error 429 Too Many Requests (as of today August 30th 2023 five requests per second are allowed)

# Apply the translations to the entire DataFrame
new_column = column + '_translated'
df[new_column] = df[column].map(translations)

# save the dataframe to a new csv file using path but with an _translated added to the file name
df.to_csv(path[:-4] + '_translated.csv', index=False)

# stop timer and print the time the script ran
end_time = time.time()
print("The script ran for", (end_time - start_time)/60, "minutes")
