# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

# Add a Multiselect
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
)

# Cleaning Up Empty Brackets
if ingredients_list:
        ingredients_string = ''
        
        for fruit_chosen in ingredients_list:
                ingredients_string += fruit_chosen + ' '
                st.subheader(fruit_chosen + ' Nutrition Information')
                fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
                fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    
    #st.write(ingredients_string) --only for testing

    # Build a SQL Insert Statement & Test It
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    # Add a Submit Button
    time_to_insert = st.button('Submit Order')
    
    # Insert the Order into Snowflake
    if time_to_insert: 
        #IF Block dependent on the submit button being clicked by the customer
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")










