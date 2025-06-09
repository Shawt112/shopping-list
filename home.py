import streamlit as st

st.set_page_config(page_title="Home Page", page_icon="🏠", layout="centered")

st.title("🏠 Welcome to My Homepage")
st.write("This is a simple homepage built using Streamlit.")

st.markdown("---")

st.header("🚀 Quick Links")

# Use Streamlit's built-in page navigation links
st.page_link("pages/About.py", label="📖 About")
st.page_link("pages/Projects.py", label="🛠️ Projects")
st.page_link("pages/Contact.py", label="📬 Contact")
st.page_link("pages/Meal Planner.py", label="🗓️ Meal Planner")
st.page_link("pages/Recipes.py", label="🍽️ Recipes")
st.page_link("pages/Shopping List.py", label="🛒 Shopping List")

st.markdown("---")

st.info("Customize this layout to match your brand or project.")
