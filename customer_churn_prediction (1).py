# -*- coding: utf-8 -*-
"""Customer churn prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dSlrxR-gMf_9VsbL9R7wVhDY97bitt5W

# Part 1: Data preprocessing

Dataset link: https://www.kaggle.com/adammaus/predicting-churn-for-bank-customers?select=Churn_Modelling.csv

## Importing the libraries and dataset
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dataset = pd.read_csv('/content/Churn_Modelling.csv')

"""## Data exploration"""

dataset.head()

dataset.shape

dataset.info()

dataset.select_dtypes(include='object').columns

len(dataset.select_dtypes(include='object').columns)

dataset.select_dtypes(include=['int64', 'float64']).columns

len(dataset.select_dtypes(include=['int64', 'float64']).columns)

# statistical summary
dataset.describe()

"""## Dealing with missing data"""

dataset.isnull().values.any()

dataset.isnull().values.sum()

"""## Encode the categorical data"""

dataset.select_dtypes(include='object').columns

dataset.head()

dataset = dataset.drop(columns=['RowNumber',	'CustomerId',	'Surname'])

dataset.head()

dataset.select_dtypes(include='object').columns

dataset['Geography'].unique()

dataset['Gender'].unique()

dataset.groupby('Geography').mean()

dataset.groupby('Gender').mean()

# one hot encoding
dataset = pd.get_dummies(data=dataset, drop_first=True)

dataset.head()

"""## Countplot"""

sns.countplot(dataset['Exited'])
plt.plot

# Staying with the bank
(dataset.Exited == 0).sum()

# Exited customers
(dataset.Exited == 1).sum()

"""## Correlation matrix and heatmap"""

dataset_2 = dataset.drop(columns='Exited')

dataset_2.corrwith(dataset['Exited']).plot.bar(
    figsize=(16,9), title='Correlated with Exited', rot=45, grid=True
)

corr = dataset.corr()

plt.figure(figsize=(16,9))
sns.heatmap(corr, annot=True)

"""## Splitting the dataset"""

dataset.head()

# independent / Matrix of feature
x = dataset.drop(columns='Exited')

# target/dependent variable
y = dataset['Exited']

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

x_train.shape

x_test.shape

y_train.shape

y_test.shape

"""## Feature scaling"""

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()

x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

x_train

x_test

"""# Part 2: Building the model

## 1) Logistic regression
"""

from sklearn.linear_model import LogisticRegression
classifier_lr = LogisticRegression(random_state=0)
classifier_lr.fit(x_train, y_train)

y_pred = classifier_lr.predict(x_test)

from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)

results = pd.DataFrame([['Logistic regression', acc, f1, prec, rec]],
                       columns=['Model', 'Accuracy', 'F1', 'precision', 'Recall'])

results

cm = confusion_matrix(y_test, y_pred)
print(cm)

"""### Cross validation"""

from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator=classifier_lr, X=x_train, y=y_train, cv=10)

print("Accuracy is {:.2f} %".format(accuracies.mean()*100))
print("Standard Deviation is {:.2f} %".format(accuracies.std()*100))

"""## 2) Random forest"""

from sklearn.ensemble import RandomForestClassifier
classifier_rf = RandomForestClassifier(random_state=0)
classifier_rf.fit(x_train, y_train)

y_pred = classifier_rf.predict(x_test)

from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)

model_results = pd.DataFrame([['Random forest', acc, f1, prec, rec]],
                       columns=['Model', 'Accuracy', 'F1', 'precision', 'Recall'])

results = results.append(model_results, ignore_index=True)

results

cm = confusion_matrix(y_test, y_pred)
print(cm)

"""### Cross validation"""

from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator=classifier_rf, X=x_train, y=y_train, cv=10)

print("Accuracy is {:.2f} %".format(accuracies.mean()*100))
print("Standard Deviation is {:.2f} %".format(accuracies.std()*100))

"""## 3) XGBoost

Documentation:https://xgboost.readthedocs.io/en/latest/

XGBoost is an implementation of gradient boosted decision trees designed for speed and performance that is dominative competitive machine learning
"""

from xgboost import XGBClassifier
classifier_xgb = XGBClassifier()
classifier_xgb.fit(x_train, y_train)

y_pred = classifier_xgb.predict(x_test)

acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)

model_results = pd.DataFrame([['XGBoost classifier', acc, f1, prec, rec]],
                       columns=['Model', 'Accuracy', 'F1', 'precision', 'Recall'])

results = results.append(model_results, ignore_index=True)
results

cm = confusion_matrix(y_test, y_pred)
print(cm)

"""### Cross validation"""

from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator=classifier_xgb, X=x_train, y=y_train, cv=10)

print("Accuracy is {:.2f} %".format(accuracies.mean()*100))
print("Standard Deviation is {:.2f} %".format(accuracies.std()*100))

"""# Part 3: Randomized Search to find the best parameters (XGBoost Classifier)"""

from sklearn.model_selection import RandomizedSearchCV

parameters = {
    'learning_rate':[0.05, 0.1, 0.15, 0.20, 0.25, 0.30],
    'max_depth':[3, 4, 5 , 6, 7, 8 , 10, 12, 15],
    'min_child_weight':[1, 3, 5, 7],
    'gamma':[0.0, 0.1, 0.2, 0.3, 0.4],
    'colsample_bytree':[0.3, 0.4, 0.5, 0.7]    
}

parameters

randomized_search = RandomizedSearchCV(estimator=classifier_xgb, param_distributions=parameters, n_iter=5,
                                       n_jobs=-1, scoring='r2', cv=5, verbose=3)

randomized_search.fit(x_train, y_train)

randomized_search.best_estimator_

randomized_search.best_params_

randomized_search.best_score_

"""# Part 4: Final Model (XGBoost Classifier)"""

from xgboost import XGBClassifier
classifier = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
              colsample_bynode=1, colsample_bytree=0.7, gamma=0.1,
              learning_rate=0.1, max_delta_step=0, max_depth=4,
              min_child_weight=1, missing=None, n_estimators=100, n_jobs=1,
              nthread=None, objective='binary:logistic', random_state=0,
              reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
              silent=None, subsample=1, verbosity=1)
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

model_results = pd.DataFrame([['Final XGBoost', acc, f1, prec, rec]],
               columns = ['Model', 'Accuracy', 'F1', 'precision', 'Recall'])


results = results.append(model_results, ignore_index = True)
results

cm = confusion_matrix(y_test, y_pred)
print(cm)

"""## Cross validation"""

from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator=classifier, X=x_train, y=y_train, cv=10)

print("Accuracy is {:.2f} %".format(accuracies.mean()*100))
print("Standard Deviation is {:.2f} %".format(accuracies.std()*100))

"""# Part 5: Predicting a single observation"""

dataset.head()

single_obs = [[625,	45,	5,	12500.01,	1,	0,	1,	101348.88, 0,	0, 1]]

single_obs

classifier.predict(sc.transform(single_obs))

"""##Bayesian Network prediction"""

!pip install pgmpy

from pgmpy.models import BayesianModel

dataset.head()

model = BayesianModel([("Age","Balance"),("Age","IsActiveMember"),("EstimatedSalary","Exited")])
model.fit(dataset)

from pgmpy.inference import VariableElimination
infer = VariableElimination(model)
q = infer.query(variables = ["Exited"],evidence={"Age":20,"Balance":159660.80})

print(q)

