import pandas as pd


df=pd.read_excel('/Users/soodk2/Documents/Roche_documents/deviation_en_all.xlsx')
# Getting the frequency count of the event_classification column
print(df.groupby('event_classification').count())

# Filtering event classification which has number of records less than 20
df = df.groupby('event_classification').filter(lambda x: len(x) >= 20)
print(df.groupby('event_classification').count())

# Getting the frequency count of the event_details
print(df.groupby('event_details').count())

# Filtering event details which has number of records less than 20
df = df.groupby('event_details').filter(lambda x: len(x) >= 20)
print(df.groupby('event_details').count())

# Exporting the filtered data frame to a .csv file
df.to_csv('/Users/soodk2/Documents/Extracted_files/Preprocessed_data/Filtered_deviation_records.csv',
header=True, index=False)