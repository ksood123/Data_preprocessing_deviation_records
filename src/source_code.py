import pandas as pd
import os
from sklearn.model_selection import train_test_split


# Defining the source path to read the original file and detsination path to write the final .csv file
source_path = '/Users/soodk2/Documents/Roche_documents/deviation_en_all.xlsx'
destination_path = '/Users/soodk2/Documents/Extracted_files/Preprocessed_data/Filtered_deviation_records.csv'


# This function filters the categories that have less than 20 records 
def filtering_records(source_path, destination_path):
    # Reading the original file
    df=pd.read_excel(source_path)

    ########################## REMOVING THE CATEGORIES WHICH HAVE LESS THAN 20 RECORDS ###########################
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
    df.to_csv(destination_path, header=True, index=False)


# This functions creates .txt files and also creates data frames, both according to the specified format
def extract_to_folder(df, path, label):
    # Extracting the combined_text into .txt file with rec_id as the file name
    # Creating a new data frame with the sepcific format
    df_temp = pd.DataFrame(columns = ['Split_name', 'File_name', 'Category'])
    row_indexer = 1
    for i in range(df.shape[0]):
        file_name = str(df.iloc[i,4]) + '.txt'
        text = str(df.iloc[i,10])
        # Creating two rows for each record
        df_temp = df_temp.append([{'Split_name': label, 'File_name': str(os.path.join(path,file_name)), 'Category':'NULL'}]*2,
        ignore_index=True)
        # Defining categories list
        categories = []
        categories.append(str(df.iloc[i,6])) ; categories.append(str(df.iloc[i,7]))
        # Creating two records for the single file
        for j in range(2):
            df_temp.iloc[row_indexer + j - 1, 2] = categories[j]
            
        with open(os.path.join(path,file_name), "w") as f:
            if text:
                f.write(text)
        row_indexer += 2
    return df_temp


# Reading the original file and cretaing a .csv file with the categories containing at least 20 records
filtering_records(source_path, destination_path)

# Importing the file containing the filtered records into a data frame
df = pd.read_csv('/Users/soodk2/Documents/Extracted_files/Preprocessed_data/Filtered_deviation_records.csv')


# Getting the indices of the columns- rec_id and combined_text
print(df.columns.get_loc('rec_id')) # 4
print(df.columns.get_loc('combined_text')) # 10
print(df.columns.get_loc('event_classification')) # 6
print(df.columns.get_loc('event_details')) # 7

# Splitting the data frame into train, validation and test data frames
train, val_test = train_test_split(df,test_size = 0.3, random_state = 42)
val, test = train_test_split(val_test, test_size = 0.15, random_state = 42)

# Creating a list to store the train, test and validation data frames
df_list = [] ; df_list.append(train) ; df_list.append(val) ; df_list.append(test)

# Printing the shapes of the train, validation and test data frames
print(train.shape) ; print(val.shape) ; print(test.shape)

# Folder directory where we write the files
folder_path = '/Users/soodk2/Documents/Extracted_files/Record_text_files'

# Writing the folder names to a list
folder_names = ['/Train', '/Validation', '/Test']

# Defining labels to a list
labels = ['TRAIN', 'VALIDATION', 'TEST']

# Creating a list to hold the new data frames created according to the specified format
df_created  = []

# Looping thrice- once for each train, validation and test sets
for i in range(3):
    actual_path = folder_path + folder_names[i]
    df_created.append(extract_to_folder(df_list[i], actual_path, labels[i]))

# Exporting the new data frames created to .csv files
for i in range(3):
    actual_path = folder_path + folder_names[i]
    file_name = actual_path + '/' + labels[i] + '.csv'
    df_created[i].to_csv(file_name, header = True, index = True)


