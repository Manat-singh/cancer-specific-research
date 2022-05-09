import pandas as pd
from kmodes.kmodes import KModes
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient

from process_cancer_data import CancerData
from process_patient_data import PatientProcess


class CancerTreatmentCluster:

    @staticmethod
    def prep_cluster():
        df_cancer = CancerData.get_cancer_data()
        df_patient = PatientProcess.get_patient_base_data()
        # print(df.head())
        # print(len(df_patient))
        df_cancer = df_cancer.drop_duplicates(subset=['pid'])
        # print(len(df_cancer))
        df = pd.merge(
            left=df_patient,
            right=df_cancer,
            on=['pid']
        )
        df.drop_duplicates(subset=['pid'])
        df = df[['diagnosis', 'age_incidence']]
        df.age_incidence = pd.to_numeric(df.age_incidence, errors='coerce')
        df['age_group'] = pd.cut(df['age_incidence'], [0, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            labels=['0-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100'])
        df = df.drop('age_incidence', axis=1)
        # print(len(df))
        df_copy = df.copy()

        from sklearn import preprocessing
        le = preprocessing.LabelEncoder()
        df = df.apply(le.fit_transform)
        print(df.head())

        # Clustering using k-modes algorithm
        x = df.reset_index().values
        k_modes = KModes(n_clusters=3, init="Huang", n_init=5, verbose=1)
        clusters = k_modes.fit_predict(df)

        cluster_df = pd.DataFrame(clusters)
        cluster_df.columns = ['cluster_predicted']
        df = df_copy.reset_index()
        combined_df = pd.concat([df, cluster_df], axis=1).reset_index()
        combined_df = combined_df.drop(['index', 'level_0'], axis=1)

        combined_df.to_excel("cancer_age_diagnosis.xlsx", index=False)

        client = MongoClient(port=27017)
        db = client.adtProject
        db.cancer_age_diagnosis.drop()
        db.cancer_age_diagnosis.insert_many(combined_df.to_dict(orient='records'))

        plt.subplots(figsize=(15, 5))
        sns.countplot(x=combined_df['age_group'], order=combined_df['age_group'].value_counts().index,
                      hue=combined_df['cluster_predicted'])
        plt.show()


CancerTreatmentCluster.prep_cluster()
