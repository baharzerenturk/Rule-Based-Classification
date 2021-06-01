#TASK-1:

#OUESTION-1: How can we read the csv file and show the general information of dataset?
df = pd.read_csv("../persona.csv")
df.shape
df.head()
df.tail()
df.info()
df.isnull().any()
df.columns

#OUESION-2: How many unique "SOURCE" in dataset? What are their frequencies?
df["SOURCE"].nunique()
print("Ratio:" ,(100 * df["SOURCE"].value_counts()) / len(df))

#3)How many unique "PRICE" in dataset?
df["PRICE"].nunique()

#QUESTION-4: How many sales were made from which "PRICE"?
df["PRICE"].value_counts()

#QUESTION-5: How many sales were made from which "COUNTRY"?
df["COUNTRY"].value_counts()

#QUESTION-6: How much was earned in total from sales by country?
df.groupby("COUNTRY").agg({"PRICE" : "sum"})

#QUESTION-7: What are the sales numbers by "SOURCE" types?
df.groupby("SOURCE")["PRICE"].count()
df.groupby("SOURCE").agg({"PRICE" : "count"})

#QUESTION-8: What are the "PRICE" averages by country?
df.groupby("COUNTRY").agg({"PRICE" : "mean"})

#9QUESTION-9: What are the "PRICE" averages by "SOURCE"?
df.groupby("SOURCE").agg({"PRICE" : "mean"})

#OUESTION-10: What are the averages of the "PRICE" in the "COUNTRY-SOURCE" distribution?
df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE" : "mean"})

#TASK-2:
#What are the total earnings in COUNTRY, SOURCE, SEX, AGE distribution?

df.groupby(["COUNTRY", "SOURCE", "AGE", "SEX"]).agg({"PRICE" : "sum"})

#TASK-3:
#Sort the output by PRICE.

agg_df = df.groupby(["COUNTRY", "SOURCE", "AGE", "SEX"]).agg({"PRICE" : "sum"}).sort_values(by = "PRICE", ascending= False)

#TASK-4:
#Convert the names in the index to the variable name.

agg_df = agg_df.reset_index()
agg_df.head()

#TASK-5:
#Convert age variable to categorical variable and add it to agg_df.

agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], bins = [0,19,24,31,41,70], labels = ["0-19", "20-24", "25-31", "32-41", "42-70"])
agg_df.head()

#TASK-6:
#Identify new level-based customers (personas).

#row[0]: COUNTRY
#row[1]: SOURCE
#row[3]: SEX
#row[5]: AGE

agg_df["customers_level_based"] = [row[0].upper()+"_"+row[1].upper()+"_"+row[3].upper()+"_"+str(row[5]) for row in agg_df.values]
agg_new_df = agg_df.groupby("customers_level_based").agg({"PRICE" : "mean"}).sort_values(by = "PRICE", ascending=False)

#TASK-7:
#Segment new customers (personas).

pd.qcut(agg_new_df["PRICE"], 4, labels = ["D", "C", "B", "A"])
agg_new_df["SEGMENT"] = pd.qcut(agg_new_df["PRICE"], 4, labels = ["D", "C", "B", "A"])
agg_new_df.head()

agg_list = ["mean", "max", "sum"]
def check_segment(dataframe, col_name, agg_col_name, agg_list):
    return dataframe.groupby(col_name).agg({agg_col_name : agg_list})

check_segment(agg_new_df, "SEGMENT", "PRICE", agg_list)

agg_new_df[agg_new_df["SEGMENT"] == "C"].describe().T

#TASK8:
#Categorize new customers according to their segments and estimate how much revenue they will generate.

new_user_1 = "TUR_ANDROID_FEMALE_32-41"
agg_df[agg_df["customers_level_based"] == new_user_1]["PRICE"]

new_user_2 = "FRA_IOS_FEMALE_32-41"
agg_df[agg_df["customers_level_based"] == new_user_2]["PRICE"]


#WITH USING FUNCTION
def price_prediction(dataframe, col_name, age, source, country, sex):
    if age >= 0 and age <= 19:
        age = "0-19"
    elif age >= 20 and age <= 24:
        age = "20-24",
    elif age >= 25 and age <= 31:
        age = "25-31"
    elif age >= 32 and age <= 41:
        age = "32-41"
    else:
        age = "42-70"
    statement = country.upper() + "_" + source.upper() + "_" + sex.upper() + "_" + age
    print(dataframe[dataframe[col_name] == statement]["PRICE"].to_string(index=False))


#The Turkish woman who is 33 years old and using Android:
price_prediction(agg_df, "customers_level_based", 33, "ANDROID", "TUR", "FEMALE")

#The French woman who is 35 years old and using IOS:
price_prediction(agg_df, "customers_level_based", 35, "IOS", "FRA", "FEMALE")