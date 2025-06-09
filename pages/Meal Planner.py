import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Meal Planner", page_icon="🗓️", layout="centered")
st.title("🗓️ Weekly Meal Planner")
st.write("Plan meals for multiple days using your saved recipes.")

RECIPE_FILE = "recipes.csv"
MEALS = ["Breakfast", "Lunch", "Tea", "Snacks"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Load recipes
if os.path.exists(RECIPE_FILE):
    recipes_df = pd.read_csv(RECIPE_FILE)
    recipe_names = sorted(recipes_df["Recipe"].unique().tolist())
else:
    st.error("No recipes found. Please add recipes first.")
    st.stop()

# Select how many days to plan
num_days = st.slider("How many days would you like to plan for?", min_value=1, max_value=7, value=3)
selected_days = DAYS[:num_days]

# Initialize session state
if "weekly_plan" not in st.session_state:
    st.session_state.weekly_plan = {
        day: {meal: "" for meal in MEALS} for day in selected_days
    }

# Update days if number changes
for day in selected_days:
    if day not in st.session_state.weekly_plan:
        st.session_state.weekly_plan[day] = {meal: "" for meal in MEALS}

# Planner UI
st.subheader("🍽️ Select Recipes for Each Meal")
for day in selected_days:
    st.markdown(f"### 📅 {day}")
    for meal in MEALS:
        current = st.session_state.weekly_plan[day].get(meal, "")
        selected = st.selectbox(
            f"{meal} for {day}",
            [""] + recipe_names,
            index=(recipe_names.index(current) + 1) if current in recipe_names else 0,
            key=f"{day}_{meal}"
        )
        st.session_state.weekly_plan[day][meal] = selected

# Show summary
st.subheader("📋 Your Weekly Plan")
for day in selected_days:
    st.markdown(f"**{day}**")
    for meal in MEALS:
        recipe = st.session_state.weekly_plan[day].get(meal, "")
        st.markdown(f"- {meal}: {recipe if recipe else '— not selected —'}")

# Clear option
if st.button("🔄 Clear Plan"):
    st.session_state.weekly_plan = {
        day: {meal: "" for meal in MEALS} for day in selected_days
    }
    st.experimental_rerun()
