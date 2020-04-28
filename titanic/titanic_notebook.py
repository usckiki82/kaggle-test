import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Setup project variables and paths
PROJECT_NAME = "titanic"

print(f"{PROJECT_NAME.upper()} KAGGLE COMPETITION")

main_path = os.path.join(os.getcwd(), "..")
data_path = os.path.join(main_path, "data", PROJECT_NAME)
output_path = os.path.join(main_path, "output", PROJECT_NAME)

if not os.path.isdir(output_path):
    print("Making output folder")
    os.mkdir(output_path)

# Load up data
print("Loading data ...")
gender_submission = pd.read_csv(os.path.join(data_path, "gender_submission.csv"))
submission_data = pd.read_csv(os.path.join(data_path, "test.csv"))
train = pd.read_csv(os.path.join(data_path, "train.csv"))

# Data information
women = train.loc[train.Sex == 'female']["Survived"]
rate_women = sum(women)/len(women)
print("% of women who survived:", rate_women)

men = train.loc[train.Sex == 'male']["Survived"]
rate_men = sum(men)/len(men)
print("% of men who survived:", rate_men)

features = ["Pclass", "Sex", "SibSp", "Parch"]
le_sex = LabelEncoder()
le_sex.fit(train["Sex"])
# print(list(le_sex.classes_))
train["Sex_Encoded"] = le_sex.transform(train["Sex"])

le_emb = LabelEncoder()
le_emb.fit(train["Embarked"].astype("str"))
# print(list(le_emb.classes_))
train["Embarked_Encoded"] = le_emb.transform(train["Embarked"].astype("str"))

sns.set(style="ticks", color_codes=True)
g_train = sns.pairplot(train, diag_kind="hist", hue="Survived")
plt.tight_layout()
plt.show()

# Split data into test train
test_ratio = 0.5
y = train["Survived"]
X = pd.get_dummies(train[features])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_ratio, random_state=42)

print("Train len:", len(X_train), "Test len:", len(X_test))

# Train model and performance
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
model.fit(X_train, y_train)
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

print("Train accuracy score:", accuracy_score(y_train, y_pred_train))
print("Test accuracy score:", accuracy_score(y_test, y_pred_test))

# Predict and Save Submission File
X_submission = pd.get_dummies(submission_data[features])
y_pred_submission = model.predict(X_submission)
output = pd.DataFrame({'PassengerId': submission_data.PassengerId, 'Survived': y_pred_submission})

g_output = sns.pairplot(output, diag_kind="hist", hue="Survived")
plt.tight_layout()
plt.show()

output.to_csv(os.path.join(output_path, f'{PROJECT_NAME}_submission.csv'), index=False)
print("Your submission was successfully saved!", len(output))
