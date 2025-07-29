from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import streamlit as st

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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 Ingredients :',
    my_dataframe.collect(),  # get list of rows
    format_func=lambda row: row["FRUIT_NAME"],
    max_selections=5
)

if ingredients_list:
    ingredients_string = ' '.join([fruit["FRUIT_NAME"] for fruit in ingredients_list])

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
