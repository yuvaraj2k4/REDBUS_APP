import streamlit as st
import mysql.connector
import pandas as pd

def get_data_from_db(query):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="20022004@Yuva",
        database="red_bus_data"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

st.set_page_config(page_title='Redbus Data Informations', layout='wide')

st.image('C:/Users/navee/Downloads/DH6ChRIU0AAj-8Q.jpg', use_column_width=True)

st.markdown("<h3 style='text-align: center;'>RBFIRST: Where every journey begins with a perfect plan.</h3>", unsafe_allow_html=True)

st.markdown("<h1 style='color: red;'>Redbus Data Filtering Information</h1>", unsafe_allow_html=True)

query = "SELECT * FROM bus_details"
data = pd.DataFrame(get_data_from_db(query))

st.sidebar.header("Filter Options")

filtered_data = data

route_filter = st.sidebar.selectbox('Select Route', data['Route_name'].unique(), index=0)
if st.sidebar.button('Apply Route Filter'):
    filtered_data = filtered_data[filtered_data['Route_name'] == route_filter]

ac_values = data['AC/NON AC'].dropna().unique()
ac_values = [value for value in ac_values if value != "" and value.lower() != "unknown"]
ac_filter = st.sidebar.selectbox('Select AC/Non AC', ac_values, index=0)
if st.sidebar.button('Apply AC/Non AC Filter'):
    filtered_data = filtered_data[filtered_data['AC/NON AC'] == ac_filter]

seat_type_values = data['SLEEPER/SEATER'].dropna().unique()
seat_type_values = [value for value in seat_type_values if value != "" and value.lower() != "unknown"]
seat_type_filter = st.sidebar.selectbox('Select Sleeper/Seater', seat_type_values, index=0)
if st.sidebar.button('Apply Sleeper/Seater Filter'):
    filtered_data = filtered_data[filtered_data['SLEEPER/SEATER'] == seat_type_filter]

price_range = st.sidebar.slider('Select Price Range', int(data['Price'].min()), int(data['Price'].max()), (500, 1500))
if st.sidebar.button('Apply Price Filter'):
    filtered_data = filtered_data[filtered_data['Price'].between(price_range[0], price_range[1])]

ratings_range = st.sidebar.slider('Select Ratings Range', 0.0, 5.0, (3.0, 5.0))
if st.sidebar.button('Apply Ratings Filter'):
    filtered_data = filtered_data[filtered_data['Ratings'].between(ratings_range[0], ratings_range[1])]

styled_data = filtered_data.style.applymap(lambda _: 'color: red')
st.dataframe(styled_data)

st.write(f"Showing {len(filtered_data)} buses for the selected filters.")
