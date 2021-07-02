'''
Name: Josephine Kantawiria
File name: Final Project
Section: CS230.HB3.SP21
'''

import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt

st.set_page_config(layout="wide") #Wide page width

DATA_URL = "https://data.ny.gov/api/views/iisn-hnyv/rows.csv?accessType=DOWNLOAD"

REGEX = "^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$"

INDEX = []
COUNTY = []
REG_DATE = []
REG_NO = []
LON = []
LAT = []
GEO = []

# ---------------------------------------------------------
# Load Data Functions
# ---------------------------------------------------------

def load_data(): #Read CSV file to lists
    raw_data = pd.read_csv(DATA_URL, delimiter=",")
    for row in raw_data.values:
        INDEX.append(row[0])
        COUNTY.append(row[1])
        REG_DATE.append(row[2])
        REG_NO.append(row[3])
        LON.append(float(row[4]))
        LAT.append(float(row[5]))
        GEO.append(row[6])

def df(): #Create dataframe
    data = {'county' : COUNTY,
            'reg_date' : REG_DATE,
            'reg_no': REG_NO,
            'lon' : LON,
            'lat' : LAT,
            'geo' : GEO
            }
    df = pd.DataFrame(data, index= INDEX)
    df['reg_date'] = pd.to_datetime(df['reg_date'])
    return df

# ---------------------------------------------------------
# Interactive Functions
# ---------------------------------------------------------

def get_date(df): #Function to call date
    min_date = pd.to_datetime(df["reg_date"].min()) #Get oldest registration date
    max_date = pd.to_datetime(df["reg_date"].max()) #Get latest registration date
    today = pd.to_datetime("today")
    return min_date, max_date, today

def filter_date(df,start_date,end_date): #Function to filter data by date range
    start_date = start_date.strftime("%m/%d/%Y") #Convert format of dates
    end_date = end_date.strftime("%m/%d/%Y")
    filter = (df["reg_date"] > start_date) & (df["reg_date"] <= end_date) #Create a filter mask
    df_datefilter = df.loc[filter] #Locate data within the dataframe
    return df_datefilter

def filter_county(df_datefilter,county_choices): #Function to filter data by county choice
    if "All" in county_choices or not county_choices: #Option All and if left empty will show all outputs
        df_countyfilter = df_datefilter
    else: #Filtered by the counties selected
        df_countyfilter = df_datefilter[df_datefilter["county"].isin(county_choices)]
    return df_countyfilter

def df_chart(county_index, county_count): #Create dataframe for chart
    chart_df = pd.DataFrame(
        county_count,
        index= county_index,
        columns=["Frequency"])
    return chart_df

def county_freq(df_countyfilter): #Count the frequency of the county selected
    county_count = {}
    for county in df_countyfilter.county: #Dictionary out of the country name and number of parks in that county
        if county not in county_count:
            county_count[county] = 0
        county_count[county] += 1
    county_count = dict(sorted(county_count.items())) #Sort alphabetically by key
    return county_count

def bar_chart(county_count,color): #Plots bar chart by county
    x = range(len(county_count))
    keys = list(county_count.keys()) #Takes dictionary key
    values = list(county_count.values()) #Takes dictionary value

    fig, ax = plt.subplots()
    ax.bar(x, values , width=0.45, label="Frequency", color=color) #Plot bar chart
    ax.grid(axis="y", color = "lightgray",linestyle="-.", linewidth= .25)
    ax.set_xticks(x)
    if len(county_count) > 8: #If the county chosen is more than 8
        ax.set_xticklabels((keys), rotation=90)
        if len(county_count) > 20: #If the county chosen is more than 20
            for tick in ax.xaxis.get_major_ticks(): #Smaller tick fonts
                tick.label.set_fontsize(5)
    else: #If the county chosen is less than 8
        ax.set_xticklabels(keys)

    st.pyplot(fig)
    st.set_option('deprecation.showPyplotGlobalUse', False) #Dismiss warning on streamlit

def line_chart(county_count,color): #Plots bar chart by county
    x = range(len(county_count))
    keys = list(county_count.keys()) #Takes dictionary key
    values = list(county_count.values()) #Takes dictionary value

    fig, ax = plt.subplots()
    ax.plot(x, values, label="Frequency", color=color) #Plot line chart
    ax.grid(color = "lightgray",linestyle="-.", linewidth= .25)
    ax.set_xticks(x)
    if len(county_count) > 8: #If the county chosen is more than 8
        ax.set_xticklabels((keys), rotation=90)
        if len(county_count) > 20: #If the county chosen is more than 20
            for tick in ax.xaxis.get_major_ticks(): #Smaller tick fonts
                tick.label.set_fontsize(5)
    else: #If the county chosen is less than 8
        ax.set_xticklabels(keys)

    st.pyplot(fig)
    st.set_option('deprecation.showPyplotGlobalUse', False) #Dismiss warning on streamlit

def scatter_chart(county_count,color): #Plots bar chart by county
    x = range(len(county_count))
    keys = list(county_count.keys()) #Takes dictionary key
    values = list(county_count.values()) #Takes dictionary value

    fig, ax = plt.subplots()
    ax.scatter(x, values, label="Frequency", color= color)
    ax.grid(color = "lightgray",linestyle="-.", linewidth= .25)
    ax.set_xticks(x)
    if len(county_count) > 8: #If the county chosen is more than 8
        ax.set_xticklabels((keys), rotation=90)
        if len(county_count) > 20: #If the county chosen is more than 20
            for tick in ax.xaxis.get_major_ticks(): #Smaller tick fonts
                tick.label.set_fontsize(5)
    else: #If the county chosen is less than 8
        ax.set_xticklabels(keys)

    st.pyplot(fig)
    st.set_option('deprecation.showPyplotGlobalUse', False) #Dismiss warning on streamlit

def button(): #For form
    button = st.button("View link") #Button widget to view link
    if button == True:
        st.markdown("Link to download data: https://data.ny.gov/api/views/iisn-hnyv/rows.csv?accessType=DOWNLOAD")

# ---------------------------------------------------------
# Pages
# ---------------------------------------------------------

def page0(): #Home page
    st.image("https://drive.google.com/uc?export=view&id=1BSJLKaIigquicNUgN6bPcELapk1JGMXI") # Image from drive

    st.header("Introduction to my Final Project")

    st.markdown('''Welcome everyone to my final project for my Python class!
    In this in this assignment, we are expected to develop an interactive data-driven 
    web-based Python application that shows our mastery of many coding concepts as we interact 
    with data real world data. The data set I chose to use for this assignment is the National 
    Parks in New York data. Below are some of the coding skills I have demonstrated in this assignment:
    
    • Coding Fundamentals: data types, if statements, loops, formatting, etc. 
    • Data Structures: Interact with lists, tuples, dictionaries (keys, values, items)
    • Functions:  passing positional and optional arguments,  returning values
    • Files: Reading data from a CSV file into a DataFrame
    • Pandas: Module functions and DataFrames to manipulate large data sets
    • MatPlotLib or pandas: Creating different types of charts
    • StreamLit.io: Displaying interactive widgets and charts
    ''')

def page1(): #Map page
    min_date, max_date, today = get_date(df)

    col1, buffer, col2 = st.beta_columns([9,1,20]) #Split page into 3 columns with buffer in the middle

    with col1: #Left narrow column
        st.header("")
        start_date = st.date_input("Start Date:", min_date, min_value= min_date, max_value= today)
        end_date = st.date_input("End Date:", max_date, min_value= min_date, max_value= today)

        county_options = sorted(list(set(COUNTY))) #Create unique list of the county list
        county_options.append("All") #Add "All" option
        county_choices = st.multiselect("Select counties:",county_options,["All"],
                                        help="Data will be filtered according to the counties selected."
                                             "Leave empty or select \"All\" to view data from all counties.") #Multiselect widget

        if start_date < end_date:
            st.success("Success: Data filtered") #Success message
        else:
            st.error("Error: End date must fall after start date.") #Error message

    with col2:
        st.header("Map of National Parks in New York")
        df_datefilter = filter_date(df,start_date,end_date) #Filters by date range
        df_countyfilter = filter_county(df_datefilter,county_choices) #Filters by county
        st.map(df_countyfilter) #Puts data into a map

    expander = st.beta_expander("More information on program") #To learn more about the program
    expander.markdown('''This is an interactive program that showcase the data set using a map. 
    To navigate, you may zoom in and out on the map, as well as move left and right. 
    The data set can be filtered national registration date. Currently, it is set at 
    default - the start date by the oldest national registration date and the end date by the 
    latest national registration date. At the default stage, you are viewing all the data available 
    on the data set. Please make sure that your start date is not later than the end date, 
    otherwise an error message will pop up. You can also filter the data set by county. If you choose 
    to leave it blank or select "All", it will feature all the data that are available between 
    the date range you selected. It is a multiselect box so feel free to choose more than one county 
    on the list.''')

def page2(): #Chart Page
    st.header("Number of National Parks by County in New York")

    col1, buffer, col2 = st.beta_columns([20,1,9])

    with col2:
        county_options = sorted(list(set(COUNTY))) #Create unique list of the county list
        county_options.append("All")
        county_choices = st.multiselect("Select counties:",county_options,["All"],
                                            help="Data will be filtered according to the counties selected."
                                                 "Leave empty or select \"All\" to view data from all counties.") #Multiselect widget
        graph_choice = st.selectbox("Graph display:", ["Bar","Line","Scatter"])
        color = st.color_picker("Select color:")

    with col1:
        df_countyfilter = filter_county(df,county_choices)
        county_count = county_freq(df_countyfilter)
        if graph_choice == "Bar":
            bar_chart(county_count,color) #Plots bar function
        if graph_choice == "Line":
            if len(county_choices) == 1 and "All" not in county_choices:
                st.error("Error. Line chart will not appear if only one county is selected, please select other display"
                         "modes or select more. Thank you.") #Limits line graph to county_choices > 1
            else:
                line_chart(county_count,color) #Plots line function
        if graph_choice == "Scatter":
            scatter_chart(county_count,color) #Plots scatter function

    expander = st.beta_expander("More information on program") #To learn more about the program
    expander.markdown('''This is an interactive program that shows frequency of national parks within each county via chart.
    There are three options of display mode: Bar, Line, and Scatter. For each chart, you are able to filter the counties
    you want to display and the color of your graph. It will change accordingly. For all of the charts, I noticed that
    after certain amount of countries display, the X-tick labels becomes hard to read. Hence, I came up with a solution,
    such as the following: 1) When you select more than 8 countries, the X-tick labels will rotate 90 degrees, creating
    more space for other labels. 2) When you select more than 20 countries, the X-tick labels will not only be rotated
    but also will lower in font size to accommodate for the smaller space available. This will ensure that users are
    able to read every single label clearly and easily.
    ''')

def page3():
    st.header("Download Form")
    st.markdown("Please complete each field in the form to access link. Thank you.")
    field_1 = st.text_input("Your Name")
    if field_1 != "":
        field_2 = st.text_input("Your Email Address", help= "example@mail.com")
        if (re.search(REGEX, field_2)):
            field_3 = st.selectbox("Your Age", ["Click to select", "Under 18 years old", "19-65 years old", "66 years or older"])
            field_4 = st.selectbox("Are you a Student?",["Click to select", "Yes","No"], help="i.e. currently a high-school student, undergraduate studies, graduate studies, etc")
            if field_3 != "Click to select":
                if field_4 == "Yes":
                    button()
                if field_4 == "No":
                    field_5 = st.selectbox("If No, are you employed in an occupation within the education sector", ["Click to select", "Yes","No"], help="i.e. Teacher, Professors, Researcher, etc")
                    if field_5 == "Yes":
                        button()
                    if field_5 == "No":
                        st.error("Error. You do not qualify to receive link to download. Sorry.")

    today = pd.to_datetime("today")
    st.text(today)

    expander = st.beta_expander("More information on program")
    expander.markdown('''This is a form made out of st.text_input, st.selectbox, and st.button function. Fields will pop up
    as the user enters information. If the information does not match the qualifications of the field, it will not
    continue. There are help buttons for clarification. The idea of the form is that if this were to be a confidential
    data that is not available for public, the owner of the data can filter who gets access and who does not. In this case,
    if you are a student or working in the education sector, you will be qualified to receive link to download. Otherwise,
    it will give an error message saying that you are not qualified. The st.selectbox function does not have an empty default
    but uses the first index on the list as a pre-filled selection. So to go around this, I added an option for "Click to select",
    which is essentially just a placeholder to make sure users select an option. ''')

# ---------------------------------------------------------
# Streamlit Navigation
# ---------------------------------------------------------

st.title("CS230 Final Project")
st.text("By: Josephine Kantawiria")

load_data()
df = df()

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Home", "Map", "Chart", "Access Data"])
if selection == "Home":
    page0()
if selection == "Map":
    page1()
if selection == "Chart":
    page2()
if selection == "Access Data":
    page3()

