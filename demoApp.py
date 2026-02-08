import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# now we have do cleaning on our data
# cleaning steps
#  1.drop remark col
#  2.set index  sno
#  3.rename col
#  4.convert amount to cr to rs
#  5.date col
#  6.drapna

st.set_page_config(layout='wide',page_title='Startup-Analysis')
# first step is read startup_funding.csv
# after all cleaning you have to convert that cleaned file into csv
# then use df as that cleaned file.

# df = pd.read_csv('startup_funding.csv')
df = pd.read_csv('startup_cleaned.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['year']=df['date'].dt.year
df['month']=df['date'].dt.month


# cleaned file

# st.dataframe(df) 
st.sidebar.title('Startup Funding Analysis')

def load_overall_analysis():
    st.title('OverAll Analysis : ')
    col1,col2,col3,col4 = st.columns(4)
    # total investment
    with col1:
        total = round(df['amount'].sum())
        st.metric('Total Investment : ',str(total)+' Cr')

    # max investment
    with col2:
        max = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Max Investment : ',str(max)+' Cr')
    
    # avg investment
    with col3:
        avg = round(df.groupby('startup')['amount'].sum().mean())
        st.metric('Avg Investment : ',str(avg)+' Cr')
        
    # total funded startup
    with col4:
        num_startup = df['startup'].nunique()
        st.metric('Total Funded Startups : ',str(num_startup))
        
    # Month on Month Chart 

    st.header('Month on Month Graph : ')
    selected_option = st.selectbox('Select type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
    else:    
        temp_df = df.groupby(['year','month'])['amount'].count().reset_index()
        
    temp_df['temp_x']= temp_df['month'].astype('str')+ '-' + temp_df['year'].astype('str')
    
    fig3,ax3 = plt.subplots()
    ax3.plot(temp_df['temp_x'],temp_df['amount'])
    st.pyplot(fig3) 
    


def load_investor_dateil(investor):
    st.title(investor)
    # load the recent 5 investments of the investor
    last5_df = df[df['Investors'].str.contains(investor)].head(5)[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments : ')
    st.dataframe(last5_df)
    
    # making columns
    col1,col2,col3 = st.columns(3)
    
    with col1:
        # biggest investment
        big_series = df[df['Investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments : ')
        # st.dataframe(big_series)
        
        # streamlit ko use karke map plot karna hai 
        fig,ax = plt.subplots()
        ax.barh(big_series.index,big_series.values)
        st.pyplot(fig)
        
    with col2:
        veritical_series = df[df['Investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        
        st.subheader('Sector Invested in : ')
        # streamlit ko use karke map plot karna hai 
        fig1,ax1 = plt.subplots()
        ax1.pie(veritical_series,labels=veritical_series.index,autopct="%0.01f%%    ")
        st.pyplot(fig1)
        
    with col3:
        # biggest investment
        stage_series = df[df['Investors'].str.contains(investor)].groupby('round')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Funding Type : ')
        # st.dataframe(big_series)
        
        # streamlit ko use karke map plot karna hai 
        fig3,ax3 = plt.subplots()
        ax3.pie(stage_series,labels=stage_series.index,autopct="%0.01f%%")
        st.pyplot(fig3)
        
    col4, col5 = st.columns(2)
    
    with col4:
        city_series = df[df['Investors'].str.contains(investor)].groupby('city')['amount'].sum()
        
        st.subheader('City : ')
        # streamlit ko use karke map plot karna hai 
        fig4,ax4 = plt.subplots()
        ax4.pie(city_series,labels=city_series.index,autopct="%0.01f%%")
        st.pyplot(fig4)    
    
    with col5:
        year_series = (
            df[df['Investors'].str.contains(investor)]
            .groupby('year')['amount']
            .sum()
        )
        fig5, ax5 = plt.subplots()
        ax5.plot(year_series.index, year_series.values, marker='o')
        ax5.grid(True)
        st.subheader('Year on Year Investment')
        st.pyplot(fig5)
        
    
    # similar investors
    
        
option = st.sidebar.selectbox('Select one',['OverAll Analysis','Startup','Investor'])

if option == 'OverAll Analysis':
        load_overall_analysis()
        
elif option == 'Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(set(df['Investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find investor Details')
    if btn2 :
        load_investor_dateil(selected_investor) # logic on line number 20

