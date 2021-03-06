from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from common.general import iterable


def identify_categorical(train_df, verbose=True):
    # Identify and characterize categorical variables
    s = (train_df.dtypes == 'object')
    categorical_cols = list(s[s].index)
    verbose and print("Categorical columns:", categorical_cols)

    # Get number of unique entries in each column with categorical data
    categorical_nunique = list(map(lambda col: train_df[col].nunique(), categorical_cols))
    d = dict(zip(categorical_cols, categorical_nunique))
    verbose and print("Unique values:", sorted(d.items(), key=lambda x: x[1]))

    return categorical_cols


# Deal with missing data fields (impute)
# Drop columns (not desired)
# Impute with Mean, 0 or mode
# Impute with Mean and add column indicating imputed rows  for col in cols_with_missing:
#     X_train_plus[col + '_was_missing'] = X_train_plus[col].isnull()
#     X_valid_plus[col + '_was_missing'] = X_valid_plus[col].isnull()
def create_numerical_transformer(imputer_strategy="constant", imputer_fill_value=None):
    # Preprocessing for numerical data
    numerical_transformer = SimpleImputer(strategy=imputer_strategy, fill_value=imputer_fill_value)
    return numerical_transformer


# Types of encoding:  drop columns, onehot encoding (<15 values), countencoder, targetencoder,
# boostencoding, labelencoding()
def create_categorical_transformer(impute_strategy="most_frequent"):
    # Preprocessing for categorical data
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy=impute_strategy)),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False))
    ])
    return categorical_transformer


def create_feature_preprocessor(numerical_transformer, numerical_cols, categorical_transformer, categorical_cols):
    # Bundle preprocessing for numerical and categorical data
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])
    return preprocessor


def get_transformer_feature_names(columnTransformer):

    output_features = []
    for name, pipe, features in columnTransformer.transformers_:
        if name!='remainder':
            if not iterable(pipe):
                pipe = [pipe]

            for i in pipe:
                if hasattr(i, 'categories'):
                    trans_features = list(i.get_feature_names(features))
                else:
                    trans_features = list(features)

            output_features = output_features + trans_features

    return output_features
