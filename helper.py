from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_validate
import numpy as np
import pandas as pd
import pickle

imp_nums = ['Age',
 'Length',
 'BP',
 'FBS',
 'TG',
 'ESR',
 'K',
 'Na',
 'Lymph',
 'PLT',
 'EF-TTE']

imp_cats = ['DM',
 'HTN',
 'Typical Chest Pain',
 'Dyspnea',
 'Atypical',
 'Nonanginal',
 'Tinversion']


imp_ords = ['Region RWMA']

def preprocess(data):
    preprocessor = ColumnTransformer(transformers = [('OHE', OneHotEncoder(handle_unknown='ignore', sparse_output=False, drop='first', dtype=np.int64), imp_cats),
                                                 ('Scaler', StandardScaler(), imp_nums)],
                                 remainder = 'passthrough',
                                 verbose_feature_names_out = False).set_output(transform = 'pandas')
    return preprocessor.fit_transform(data)



# BMI Calculator
def calculate_bmi(weight, height):
    if height > 0:
        return weight / ((height / 100) ** 2)
    else:
        return 0
    


num_cols = ['Age','Weight', 'Length','BMI', 'BP', 'PR', 'FBS', 'CR', 'TG', 'LDL', 'HDL', 'BUN', 'ESR', 'HB', 'K', 'Na', 'WBC', 'Lymph', 'Neut', 'PLT', 'EF-TTE']

cat_cols = ['Sex', 'DM', 'HTN', 'Current Smoker', 'EX-Smoker', 'FH', 'Obesity', 'CRF', 'CVA', 'Airway disease', 'Thyroid Disease', 'CHF', 'DLP', 'Edema', 'Weak Peripheral Pulse', 'Lung rales', 'Systolic Murmur', 'Diastolic Murmur', 'Typical Chest Pain', 'Dyspnea', 'Atypical', 'Nonanginal', 'Exertional CP', 'LowTH Ang', 'Q Wave', 'St Elevation', 'St Depression', 'Tinversion', 'LVH', 'Poor R Progression']

ord_cols = ['Function Class', "Region RWMA", "VHD"]


import numpy as np
import pandas as pd


# PREDICTION
def predict(data):
    file_path = 'cat_model.pkl'
    # Numerical variables:
    data = preprocess(data)
    with open(file_path, 'rb') as file:
            model = pickle.load(file)
            pred = model.predict(data)
            return pred


# PREPROCESS

def preprocess(data):
    with open('preprocessor.pkl', 'rb') as f:
        preprocessor = pickle.load(f)
    data = preprocessor.transform(data)
    key_order = ['Sex_Male',
            'DM_1',
            'HTN_1',
            'Current Smoker_1',
            'EX-Smoker_1',
            'FH_1',
            'Obesity_1',
            'CRF_1',
            'CVA_1',
            'Airway disease_1',
            'Thyroid Disease_1',
            'CHF_1',
            'DLP_1',
            'Edema_1',
            'Weak Peripheral Pulse_1',
            'Lung rales_1',
            'Systolic Murmur_1',
            'Diastolic Murmur_1',
            'Typical Chest Pain_1',
            'Dyspnea_1',
            'Atypical_1',
            'Nonanginal_1',
            'LowTH Ang_1',
            'Q Wave_1',
            'St Elevation_1',
            'St Depression_1',
            'Tinversion_1',
            'LVH_1',
            'Poor R Progression_1',
            'Age',
            'Weight',
            'Length',
            'BMI',
            'BP',
            'PR',
            'FBS',
            'CR',
            'TG',
            'LDL',
            'HDL',
            'BUN',
            'ESR',
            'HB',
            'K',
            'Na',
            'WBC',
            'Lymph',
            'Neut',
            'PLT',
            'EF-TTE',
            'Function Class',
            'Region RWMA',
            'VHD']
    ordered_dict = {key: data[key] for key in key_order if key in data}
    return pd.DataFrame(ordered_dict)


        
        
            