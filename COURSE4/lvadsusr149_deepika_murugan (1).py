# -*- coding: utf-8 -*-
"""LVADSUSR149_DEEPIKA MURUGAN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DkmaSxMyU7_2Ymbujw0dgSKCSeRXADom
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
# import statsmodels.api as sm

from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()

from sklearn.metrics import r2_score,mean_squared_error
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix

df=pd.read_csv('/content/sample_data/expenses.csv')
df.head(10)

#handling missing value
df.isnull().sum()

imputer=KNNImputer()
df['bmi']=imputer.fit_transform(df[['bmi']])

#checking for outliers in data
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns

# Create a box plot for each numerical column
for column in numerical_columns:
    plt.figure(figsize=(10, 6))  # Set the figure size for better readability
    sns.boxplot(x=df[column])
    plt.title(f'Box Plot of {column}')
    plt.xlabel(column)
    plt.show()

#managing box plots
q1=df['bmi'].quantile(0.25)
q3=df['bmi'].quantile(0.75)
iqr=q3-q1
lower=q1-1.5*iqr
upper=q3+1.5*iqr

new_df=df.loc[(df['bmi']>lower) & (df['bmi']<upper)]

new_df

#encode categorical data
for i in new_df.columns:
  if new_df[i].dtype==np.number:
    continue
  new_df[i]=label_encoder.fit_transform(new_df[i])

new_df

#feature selection
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
# Compute the correlation matrix for numerical variables
correlation_matrix = df[numerical_columns].corr()
print("Correlation matrix:\n", correlation_matrix)

x=new_df.drop('charges',axis='columns')
x=StandardScaler().fit_transform(x)

#data splitting
y=new_df['charges']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=20)
model=LinearRegression()
model.fit(x_train,y_train)

y_pred=model.predict(x_test)
y_pred

#Model evaluation
mse = mean_squared_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred,squared=False)
r2_s = r2_score(y_test, y_pred)
print("r2score:",r2_s)
print("mse",mse)
print("rmse",rmse)