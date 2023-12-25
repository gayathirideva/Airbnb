# C:\Users\LENOVO\Projects\Airbnb.py

import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib as matplotlib
import pandas as pd
import os
import pymongo
from PIL import Image
import warnings
import streamlit as st

# Using object notation
# add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone")
# )

# # Using "with" notation
# with st.sidebar:
#     add_radio = st.radio(
#         "Choose a shipping method",
#         ("Standard (5-15 days)", "Express (2-5 days)")
#     )

st.set_page_config(page_title="AirBnb-Analysis", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart:   AirBnb-Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


# Side bar options to be added 

SELECT = option_menu(
    menu_title= "MENU",
    options = ["Home", "Data Analysis"],
    icons = ["house","activity"],
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white", "size": "cover", "width": "100"},
            "icon": {"color": "black", "font-size": "20px"},

            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
            "nav-link-selected": {"background-color": "#6F36AD"}}
    )

# MENU 

if SELECT == "Home":
    st.header('Airbnb Analysis')
    st.subheader("Analysing the Airbnb service provided by the host, who is willing to rent the property based on the ocassions.")

if SELECT == "Data Analysis":
    #st.write("selected Data Analysis of the Airbnb")
    # Upload the file got after the data cleaning 
    file_upload = st.file_uploader(label = "Select file", type =(["csv","txt","xls"]))

    if file_upload is not None :
        #fileName = file_upload.read()
        fileName = file_upload.name
        st.write(fileName)
        
        # Read as df 
        df = pd.read_csv(file_upload)
        st.write(df)
    else :
       st.write ("Choose a Correct file")

# Creating a side bar to select the neighbourhood 
       
    st.sidebar.header("Select filter :")

    neighbourhood_group = st.sidebar.multiselect("Pick your neighbourhood_group", df["neighbourhood_group"].unique())
    if not neighbourhood_group:
          df2 = df.copy()
    else:
         df2 = df[df["neighbourhood_group"].isin(neighbourhood_group)]


 # Create for neighbourhood
    neighbourhood = st.sidebar.multiselect("Pick the neighbourhood", df2["neighbourhood"].unique())
    if not neighbourhood:
        df3 = df2.copy()
    else:
        df3 = df2[df2["neighbourhood"].isin(neighbourhood)]

    # Filter the data based on neighbourhood_group, neighbourhood

    if not neighbourhood_group and not neighbourhood:
        filtered_df = df
    elif not neighbourhood:
        filtered_df = df[df["neighbourhood_group"].isin(neighbourhood_group)]
    elif not neighbourhood_group:
        filtered_df = df[df["neighbourhood"].isin(neighbourhood)]
    elif neighbourhood:
        filtered_df = df3[df["neighbourhood"].isin(neighbourhood)]
    elif neighbourhood_group:
        filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group)]
    elif neighbourhood_group and neighbourhood:
        filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]
    else:
        filtered_df = df3[df3["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]

# Group the neighbourhood using groupby room type 
        
    room_type_df = filtered_df.groupby(by=["room_type"], as_index=False)["price"].sum()


    col1, col2 = st.columns(2)
    with col1:
        st.subheader("room_type_ViewData") #room_type_ViewData
        fig = px.bar(room_type_df, x="room_type", y="price", text=['${:,.2f}'.format(x) for x in room_type_df["price"]],
                 template="seaborn")
        st.plotly_chart(fig, use_container_width=True, height=200)
    
    with col2:
        st.subheader("neighbourhood_group_ViewData") #neighbourhood_group_ViewData
        fig = px.pie(filtered_df, values="price", names="neighbourhood_group", hole=0.5)
        fig.update_traces(text=filtered_df["neighbourhood_group"], textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
     
# Create a scatter plot
    data1 = px.scatter(filtered_df, x="neighbourhood_group", y="neighbourhood", color="room_type")
    data1['layout'].update(title="Room_type in the Neighbourhood and Neighbourhood_Group wise data using Scatter Plot.",
                        titlefont=dict(size=20), xaxis=dict(title="Neighbourhood_Group", titlefont=dict(size=20)),
                        yaxis=dict(title="Neighbourhood", titlefont=dict(size=20)))
    st.plotly_chart(data1, use_container_width=True)

    with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
     st.write(filtered_df.iloc[:500, 1:20:2]) #.style.background_gradient(cmap="Oranges"))

import plotly.figure_factory as ff

st.subheader(":point_right: Neighbourhood_group wise Room_type and Minimum stay nights")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["neighbourhood_group", "neighbourhood", "reviews_per_month", "room_type", "price", "minimum_nights", "host_name"]]
    fig = ff.create_table(df_sample, colorscale="Cividis")
    st.plotly_chart(fig, use_container_width=True)

 # map function for room_type

# If your DataFrame has columns 'Latitude' and 'Longitude':
st.subheader("Airbnb Analysis in Map view")
df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
st.map(df)
