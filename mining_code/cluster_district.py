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
        df = df[['diagnosis', 'district']]
        # print(len(df))
        df_copy = df.copy()

        from sklearn import preprocessing
        le = preprocessing.LabelEncoder()
        df = df.apply(le.fit_transform)
        print(df.head())

        # Clustering using k-modes algorithm
        # x = df.reset_index().values
        k_modes = KModes(n_clusters=3, init="Huang", n_init=5, verbose=1)
        clusters = k_modes.fit_predict(df)
        # # insert cluster number in the dataset
        cluster_df = pd.DataFrame(clusters)
        cluster_df.columns = ['cluster_predicted']
        df = df_copy.reset_index()
        combined_df = pd.concat([df, cluster_df], axis=1).reset_index()
        combined_df = combined_df.drop(['index', 'level_0'], axis=1)
        # cluster_0 = combinedDf[combinedDf['cluster_predicted'] == 0]
        # cluster_1 = combinedDf[combinedDf['cluster_predicted'] == 1]

        combined_df.to_excel("cancer_district_diagnosis.xlsx", index=False)

        client = MongoClient(port=27017)
        db = client.adtProject
        db.cancer_district_diagnosis.drop()
        db.cancer_district_diagnosis.insert_many(combined_df.to_dict(orient='records'))

        plt.subplots(figsize=(15, 5))
        sns.countplot(x=combined_df['district'], order=combined_df['district'].value_counts().index,
                      hue=combined_df['cluster_predicted'])
        plt.show()
        # sns.catplot(x='diagnosis', y='district', data=combined_df)


CancerTreatmentCluster.prep_cluster()
