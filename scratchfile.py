st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", ["Map","Chart","Download"])
if selection == "Map":
    page1()
if selection == "Chart":
    page2()
if selection == "Download":
    page3()


        start_date = st.date_input("Start date:", min_date) #Ask for date input, default value is latest date
        end_date = st.date_input("End date:", max_date.sftrtime()) #Ask for date input, default value is latest date


def get_date(df): #Function to call date
    min_date = pd.to_datetime(df["reg_date"].min(), errors='coerce').dt.strftime('%m/%d/%Y') #Get oldest registration date
    max_date = pd.to_datetime(df["reg_date"].max(), errors='coerce').dt.strftime('%m/%d/%Y') #Get latest registration date
    return min_date, max_date

def filter_date(df,start_date,end_date): #Function to filter data by date range
    start_date = start_date.strftime("%m/%d/%Y") #Convert format of dates
    end_date = end_date.strftime("%m/%d/%Y")
    filter = (df["reg_date"] > start_date) & (df["reg_date"] <= end_date) #Create a filter mask
    df_datefilter = df.loc[filter] #Locate data within the dataframe
    return df_datefilter
