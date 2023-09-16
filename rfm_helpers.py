# importing required libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


# overviewing dataframe for EDA/checking for observation after manipulations
def overview_df(dataframe, head=10):
    print(f"Shape: {dataframe.shape}")
    print("------------------------------------------------ Data Head ------------------------------------------------")
    print(dataframe.head(head))
    print("------------------------------------------------ Data Tail ------------------------------------------------")
    print(dataframe.tail())
    print("------------------------------ Data Types ------------------------------")
    print(dataframe.dtypes)
    print("---------------------------- Unique Values -----------------------------")
    print(dataframe.nunique())
    print("------------------------------ NaN Values ------------------------------")
    print(dataframe.isnull().sum())
    print("------------------------------ Describe  -------------------------------")
    print(dataframe.describe([0.01, 0.1, 0.25, 0.50, 0.75, 0.9, 0.95, 0.99]))


# data pre-processing
def preprocess_data(dataframe):
    # remove canceled transaction invoices
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    print("Canceled transaction invoices have been removed.")

    # filter invalid rows with negative price
    dataframe = dataframe[dataframe["Price"] >= 0]
    print("Invalid price values have been removed.")

    # filter invalid rows with negative quantity
    dataframe = dataframe[(dataframe["Quantity"] > 0)]
    print("Void transactions have been removed.")

    # drop rows with missing values
    dataframe.dropna(inplace=True)
    print("Rows without information have been dropped.")
    print("Preprocessing completed.")

    return dataframe


def clean_invalid_codes(dataframe):
    # remove rows with stockcodes have ambiguous description
    dataframe = dataframe[dataframe["StockCode"] != "M"]
    print("Stock code of ambiguous description have been removed.")

    # find, document and remove invalid stockcodes
    invalid_codes = dataframe[dataframe["StockCode"].astype(str).str.contains(r"[a-zA-Z]{3,}")]["StockCode"].unique().tolist()

    print("#####################################################")
    invalid_df = dataframe[dataframe["StockCode"].isin(invalid_codes)].groupby(["StockCode"]).agg({"Invoice": "nunique",
                                                                                                   "Quantity": "sum",
                                                                                                   "Price": "sum",
                                                                                                   "Customer ID": "nunique"})
    print(invalid_df)
    dataframe = dataframe[~dataframe["StockCode"].isin(invalid_codes)].reset_index(drop=True)
    print("#####################################################")

    print(f"Invalid stock codes have been removed: {invalid_codes}")

    return dataframe


# returning dataframe with selected country column
def select_country(dataframe, country):
    country_df = dataframe.loc[dataframe["Country"] == country]
    return country_df


# checking missing (null) values
def missing_values(dataframe, na_name=False):
    # find columns with missing values
    na_columns = [col for col in dataframe.columns
                  if dataframe[col].isnull().sum() > 0]

    # calculate missing value statistics
    n_missing = dataframe[na_columns].isnull().sum().sort_values(ascending=False)
    ratio = (n_missing / dataframe.shape[0] * 100).sort_values(ascending=False)

    # create and print a DataFrame to display missing value information
    missing_df = pd.concat([n_missing, np.round(ratio, 2)],
                           axis=1, keys=['n_missing', 'ratio'])
    print(missing_df)

    # return columns with missing values if na_name is True
    if na_name:
        return na_columns


# specification of outlier thresholds with IQR method
def outlier_thresholds(dataframe, variable, q1=0.05, q3=0.95):
    quantile1 = dataframe[variable].quantile(q1)
    quantile3 = dataframe[variable].quantile(q3)
    interquantile_range = quantile3 - quantile1
    up_limit = quantile3 + 1.5 * interquantile_range
    low_limit = quantile1 - 1.5 * interquantile_range
    return low_limit, up_limit


# observation of outlier values
def check_outlier(dataframe, column):
    low_limit, up_limit = outlier_thresholds(dataframe, column)
    if dataframe[(dataframe[column] > up_limit) | (dataframe[column] < low_limit)].any(axis=None):
        return True

    else:
        return False


# solution for outliers with replacement
def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    # if related value is lower than low_limit then impute low_limit
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    # if related value is greater than up_limit then impute up_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


# standard scaler for feature scaling
def standard_scaler(dataframe, column):
    scaler = StandardScaler()
    scaled_df = scaler.fit_transform(dataframe[column])
    return scaled_df
