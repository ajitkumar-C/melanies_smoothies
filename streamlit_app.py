from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import streamlit as st
import requests
import pandas as pd

# Snowflake connection settings
connection_parameters = st.secrets["snowflake"]

# Create the session
session = Session.builder.configs(connection_parameters).create()

# Streamlit UI
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Get fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe , use_container_width=True)
# st.stop()
pd_df= my_dataframe.to_pandas()


ingredients_list = st.multiselect(
'Choose up to 5 Ingredients :',my_dataframe,max_selections=5
)
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
        smoothiefroot_response = requests.get("https://www.fruityvice.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+name_on_order +'!', icon="✅")




