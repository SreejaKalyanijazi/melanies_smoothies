import streamlit as st
from snowflake.snowpark.functions import col
# Write directly to the app
st.title("Customize your smoothie :cup_with_straw:")
st.write(
 "Choose fruits that you want in your custom smoothie"
)

name_on_the_order = st.text_input("Name on the Smoothie:")
st.write("The name on your Smoothie will be", name_on_the_order)

# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Apple", "Strawberries", "Mango"))

# st.write("Your favorite fruit is:", option)
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list=st.multiselect(
    'Choose upto 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string=''
    for each_ingredient in ingredients_list:
        ingredients_string+=each_ingredient+' '
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_the_order)
            values ('""" + ingredients_string + """','""" + name_on_the_order + """')"""

    # st.write(my_insert_stmt)
    
    time_to_submit=st.button('Submit Order')
    if time_to_submit:
        session.sql(my_insert_stmt).collect()
        
    st.success('Your Smoothie is ordered!', icon="✅")
