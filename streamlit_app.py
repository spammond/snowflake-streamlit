import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
  
streamlit.title("Spammond's Diner")

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('Build your own Smoothie')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Apple','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the results on the page.
streamlit.dataframe(fruits_to_show)

#################################################################################################################
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice's Fruit Advice")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    streamlit.write('Information for: ', fruit_choice)
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
  streamlit.error()

#################################################################################################################
streamlit.text("The fruit load list contains: ")
def get_fruit_list():
  with my_cnx.cursor() as mycur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

if streamlit.button('Load fruits'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.dataframe(get_fruit_list())

#################################################################################################################
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as mycur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "') ")
    return 'Thanks for adding' + new_fruit
  
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add Fruit'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.write(insert_row_snowflake(add_my_fruit))
