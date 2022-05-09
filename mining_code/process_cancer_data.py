from pymongo import MongoClient
import pandas as pd

from pyspark.sql.types import DoubleType


class CancerData:
    @staticmethod
    def get_cancer_data():
        client = MongoClient(port=27017)
        #print(client)
        db=client.adtProject
        coll = db.cancer
        #print(coll)
        sample=coll.find({}, {'_id': 0})
        #print(sample)
        json_projects = []
        for project in sample:
            json_projects.append(project)
        df = pd.DataFrame(json_projects)

        df.loc[df['treatment_type'] == '1', 'treatment_type'] = "Surgery"
        df.loc[df['treatment_type'] == '2', 'treatment_type'] = "Radiotherapy"
        df.loc[df['treatment_type'] == '3', 'treatment_type'] = "Chemotherapy"
        df.loc[df['treatment_type'] == '4', 'treatment_type'] = "Immunotherapy"
        df.loc[df['treatment_type'] == '5', 'treatment_type'] = "Normal Medication"
        df.loc[df['treatment_type'] == '6', 'treatment_type'] = "Hormonal"
        # print(df.head())
        # print(df.columns)
        return df

