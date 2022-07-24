import pandas as pd
import numpy as np
import data_check
from sklearn.preprocessing import normalize
import re

def normalizer(array):
    return normalize([array])[0]

cars_data = data_check.read_data('./data/autos.csv',encoding='ISO-8859-1')

col_to_replace = {'dateCreated':'ad_created',
                 'dateCrawled':'date_crawled',
                 'fuelType':'fuel_type',
                 'lastSeen':'last_seen',
                 'monthOfRegistration':'registration_month',
                 'notRepairedDamage':'unrepaired_damage',
                 'nrOfPictures':'num_of_pictures',
                 'offerType':'offer_type',
                 'postalCode':'postal_code',
                 'powerPS':'power_ps',
                 'vehicleType':'vehicle_type',
                 'yearOfRegistration':'registration_year'}

cars_data = cars_data.rename(columns=col_to_replace)

cars_data['ad_created'] = pd.to_datetime(cars_data['ad_created'])
cars_data['date_crawled'] = pd.to_datetime(cars_data['date_crawled'])
cars_data['last_seen'] = pd.to_datetime(cars_data['last_seen'])

cars_data['price'] = cars_data['price'].apply(lambda x: int(re.sub(r'[^\d]','',x)))
cars_data['odometer'] = cars_data['odometer'].apply(lambda x: int(re.sub(r'[^\d]','',x)))

col_to_drop = ['seller','offer_type']
cars_data = cars_data.drop(col_to_drop, axis=1)

cars_data = cars_data.drop('num_of_pictures',axis=1)

cars_data = cars_data.drop(['name','postal_code'],axis=1)

Q1 = np.percentile(cars_data['price'], 25,
                   interpolation='midpoint')

Q3 = np.percentile(cars_data['price'], 75,
                   interpolation='midpoint')

print('interquartile range:', Q3 - Q1)

cars_data = cars_data[(cars_data['price'] >= 500) & (cars_data['price'] <= 40000)].reset_index(drop=True)

for col in cars_data.columns:
    if cars_data[col].dtype == 'object':
        cars_data[col] = cars_data[col].fillna(cars_data[col].mode()[0])
    elif cars_data[col].dtype == 'int64':
        cars_data[col] = cars_data[col].fillna(cars_data[col].median())


for col in cars_data2.columns:
    if cars_data2[col].dtype == 'int64':
        if col != 'price':
            arr = cars_data2[col].values
            cars_data2[col] = normalizer(arr)

for col in cars_data2.columns:
    if cars_data2[col].dtype == 'object':
        cars_data2 = pd.get_dummies(cars_data2, columns=[col], prefix=[col] )

cars_data.to_csv('./data/autos_preprocessed.csv',index=False)