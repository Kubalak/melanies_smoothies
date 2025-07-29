import requests
import pandas as pd
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie! :cup_with_straw:")


name_on_order = st.text_input('Name on Smoothie:', max_chars=100)

st.write(
  """Choose fruits you want in your Smoothie!
  """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_df = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'),col('SEARCH_ON')).to_pandas()
# st.dataframe(data=my_df, use_container_width=True)

options = st.multiselect("Choose up to 5 ingredients:",
        my_df,
        max_selections=5
        )

if options:
    #ingredients = ' '.join([str(item) for item in options])
    ingredients = ''
    for fruit_chosen in options:
        ingredients += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        search_on = my_df[my_df['FRUIT_NAME'] == fruit_chosen]['SEARCH_ON'].iloc[0]
        smoothieroot_resp = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data=smoothieroot_resp.json(), use_container_width=True)
    
    # st.write(ingredients)
    # st.write(my_insert_stmt)
    submit = st.button("Submit order :cup_with_straw:")
    if submit and ingredients:
        my_insert_stmt = f"insert into smoothies.public.orders(name_on_order, ingredients) values ('{name_on_order}','{ingredients}')"
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")
