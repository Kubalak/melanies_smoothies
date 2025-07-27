# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie! :cup_with_straw:")


name_on_order = st.text_input('Name on Smoothie:', max_chars=100)

st.write(
  """Choose fruits you want in your Smoothie!
  """
)

session = get_active_session()
my_df = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'))
# st.dataframe(data=my_df, use_container_width=True)

# option = st.selectbox('How would you like to be contacted?', ('Email', 'Home Phone', 'Mobile Phone'))

options = st.multiselect("Choose up to 5 ingredients:",
        my_df,
        max_selections=5
        )

if options:
    ingredients = ' '.join([str(item) for item in options])
    my_insert_stmt = f"insert into smoothies.public.orders(name_on_order, ingredients) values ('{name_on_order}','{ingredients}')"
    # st.write(ingredients)
    # st.write(my_insert_stmt)
    submit = st.button("Submit order :cup_with_straw:")
    if submit and ingredients:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")
