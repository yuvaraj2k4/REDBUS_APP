import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

data = pd.read_csv(r"C:\Users\navee\OneDrive\Desktop\REDBUS_PROJECT\redbus_data.csv")

st.image(r"C:\Users\navee\Downloads\DH6ChRIU0AAj-8Q.jpg", 
         caption="Travel made easy. One bus, one click, one unforgettable journey.", use_column_width=True)

st.markdown("<h1 style='color: red;'>RedBus Data Explorer</h1>", unsafe_allow_html=True)

st.sidebar.header("Filters")

bus_types = data['Bus_type'].unique()
selected_bus_type = st.sidebar.multiselect("Select Bus Type", bus_types)

if st.sidebar.button('Apply Bus Type Selection'):
    if selected_bus_type:
        st.write(f"Selected Bus Type(s): {', '.join(selected_bus_type)}")
    else:
        st.write("No Bus Type selected. Showing all types.")

routes = data['Route_name'].unique()
selected_route = st.sidebar.multiselect("Select Route", routes)

if st.sidebar.button('Apply Route Selection'):
    if selected_route:
        st.write(f"Selected Route(s): {', '.join(selected_route)}")
    else:
        st.write("No Route selected. Showing all routes.")

min_price = int(data['Price'].min())
max_price = int(data['Price'].max())
price_range = st.sidebar.slider("Price Range (INR)", min_price, max_price, (min_price, max_price))

min_rating = float(data['Ratings'].min())
max_rating = float(data['Ratings'].max())
rating_filter = st.sidebar.slider("Star Rating Range", min_rating, max_rating, (min_rating, max_rating))

availability_filter = st.sidebar.radio(
    "Filter by Seat Availability",
    ('Show All', 'Available Seats Only')
)

with st.spinner('Applying filters, please wait...'):
    filtered_data = data[
        (data['Bus_type'].isin(selected_bus_type if selected_bus_type else bus_types)) &
        (data['Route_name'].isin(selected_route if selected_route else routes)) &
        (data['Price'] >= price_range[0]) & 
        (data['Price'] <= price_range[1]) & 
        (data['Ratings'] >= rating_filter[0]) & 
        (data['Ratings'] <= rating_filter[1])
    ]
    
    if availability_filter == 'Available Seats Only':
        filtered_data = filtered_data[filtered_data['Seats_Available'] != 'Sold Out']

if len(filtered_data) == 0:
    st.warning("No results found. Please adjust your filters.")
else:
    st.write(f"Showing {len(filtered_data)} results")
    st.dataframe(filtered_data, width=1500)  

    st.write("Statistics of Filtered Results:")
    st.write(f"Average Price: ₹{filtered_data['Price'].mean():.2f}")
    st.write(f"Average Rating: {filtered_data['Ratings'].mean():.1f} Stars")
