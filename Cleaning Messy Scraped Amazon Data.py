# Import useful Libraries
import pandas as pd
import numpy as np
import seaborn as sns
import plotly as py

#import raw data file
Data = pd.read_csv(r"C:\Users\omarm\Documents\Career Essentials & Job Apps\Guided Projects with Business Problems-or-Requirements\Amazon_ecommerce_sample.csv")
Data


#CLEANING

Data1 = Data.drop(columns = ["uniq_id","customers_who_bought_this_item_also_bought","description","product_information","product_description","items_customers_buy_after_viewing_this_item","customer_questions_and_answers","sellers","number_of_answered_questions","customer_reviews"])
Data1

Data2 = Data1.rename(columns = {"product_name":"Product Name", "manufacturer":"Manufacturer","number_available_in_stock":"Available Stock","number_of_reviews":"Number of Reviews","average_review_rating":"Average Rating (Out of 5)", "price":"Price (£)", "amazon_category_and_sub_category": "Category"})
Data2["Price (£)"] = Data2["Price (£)"].str.replace("£","")
Data2["Average Rating (Out of 5)"] = Data2["Average Rating (Out of 5)"].str.replace(" out of 5 stars","")
Data2

Data2["Available Stock"] = Data2["Available Stock"].str.replace("new","")

# Replacing NaNs with 0 for stocks and reviews
Data2["Available Stock"] = Data2["Available Stock"].fillna(0)
Data2["Number of Reviews"] = Data2["Number of Reviews"].fillna(0)
Data2

Data2["Available Stock"].isnull().sum()
Data2["Number of Reviews"].isnull().sum()

Data2[["Category","Subcategory","Subcategory2","Subcategory3","Subcategory4"]] = Data2["Category"].str.split(">", expand = True)
Data2

Data2.info()

# We will drop Subcategory 2,3 and 4 as we are only interested in Category and Subcategory,
# In addition to this, most of them only contain category and subcategory information. 
#We will also drop Null values from prices and ratings since we are only interested in products with actual prices and ratings.

Data2 = Data2.drop(columns = ["Subcategory2","Subcategory3","Subcategory4"])
Data3 = Data2.dropna(subset = ["Price (£)","Average Rating (Out of 5)"])
Data3

#Reset index due to the drop of rows with NaNs
Data3.reset_index(drop=True, inplace = True)
Data3

#Confirming NaN dropped from prices and ratings(by finding the sum of NaNs)
Data3[["Price (£)","Average Rating (Out of 5)"]].isna().sum()
Data3.info()

# found out ranges of prices in the price column
# I will take the minimum by expanding using delimiter and then dropping max price]

# I also found out that the prices listed incorrectly contain commas. 
# My choice is to remove them and see if it will have any impact on the data

# Also, I will remove non-numeric characters from the Available Stock and Number of Reviews and fill NaNs again with zero in case they arise

Data3[["Price (£)", "Max Price"]] = Data3["Price (£)"].str.split("-", expand = True)
Data3.drop(columns = ["Max Price"])

Data3 = Data3[~Data3["Price (£)"].str.contains(',')]
Data3.info()

Data3["Available Stock"] = Data3["Available Stock"].str.replace(r'\D', '')
Data3["Number of Reviews"] = Data3["Number of Reviews"].str.replace(r'\D', '')
Data3["Available Stock"].fillna(0, inplace=True)
Data3["Number of Reviews"].fillna(0, inplace=True)

# Here, I convert data types to make it easy to work with the different data types
Data3["Price (£)"] = Data3["Price (£)"].astype('float')
Data3["Average Rating (Out of 5)"] = Data3["Average Rating (Out of 5)"].astype('float')
Data3["Available Stock"] = Data3["Available Stock"].astype('int')
Data3["Number of Reviews"] = Data3["Number of Reviews"].astype('int')

Data3.dtypes

# Data is ready for use! I converted the NaNs in the Number of Reviews and Available Stock to zero because I believe we can use them to find interesting information from the data, such as how products with NaN in available stock (i.e., zero stock) vary with the customer rating, etc.
# An interesting hypothesis to test, in the case that NaN is replaced with 0, could be that products with NaNs (zero) in stock are likely to be products with high customer ratings because it could signify that they are products loved by customers and thus are sold out.
# I will export the cleaned data to Tableau as a CSV file, ready to create a dashboard that will answer a few business questions!

Cleaned = Data3.to_csv(r"C:\Users\omarm\Documents\Career Essentials & Job Apps\Guided Projects with Business Problems-or-Requirements\Amazon.csv", index = False)

