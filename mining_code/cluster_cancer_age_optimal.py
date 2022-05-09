import pandas as pd
from kmodes.kmodes import KModes
import matplotlib.pyplot as plt

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
        df = df[['diagnosis', 'age_incidence']]
        df.age_incidence = pd.to_numeric(df.age_incidence, errors='coerce')
        df['age_group'] = pd.cut(df['age_incidence'], [0, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                                 labels=['0-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90',
                                         '90-100'])
        df = df.drop('age_incidence', axis=1)
        # print(len(df))

        from sklearn import preprocessing
        le = preprocessing.LabelEncoder()
        df = df.apply(le.fit_transform)
        print(df.head())

        cost = []
        K = range(1, 5)
        # TO FIND OPTIMAL CLUSTERS BASED ON COST
        for num_clusters in list(K):
            kmode = KModes(n_clusters=num_clusters, init="random", n_init=5, verbose=1)
            kmode.fit_predict(df)
            cost.append(kmode.cost_)
        plt.plot(K, cost, 'bx-')
        plt.xlabel('No. of clusters')
        plt.ylabel('Cost')
        plt.title('Elbow Method For Optimal k')
        plt.show()


CancerTreatmentCluster.prep_cluster()
