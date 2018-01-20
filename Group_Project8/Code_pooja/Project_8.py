
# coding: utf-8

# In[1]:


# Dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
plotly.offline.init_notebook_mode()


# In[2]:


# Save path to data set in a variable
census_tract_data_file = "Resources/2015_census_tract_data.csv"


# In[3]:


# Use Pandas to read data
census_df = pd.read_csv(census_tract_data_file, encoding = "latin-1")
census_df.head()


# In[4]:


census_CA_df = census_df.loc[census_df["State"]=="California"].copy()
census_CA_df.head()


# In[5]:


#setting the index of california dataframe to start from zero
census_CA_df= census_CA_df.reset_index(drop = True)


# In[6]:


# Export file as a CSV, without the Pandas index, but with the header
census_CA_df.to_csv("Output/census_CA.csv", encoding = "latin-1", index=False, header=True)


# In[7]:


counties = census_CA_df["County"].unique()
counties


# In[8]:


census_groupby_county_CA_df = census_CA_df.groupby(["County","State"], as_index= False).sum()
census_groupby_county_CA_df.head()


# In[9]:


#Fixing mean column for income
No_of_censusTract_grouped = census_CA_df.groupby(["County"], as_index= False).count()
No_of_censusTract = No_of_censusTract_grouped["CensusTract"]
No_of_censusTract
census_groupby_county_CA_df["Income"]= round(census_groupby_county_CA_df["Income"]/No_of_censusTract, 0)
#census_groupby_county_CA_df["Income"]


# In[10]:


# Export file as a CSV, without the Pandas index, but with the header
census_groupby_county_CA_df.to_csv("Output/census_groupby_county_CA.csv", encoding = "latin-1", index=False, header=True)


# In[11]:


def top_highest(df,col,top = 10):
    list_of_top_ten = df.sort_values(col, ascending=False).head(top)
    return list_of_top_ten


# In[12]:


#census_groupby_county_CA_df["County"] = census_groupby_county_CA_df.loc[0]
#census_groupby_county_CA_df


# In[13]:


#What are some counties in california with top 5 highest population
high_pop = top_highest(census_groupby_county_CA_df, "TotalPop", 5)
counties_high_population = high_pop[["County", "TotalPop"]]
print(counties_high_population)


# In[14]:


#Cleaning data if there is any NA in Men or Women column
#Add this part later on - write function/s to check and replace NA and blank values with zero
#census_groupby_county_CA_df["Women"]
#pd.isnull(census_groupby_county_CA_df["Women"])
#pd.isnull(census_groupby_county_CA_df["Men"])


# In[15]:


len(census_groupby_county_CA_df["Women"])
#census_groupby_county_CA_df["Men"].head()


# In[16]:


census_groupby_county_CA_df["Men"].loc[57]


# In[17]:


census_groupby_county_CA_df["Women"].loc[57]


# In[18]:


Ratio = census_groupby_county_CA_df["Women"].loc[57]/census_groupby_county_CA_df["Men"].loc[57]
Ratio


# In[19]:


FemaleToMaleRatio= []


# In[20]:


#division involved so if it is divided by zero, making it divided by one to avoid INF result
#Adding a new column to dataframe with female to male info
for i in range (0, len(census_groupby_county_CA_df["Men"]-1)):
    if(census_CA_df["Men"].loc[i] ==0):
        Ratio = census_groupby_county_CA_df["Women"].loc[i]/1
    else:
        Ratio = census_groupby_county_CA_df["Women"].loc[i]/census_groupby_county_CA_df["Men"].loc[i]
    #increment the index of loop
    i = i+1
    #append to FemaleToMaleRatio list column
    FemaleToMaleRatio.append(Ratio)
#FemaleToMaleRatio
census_groupby_county_CA_df["FemaleToMaleRatio"] = FemaleToMaleRatio


# In[21]:


#what are some counties with highest female/male ratio
#FemaleToMaleRatio = []
high_female_to_male = top_highest(census_groupby_county_CA_df, "FemaleToMaleRatio", 5)
counties_high_female_to_male = high_female_to_male[["County", "FemaleToMaleRatio"]]
print(counties_high_female_to_male)


# In[22]:


# Export file as a CSV, without the Pandas index, but with the header
census_groupby_county_CA_df.to_csv("Output/census_groupby_county_CA.csv", encoding = "latin-1", index=False, header=True)


# In[23]:


source = census_groupby_county_CA_df["FemaleToMaleRatio"]
source


# In[24]:


#california population divided among counties and visualized as a bar chart
Pop = census_groupby_county_CA_df["TotalPop"]/1000000
x_axis = np.arange(58)
tick_locations = [value for value in x_axis]
source = census_groupby_county_CA_df["County"]
plt.figure(figsize=(20,10))
bar1 = plt.bar(x_axis, Pop, width = .5, align='center', alpha = 1, color = 'b')
plt.xticks(x_axis, source, rotation = 'vertical')
plt.ylabel('Population in million')
plt.title('Populatoion of california spread in counties')
plt.xlim(-1, len(x_axis))
plt.ylim(0, max(Pop)+0.1)
plt.grid()
#fig = plt.figure(1, [40, 40])
#fig.autofmt_xdate()
plt.tight_layout()


# In[25]:


# Saves an image of our chart so that we can view it in a folder
plt.savefig("Output_graphs/Pop_County_Bar.png")
plt.show()


# In[26]:


#california population divided among counties and visualized as a bar chart - Taking LA out
i = census_groupby_county_CA_df[(census_groupby_county_CA_df.County == 'Los Angeles')].index
#i
census_groupby_county_CA_Without_LA_df = census_groupby_county_CA_df.drop(i)
census_groupby_county_CA_Without_LA_df.tail()
# Export file as a CSV, without the Pandas index, but with the header
census_groupby_county_CA_Without_LA_df.to_csv("Output/census_groupby_county_CA_without_LA.csv", encoding = "latin-1", index=False, header=True)


# In[27]:


#california population divided among counties and visualized as a bar chart - Taking LA out
Pop_without_LA = census_groupby_county_CA_Without_LA_df["TotalPop"]/1000000
x_axis = np.arange(57)
tick_locations = [value for value in x_axis]
source = census_groupby_county_CA_Without_LA_df["County"]
plt.figure(figsize=(20,10))
bar2 = plt.bar(x_axis, Pop_without_LA, width = .5, align='center', alpha = 0.5, color = 'r')
plt.xticks(x_axis, source, rotation = 'vertical')
plt.ylabel('Population in million_barring LA')
plt.title('Population of california spread in counties except LA')
plt.xlim(-1, len(x_axis))
plt.ylim(0, max(Pop_without_LA)+0.1)
plt.grid()
#fig = plt.figure(1, [40, 40])
#fig.autofmt_xdate()
#plt.tight_layout()


# In[28]:


# Saves an image of our chart so that we can view it in a folder - Taking LA out
plt.savefig("Output_graphs/Pop_County_Bar_without LA.png")
plt.show()


# In[29]:


#What is Female to male ratio across counties and visualized as a bar chart
x_axis = np.arange(58)
tick_locations = [value+0.4 for value in x_axis]
source = census_groupby_county_CA_df["FemaleToMaleRatio"]
plt.figure(figsize=(20,2))
bar1 = plt.bar(x_axis, source, width = .5, align='center', alpha = 1, color = 'y')
plt.xticks(tick_locations, census_groupby_county_CA_df["County"], rotation="vertical")
plt.ylabel('Female to male ratio')
plt.title('Female to male ratio across counties in California')
plt.xlim(-1,60)
plt.ylim(0, 1.1)
plt.grid()
#fig = plt.figure(1, [1.5, 10])
#fig.autofmt_xdate()
#plt.tight_layout()


# In[30]:


# Saves an image of our chart so that we can view it in a folder
plt.savefig("Output_graphs/FemaletoMale_County_Bar.png")
plt.show()


# In[31]:


#how does race spread look like across california
#Hispanic	White	Black	Native	Asian	Pacific
total_population_CA = census_groupby_county_CA_df["TotalPop"].sum()
#total_population_CA
total_Hispanic = int(census_groupby_county_CA_df["Hispanic"].sum())
total_Hispanic
total_White = int(census_groupby_county_CA_df["White"].sum())
total_White
total_Black = int(census_groupby_county_CA_df["Black"].sum())
total_Black
total_Native = int(census_groupby_county_CA_df["Native"].sum())
total_Native
total_Asian = int(census_groupby_county_CA_df["Asian"].sum())
total_Asian
total_Pacific = int(census_groupby_county_CA_df["Pacific"].sum())
total_Pacific

race_spread = [total_Hispanic, total_Pacific, total_White, total_Asian, total_Black, total_Native]


# In[32]:


#Creating a pie chart showing racial spread of california
colors = ["coral", "black", "purple", "lightgreen", "yellow", "lightskyblue"]
labels = ["Hispanic represented in Coral", "Pacific represented in Black", "White represented in Purple", "Asian represented in Green", "Black represented in yellow", "Native represented in Skyblue"]
patches = plt.pie(race_spread, colors = colors, labels = labels, shadow = True, autopct='%1.2f%%')


# In[33]:


# Saves an image of our chart so that we can view it in a folder
plt.title("Diversity spread of California")
plt.savefig("Output_graphs/Diversity_CA.png")
plt.show()


# In[34]:


#Counties with highest income levels
high_income = top_highest(census_groupby_county_CA_df, "Income", 5)
counties_high_income = high_income[["County", "Income"]]
print(counties_high_income)


# In[35]:


range_income_thousands= [min(census_groupby_county_CA_df["Income"])/1000, 
                         max(census_groupby_county_CA_df["Income"])/1000]
range_income_thousands


# In[36]:


#A line graph of Income spread across counties in California
x_axis = np.arange(0,58)
income_thousands = census_groupby_county_CA_df["Income"]/1000
income_thousands
tick_locations = [value+0.4 for value in x_axis]
source = census_groupby_county_CA_df["County"]
plt.figure(figsize=(20,10))
plt.xticks(x_axis, source, rotation = 'vertical')
income_spread = plt.plot(x_axis, income_thousands, marker="+",color="green", linewidth=2.5, label="Income in millions")

# Create labels for the X and Y axis
plt.xlabel("Counties")
plt.ylabel("Mean Income in thousands")

# Saves an image of our chart so that we can view it in a folder
plt.title("Income spread of California")
plt.grid()
plt.savefig("Output_graphs/Income_CA.png")
plt.show()


# In[37]:


#Which sectors in California people work for
#Professional	Service	Office	Construction	Production

#Professional = % employed in management, business, science, and arts
total_Professional = int((total_population_CA/100)*census_groupby_county_CA_df["Professional"].sum())
total_Professional

#Service = % employed in service jobs
total_ServiceWorkers = int((total_population_CA/100)*census_groupby_county_CA_df["Service"].sum())
total_ServiceWorkers

#Office = % employed in sales and office jobs
total_OfficeGoers = int((total_population_CA/100)*census_groupby_county_CA_df["Office"].sum())
total_OfficeGoers

#Construction = % employed in natural resources, construction, and maintenance
total_ConstructionWorkers = int((total_population_CA/100)*census_groupby_county_CA_df["Construction"].sum())
total_ConstructionWorkers

#Production = % employed in production, transportation, and material movement
total_ProductionWorkers = int((total_population_CA/100)*census_groupby_county_CA_df["Production"].sum())
total_ProductionWorkers

work_spread = [total_Professional, total_ServiceWorkers, total_OfficeGoers, total_ConstructionWorkers, total_ProductionWorkers]
work_spread
# 1, 3, 2, 5, 4


# In[38]:


#Creating a pie chart showing working sectors of california
colors = ["coral", "black", "purple", "lightgreen", "yellow"]
labels = ["Professional represented in Coral",  "Service represented in Black", "Office represented in purple",
          "Construction represented in Lightgreen", "Production in represented Yellow"]
patches = plt.pie(work_spread, colors = colors, labels = labels, shadow = True, autopct='%1.2f%%')


# In[39]:


# Saves an image of our chart so that we can view it in a folder
plt.title("Sectors where Californians work")
plt.savefig("Output_graphs/WorkSectors_CA.png")
plt.show()


# In[40]:


#How are Californians getting around
#Drive	Carpool	Transit	Walk	OtherTransp	WorkAtHome

#Professional = % commuting alone in a car, van, or truck
total_Drivers = int((total_population_CA/100)*census_groupby_county_CA_df["Drive"].sum())
total_Drivers

#Carpool = % carpooling in a car, van, or truck
total_Carpoolers = int((total_population_CA/100)*census_groupby_county_CA_df["Carpool"].sum())
total_Carpoolers

#Transit = % commuting on public transportation
total_PublicCommuters = int((total_population_CA/100)*census_groupby_county_CA_df["Transit"].sum())
total_PublicCommuters

#Walk = % walking to work
total_Walkers = int((total_population_CA/100)*census_groupby_county_CA_df["Walk"].sum())
total_Walkers

#OtherTransp = % commuting via other means
total_OtherTransporters = int((total_population_CA/100)*census_groupby_county_CA_df["OtherTransp"].sum())
total_OtherTransporters

#WorkAtHome = % working at home
total_WorkAtHomers = int((total_population_CA/100)*census_groupby_county_CA_df["WorkAtHome"].sum())
total_WorkAtHomers

commute_spread = [total_Drivers, total_Carpoolers, total_PublicCommuters, total_Walkers, total_OtherTransporters,  total_WorkAtHomers]
commute_spread


# In[41]:


#Creating a pie chart showing commuter sectors of california
#colors = ["red", "blue", "green", "yellow", "purple", "gray"]
colors = ["coral", "gray", "purple", "lightgreen", "yellow", "lightskyblue"]
labels = ["Drivers represented in Coral",  "Carpoolers represented in Gray", 
          "Public commuters represented in Purple", "Walkers represented in Lightgreen", "Others represented in Yellow",
          "Work@homers represented in Lightskyblue"]
patches = plt.pie(commute_spread, colors = colors, labels = labels, shadow = True, autopct='%1.1f%%')


# In[42]:


# Saves an image of our chart so that we can view it in a folder
plt.title("How do Californians commute to work")
plt.savefig("Output_graphs/Commuters_CA.png")
plt.show()


# In[43]:


#What kind of work Californians are doing
#Employed	PrivateWork	PublicWork	SelfEmployed	FamilyWork	Unemployment

#Employed = % employed (16+)
#total_Employed = int((total_population_CA/100)*census_groupby_county_CA_df["Employed"].sum())
#total_Employed

#PrivateWork = % employed in private industry
total_PrivateWorkers = int((total_population_CA/100)*census_groupby_county_CA_df["PrivateWork"].sum())
total_PrivateWorkers

#ublicWork = % employed in public jobs
total_PublicWorkers = int((total_population_CA/100)*census_groupby_county_CA_df["PublicWork"].sum())
total_PublicWorkers

#SelfEmployed = % self-employed
total_SelfEmployers = int((total_population_CA/100)*census_groupby_county_CA_df["SelfEmployed"].sum())
total_SelfEmployers

#FamilyWork = % in unpaid family work
total_FamilyWorkers = int((total_population_CA/100)*census_groupby_county_CA_df["FamilyWork"].sum())
total_FamilyWorkers

#Unemployment = Unemployment rate (%)
total_unemployed = int((total_population_CA/100)*census_groupby_county_CA_df["Unemployment"].sum())
total_unemployed

employment_type_spread = [total_PrivateWorkers, total_PublicWorkers, total_SelfEmployers, total_FamilyWorkers, total_unemployed]
employment_type_spread


# In[44]:


#Creating a pie chart showing commuter sectors of california
colors = ["lightskyblue", "green", "yellow", "black", "red"]
labels = [ "total_PrivateWorkers represented in LightSkyBlue", "Public commuters represented in Green", 
          "total_SelfEmployers represented in yellow", "total_FamilyWorkers represented in Black", 
          "total_unemployed represented in Red"]
patches = plt.pie(employment_type_spread, colors = colors, labels = labels, shadow = False, autopct='%1.1f%%')


# In[45]:


# Saves an image of our chart so that we can view it in a folder
plt.title("Employment status of Californians")
plt.savefig("Output_graphs/employment_type_CA.png")
plt.show()


# In[46]:


#Income per person in each county and see top 5 for highest average income counties
#what are some counties with highest female/male ratio
#IncomePerPerson = census_groupby_county_CA_df["Income"]/census_groupby_county_CA_df["TotalPop"]
#IncomePerPerson = census_groupby_county_CA_df["Income"]


# In[47]:


#census_groupby_county_CA_df["IncomePerPerson"] = IncomePerPerson
# Export file as a CSV, without the Pandas index, but with the header
#census_groupby_county_CA_df.to_csv("Output/census_groupby_county_CA.csv", encoding = "latin-1", index=False, header=True)


# In[48]:


top_high_income = top_highest(census_groupby_county_CA_df, "Income", 5)
#counties_high_income_per_person = high_income_per_person[["County", "IncomePerPerson"]]
#print(counties_high_income_per_person)
high_income = top_high_income[["County", "Income"]]
high_income


# In[49]:


#How is poverty level esp in high income places
poverty_in_thousands = ((census_groupby_county_CA_df["Poverty"]/100)*census_groupby_county_CA_df["TotalPop"])/1000
#child_poverty = census_groupby_county_CA_df["ChildPoverty"]
income_in_thousands = census_groupby_county_CA_df["Income"]/1000


# In[50]:


range= [min(poverty_in_thousands), max(poverty_in_thousands)]
print(range)
#rangeC = [min(child_poverty), max(child_poverty)]
#print(rangeC)
rangeI = [min(income_in_thousands), max(income_in_thousands)]
print(rangeI)


# In[51]:


#Poverty = % under poverty level vs Income levels
#ChildPoverty = % of children under poverty level vs Income
plt.title("under poverty level vs Income levels")
plt.xlabel("Income in thousands\n Note: Circle size correlates to a factor of Income")
plt.ylabel("Poverty level in thousands")
plt.xlim(30, 110)
plt.ylim(0, 4500000)
plt.scatter(income_in_thousands, poverty_in_thousands, marker="o", facecolors="coral", edgecolors="black",
            s=2*income_in_thousands, alpha=0.75)
#plt.tight_layout()

# Save the figure
plt.savefig("Output_graphs/Income levels and Poverty.png")
plt.show()


# In[52]:


fig, ax = plt.subplots()
fit = np.polyfit(income_in_thousands, poverty_in_thousands, deg=1)
#print(fit)
plt.xlim(30, 110)
plt.ylim(0, 500000)
plt.title("under poverty level vs Income levels with a trend line")
plt.xlabel("Income in thousands\n Note: Circle size correlates to a factor of Income")
plt.ylabel("Poverty level in thousands removing one high outlier")
ax.plot(income_in_thousands, fit[0] * income_in_thousands + fit[1], color='red')
ax.scatter(income_in_thousands, poverty_in_thousands, marker="o", facecolors="coral", edgecolors="black",
            s=2*income_in_thousands, alpha=0.75)
# Save the figure
plt.savefig("Output_graphs/Income levels and Poverty with a trend line.png")
# Show plot
plt.show()

