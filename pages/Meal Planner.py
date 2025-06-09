import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Meal Planner", page_icon="🗓️", layout="centered")
st.title("🗓️ Daily Meal Planner")
st.write("Plan your daily meals from your saved recipes.")

RECIPE_FILE = "recipes.csv"
MEALS = ["Breakfast", "Lunch", "Tea", "Snacks"]

# Load recipes
if os.path.exists(RECIPE_FILE):
    recipes_df = pd.read_csv(RECIPE_FILE)
    recipe_names = sorted(recipes_df["Recipe"].unique().tolist())
else:
    st.error("No recipes found. Please add recipes first.")
    st.stop()

# Initialize session state for planner
if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = {meal: "" for meal in MEALS}

st.subheader("🍽️ Select Recipes for Each Meal")

# UI to select and update meal plan
for meal in MEALS:
    current_value = st.session_state.meal_plan.get(meal, "")
    selected = st.selectbox(
        f"{meal} Recipe",
        [""] + recipe_names,
        index=(recipe_names.index(current_value) + 1) if current_value in recipe_names else 0,
        key=f"select_{meal}"
    )
    st.session_state.meal_plan[meal] = selected

# Display current plan
st.subheader("📋 Current Meal Plan")
for meal, recipe in st.session_state.meal_plan.items():
    st.markdown(f"**{meal}**: {recipe if recipe else '— not selected —'}")

# Optional reset
if st.button("🔄 Clear Plan"):
    for meal in MEALS:
        st.session_state.meal_plan[meal] = ""
    st.experimental_rerun()
