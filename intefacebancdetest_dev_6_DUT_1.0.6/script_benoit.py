import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from datetime import datetime

sns.set_style("darkgrid")

df = pd.read_csv("data_dut_2_2019-2-22-17-34-36.csv", sep=";", dtype={"Value": str})

df.Value = df.Value.apply(lambda x: float(x.replace(',', '.')))
df['label'] = KMeans(n_clusters=2, random_state=0).fit_predict(df.Value.values.reshape(-1, 1))
df['datetime'] = pd.to_datetime(df['date-time'], format='%Y-%m-%d %H:%M:%S.%f').astype(datetime)
    
mask_class0 = df.loc[df.label == 0, 'Value']-df.loc[df.label == 0, 'Value'].mean() <= (1*(df.loc[df.label == 0, 'Value'].std()))
mask_class1 = df.loc[df.label == 1, 'Value']-df.loc[df.label == 1, 'Value'].mean() <= (1*(df.loc[df.label == 1, 'Value'].std()))

min_class0 = df.loc[df.label == 0, 'Value'][mask_class0].min()
max_class0 = df.loc[df.label == 0, 'Value'][mask_class0].max()

min_class1 = df.loc[df.label == 1, 'Value'][mask_class1].min()
max_class1 = df.loc[df.label == 1, 'Value'][mask_class1].max()

print(min_class0)
print(max_class0)

print(min_class1)
print(max_class1)

