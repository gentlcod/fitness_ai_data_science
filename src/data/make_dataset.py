import pandas as pd 
from glob import glob

# --------------------------------------------------------------
# Read single CSV file
# --------------------------------------------------------------
single_file_acc = pd.read_csv(
    '../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv'
)

single_file_gyr = pd.read_csv(
    '../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv'
)

# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------
files = glob('../../data/raw/MetaMotion/*.csv')
print(len(files))

# --------------------------------------------------------------
# Extract features from filename
# --------------------------------------------------------------
data_path = '../../data/raw/MetaMotion/'
f = files[0]
participant = f.split('-')[0].replace(data_path, '')
label = f.split('-')[1]
category = f.split('-')[2].rstrip('123').rstrip('_MetaWear_2019')        # Remove trailing '123' and _MetaWear_2019 so when printing the data just show in short name as it can 

df = pd.read_csv(f)

df["participant"] = participant
df["label"] = label
df["category"] = category

# --------------------------------------------------------------
# Read all files
# --------------------------------------------------------------
acc_df = pd.DataFrame()  # Initialize as an empty DataFrame
gyr_df = pd.DataFrame()

acc_set = 1
gyr_set = 1
 
for f in files:
    participant = f.split('-')[0].replace(data_path, '')
    label = f.split('-')[1]
    category = f.split('-')[2].rstrip('123').rstrip('_MetaWear_2019')       # Remove trailing '123' and _MetaWear_2019 so when printing the data just show in short name as it can  
    print(participant, label, category)
    
    df = pd.read_csv(f)
    
    df["participant"] = participant
    df["label"] = label
    df["category"] = category
    
    if 'Accelerometer' in f:
        df['set'] = acc_set
        acc_set += 1  # Increment the set number
        acc_df = pd.concat([acc_df, df], ignore_index=True)
        
    if 'Gyroscope' in f:
        df['set'] = gyr_set
        gyr_set += 1  # Increment the set number
        gyr_df = pd.concat([gyr_df, df], ignore_index=True)

# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------
acc_df.info()

pd.to_datetime(df['epoch (ms)'], unit='ms')
# df['time (01:00)'] # here when checkig this line is showing the hour is added + 1 as the previous because it is te result of the difference between UTC time and CET winter time, that one of the case sometime time confusing happen so the unix time doesn't care about summer time that why we get difference. here the dtype: object 
# (df['time (01:00)']).dt.weekday
# pd.to_datetime(df['time (01:00)']).dt.month # here the dtype: datetime64[ns]
acc_df.index = pd.to_datetime(acc_df['epoch (ms)'], unit='ms')
gyr_df.index = pd.to_datetime(gyr_df['epoch (ms)'], unit='ms')

del acc_df['epoch (ms)']
del acc_df['time (01:00)']
del acc_df['elapsed (s)']

del gyr_df['epoch (ms)']
del gyr_df['time (01:00)']
del gyr_df['elapsed (s)']
# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------
def read_data_from_files(files):
    acc_df = pd.DataFrame()  # Initialize as an empty DataFrame
    gyr_df = pd.DataFrame()
    
    acc_set = 1
    gyr_set = 1

    for f in files:
        participant = f.split('-')[0].replace(data_path, '')
        label = f.split('-')[1]
        category = f.split('-')[2].rstrip('123').rstrip('_MetaWear_2019')  
        print(participant, label, category)
        
        df = pd.read_csv(f)
        
        df["participant"] = participant
        df["label"] = label
        df["category"] = category
        
        if 'Accelerometer' in f:
            df['set'] = acc_set
            acc_set += 1  # Increment the set number
            acc_df = pd.concat([acc_df, df], ignore_index=True)
            
        if 'Gyroscope' in f:
            df['set'] = gyr_set
            gyr_set += 1  # Increment the set number
            gyr_df = pd.concat([gyr_df, df], ignore_index=True)

    # Converting 'epoch (ms)' to datetime index for both DataFrames
    acc_df.index = pd.to_datetime(acc_df['epoch (ms)'], unit='ms')
    gyr_df.index = pd.to_datetime(gyr_df['epoch (ms)'], unit='ms')

    # Removing unnecessary columns
    del acc_df['epoch (ms)']
    del acc_df['time (01:00)']
    del acc_df['elapsed (s)']

    del gyr_df['epoch (ms)']
    del gyr_df['time (01:00)']
    del gyr_df['elapsed (s)']

    return acc_df, gyr_df

# List all data in data/raw/MetaMotion
data_path = '../../data/raw/MetaMotion/'
files = glob(data_path + '*.csv')
print(len(files))

# Call the function
acc_df, gyr_df = read_data_from_files(files)

# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------
data_merged = pd.concat([acc_df.iloc[:,:3], gyr_df], axis=1) # this case so often ith some functions in pandas we can specify an access and that is either 0 or 1 (0 would be row wise and 1 would be column wis) and we want to concat these 2 data frames column wise because we want to create one row where we have all columns from both data sets  
# data_merged.dropna() 
# data_merged.head(50) 

# renaming columns
data_merged.columns = [
    'acc_x',
    'acc_y',
    'acc_z',
    'gyr_x',
    'gyr_y',
    'gyr_z',
    'participant',	
    'label'	,
    'category',	
    'set'
]


# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz
# print(data_merged.dtypes)
# data_merged[:1000].resample(rule="S").mean()


# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------
