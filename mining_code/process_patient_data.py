from pymongo import MongoClient
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


class PatientProcess:

    @staticmethod
    def get_patient_base_data():
        client = MongoClient(port=27017)
        #print(client)
        db=client.adtProject
        coll = db.patientData
        #print(coll)
        sample=coll.find({}, {'_id': 0})
        #print(sample)
        json_projects = []
        for project in sample:
            json_projects.append(project)
        df = pd.DataFrame(json_projects)

        df.loc[df['exercise'] == '1', 'exercise'] = True
        df.loc[df['exercise'] == '0', 'exercise'] = False

        df.loc[df['obese'] == '1', 'obese'] = True
        df.loc[df['obese'] == '0', 'obese'] = False

        df.loc[df['alcoholUse'] == '1', 'alcoholUse'] = True
        df.loc[df['alcoholUse'] == '0', 'alcoholUse'] = False

        df.loc[df['tobaccoUse'] == '1', 'tobaccoUse'] = True
        df.loc[df['tobaccoUse'] == '0', 'tobaccoUse'] = False

        df.loc[df['sex'] == 'MALE', 'sex'] = 'Male'
        df.loc[df['sex'] == 'FEMALE', 'sex'] = 'Female'
        # print(df.head())
        # print(df.columns)
        return df
