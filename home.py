import streamlit as st

st.set_page_config(page_title="Home Page", page_icon="🏠", layout="centered")

st.title("🏠 Welcome to the Food Shopping App")
st.write("This is the homepage.")

st.markdown("---")

st.header("Quick Links")

# Use Streamlit's built-in page navigation links
st.page_link("pages/1_Meal Planner.py", label="🗓️ Meal Planner")
st.page_link("pages/2_Recipes.py", label="🍽️ Recipes")
st.page_link("pages/3_Shopping List.py", label="🛒 Shopping List")

st.markdown("---")

st.info("Customize this layout to match your brand or project.")
