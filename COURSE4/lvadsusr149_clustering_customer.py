# -*- coding: utf-8 -*-
"""LVADSUSR149-CLUSTERING-CUSTOMER.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JHoSr9RvW1HTR43am1GVYNe_hbVQMlRq
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
# import statsmodels.api as sm

import warnings
warnings.filterwarnings("ignore")

from sklearn.preprocessing import LabelEncoder,MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.impute import KNNImputer
label_encoder = LabelEncoder()
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

df=pd.read_csv('/content/sample_data/customer_segmentation.csv')
df.head(10)

df.info()

df.isnull().sum()

#handling null values
impute=KNNImputer()
for i in df.select_dtypes(include='number').columns:
  df[i]=impute.fit_transform(df[[i]])
df.isnull().sum()

df.duplicated().sum()

#identify the outliers
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns

# Create a box plot for each numerical column
for column in numerical_columns:
    plt.figure(figsize=(10, 6))  # Set the figure size for better readability
    sns.boxplot(x=df[column])
    plt.title(f'Box Plot of {column}')
    plt.xlabel(column)
    plt.show()



numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
# Compute the correlation matrix for numerical variables
correlation_matrix = df[numerical_columns].corr()
print("Correlation matrix:\n", correlation_matrix)

plt.figure(figsize=(20, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Heatmap of Correlation Matrix')
plt.show()

#handling outliers
#handling outliers
for columns in df.select_dtypes(include="number"):
  q1=df[columns].quantile(0.25)
  q3=df[columns].quantile(0.75)
  iqr=q3-q1
  lower=q1-1.5*iqr
  upper=q3+1.5*iqr
  new_df=df.loc[(df[columns]<upper)&(df[columns]>lower)]

#scaling
scaler = MinMaxScaler()
for column in df.select_dtypes(include=['float64','int64']):
  df[column] = scaler.fit_transform(df[[column]])

df.describe()

df.info()

#finding elbow
k_range = range(1,10)
sse = []
for k in k_range:
  km = KMeans(n_clusters=k)
  x=df.drop(columns=['ID','Education','Year_Birth','Marital_Status','Dt_Customer','Z_CostContact','Z_Revenue','AcceptedCmp2','Response','Complain','AcceptedCmp3','Recency'])
  km.fit(x)
  sse.append(km.inertia_)
plt.xlabel('Clusters')
plt.ylabel('SSE value')
plt.plot(k_range,sse,marker='.')

df.head(4)

km=KMeans(n_clusters=2)
y_pred = km.fit_predict(x)
df['cluster'] = y_pred
df1 = df[df.cluster == 0]
df2 = df[df.cluster == 1]
# df3 = df[df.cluster == 2]
# df4 = df[df.cluster == 3]
# df5 = df[df.cluster == 4]
# df6 = df[df.cluster == 5]
plt.scatter(df1.Income,df1['NumStorePurchases'],color='green')
plt.scatter(df2.Income,df2['NumStorePurchases'],color='blue')
# plt.scatter(df3.Income,df3['NumStorePurchases'],color='black')
# plt.scatter(df4.Income,df4['NumStorePurchases'],color='purple')
# plt.scatter(df5.Age,df5['Annual Income (k$)'],color='orange')
# plt.scatter(df6.Age,df6['Annual Income (k$)'],color='yellow')
plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='red',marker='*',label='centroid')
plt.xlabel('Age')
plt.ylabel('Annual income')
plt.legend()

silhouette_score(x, y_pred)