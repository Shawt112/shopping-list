import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Meal Planner", page_icon="🗓️", layout="centered")
st.title("🗓️ Weekly Meal Planner")
st.write("Easily plan meals for the week. Optimized for mobile use.")

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

# Number of days
num_days = st.slider("How many days do you want to plan for?", 1, 7, 3)
selected_days = DAYS[:num_days]

# Session state
if "weekly_plan" not in st.session_state:
    st.session_state.weekly_plan = {
        day: {meal: "" for meal in MEALS} for day in selected_days
    }

# Keep state when day count changes
for day in selected_days:
    if day not in st.session_state.weekly_plan:
        st.session_state.weekly_plan[day] = {meal: "" for meal in MEALS}

# Mobile-friendly layout using expandable cards
st.subheader("👜 Plan Your Meals")
for day in selected_days:
    with st.expander(f"🌐 {day}", expanded=False):
        for meal in MEALS:
            current = st.session_state.weekly_plan[day].get(meal, "")
            selected = st.selectbox(
                f"{meal}",
                ["-"] + recipe_names,
                index=(recipe_names.index(current) + 1) if current in recipe_names else 0,
                key=f"{day}_{meal}"
            )
            st.session_state.weekly_plan[day][meal] = selected

# Summary in a table
st.subheader("📄 Weekly Overview")
summary_data = []
for day in selected_days:
    row = {"Day": day}
    for meal in MEALS:
        row[meal] = st.session_state.weekly_plan[day].get(meal, "")
    summary_data.append(row)

summary_df = pd.DataFrame(summary_data)
st.dataframe(summary_df, use_container_width=True)

# Clear button
if st.button("🔄 Clear Plan"):
    st.session_state.weekly_plan = {
        day: {meal: "" for meal in MEALS} for day in selected_days
    }
    st.experimental_rerun()
