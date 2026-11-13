
import pandas as pd
import numpy as np

data = r"C:\Users\gonug\Downloads\online_retail_II.xlsx"
df1 = pd.read_excel(data,sheet_name = "Year 2009-2010")


df2 = pd.read_excel(data,sheet_name= "Year 2010-2011")


# Combine both sheets
ecommerce = pd.concat(
    [df1, df2],
    ignore_index=True
)

print("Original Shape:", ecommerce.shape)

# Keep an untouched copy
raw_data = ecommerce.copy()




print("Duplicates:", ecommerce.duplicated().sum())

ecommerce = ecommerce.drop_duplicates().copy()

print("After Duplicate Removal:", ecommerce.shape)




ecommerce.columns = ecommerce.columns.str.strip()



# Invoice as string
ecommerce["Invoice"] = (
    ecommerce["Invoice"].astype("string").str.strip()
)

# StockCode as string
ecommerce["StockCode"] = (
    ecommerce["StockCode"].astype("string").str.strip()
)

# Description
ecommerce["Description"] = (
    ecommerce["Description"].astype("string").str.strip()
)

# Country
ecommerce["Country"] = (
    ecommerce["Country"].astype("string").str.strip().str.title()
)

# Convert date
ecommerce["InvoiceDate"] = pd.to_datetime(
    ecommerce["InvoiceDate"], errors="coerce"
)

# Convert numerical columns
ecommerce["Quantity"] = pd.to_numeric(
    ecommerce["Quantity"], errors="coerce"
)

ecommerce["Price"] = pd.to_numeric(
    ecommerce["Price"], errors="coerce"
)

ecommerce["Customer ID"] = pd.to_numeric(
    ecommerce["Customer ID"], errors="coerce"
).astype("Int64")



print("Missing Values:")
print(ecommerce.isnull().sum())

# Keep missing Customer ID rows
# They are useful for sales analysis

# Fill missing product descriptions
ecommerce["Description"] = (
    ecommerce["Description"].fillna("Unknown Product")
)

# Remove rows missing essential transaction information
ecommerce = ecommerce.dropna(
    subset=[
        "Invoice",
        "StockCode",
        "InvoiceDate",
        "Quantity",
        "Price"
    ]
).copy()




cancel_mask = ecommerce["Invoice"].str.startswith(
    "C", na=False
)

cancel_record = ecommerce[cancel_mask].copy()

# Normal invoices
normal_record = ecommerce[~cancel_mask].copy()

print("Cancellation Records:", cancel_record.shape)
print("Normal Records:", normal_record.shape)


# Negative quantities indicate returned goods
returns_record = normal_record[
    normal_record["Quantity"] < 0
].copy()

# Positive quantity records
sales_record = normal_record[
    normal_record["Quantity"] > 0
].copy()

# Zero quantity records are not useful for sales
zero_quantity = normal_record[
    normal_record["Quantity"] == 0
].copy()

print("Returns:", returns_record.shape)
print("Positive Sales:", sales_record.shape)
print("Zero Quantity:", zero_quantity.shape)




# Identify invalid prices
invalid_price = sales_record[
    sales_record["Price"] <= 0
].copy()

# Keep only positive-price sales for revenue analysis
sales_record = sales_record[
    sales_record["Price"] > 0
].copy()




sales_record["Revenue"] = (
    sales_record["Quantity"] * sales_record["Price"]
)


returns_record["Return_Value"] = (
    returns_record["Quantity"].abs() *
    returns_record["Price"]
)



sales_record["Year"] = (
    sales_record["InvoiceDate"].dt.year
)

sales_record["Month"] = (
    sales_record["InvoiceDate"].dt.month
)

sales_record["Month_Name"] = (
    sales_record["InvoiceDate"].dt.strftime("%b")
)

sales_record["Quarter"] = (
    sales_record["InvoiceDate"].dt.quarter
)

sales_record["Day"] = (
    sales_record["InvoiceDate"].dt.day
)

sales_record["Weekday"] = (
    sales_record["InvoiceDate"].dt.day_name()
)




customer_data = sales_record.dropna(
    subset=["Customer ID"]
).copy()




print("\nFINAL DATA CHECK")

print("Sales Shape:", sales_record.shape)

print("Returns Shape:", returns_record.shape)

print("Cancellation Shape:", cancel_record.shape)

print("Missing Values:")
print(sales_record.isnull().sum())

print("Duplicates:")
print(sales_record.duplicated().sum())

print("Total Revenue:")
print(sales_record["Revenue"].sum())




sales_record.to_csv(
    "cleaned_sales_data.csv",
    index=False
)

returns_record.to_csv(
    "returns_data.csv",
    index=False
)

cancel_record.to_csv(
    "cancellation_data.csv",
    index=False
)

customer_data.to_csv(
    "customer_analysis_data.csv",
    index=False
)

