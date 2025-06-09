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

# Number of days to plan
num_days = st.slider("How many days do you want to plan for?", 1, 7, 3)
selected_days = DAYS[:num_days]

# Initialize full session state for all days
if "weekly_plan" not in st.session_state:
    st.session_state.weekly_plan = {
        day: {meal: "" for meal in MEALS} for day in DAYS
    }

# Ensure selected_days exist in plan
for day in selected_days:
    if day not in st.session_state.weekly_plan:
        st.session_state.weekly_plan[day] = {meal: "" for meal in MEALS}

# Remove days outside the selected range
for day in list(st.session_state.weekly_plan.keys()):
    if day not in DAYS[:num_days]:
        st.session_state.weekly_plan.pop(day)

# Planner UI
st.subheader("👜 Plan Your Meals")
for day in selected_days:
    with st.expander(f"🌐 {day}", expanded=False):
        for meal in MEALS:
            saved = st.session_state.weekly_plan[day].get(meal, "")
            index = recipe_names.index(saved) + 1 if saved in recipe_names else 0
            choice = st.selectbox(
                f"{meal}",
                ["-"] + recipe_names,
                index=index,
                key=f"{day}_{meal}"
            )
            st.session_state.weekly_plan[day][meal] = choice

# Summary table
st.subheader("📄 Weekly Overview")
summary_data = []
for day in selected_days:
    row = {"Day": day}
    for meal in MEALS:
        row[meal] = st.session_state.weekly_plan[day].get(meal, "")
    summary_data.append(row)

summary_df = pd.DataFrame(summary_data)
st.dataframe(summary_df, use_container_width=True)

# Clear plan
if st.button("🔄 Clear Plan"):
    st.session_state.weekly_plan = {
        day: {meal: "" for meal in MEALS} for day in DAYS
    }
    st.experimental_rerun()

# Pass data to other pages
selected_recipes = {
    meal for meals in st.session_state.weekly_plan.values()
    for meal in meals.values() if meal and meal != "-"
}
st.session_state["selected_recipes"] = list(selected_recipes)
st.session_state["recipes_df"] = recipes_df
st.session_state["meal_plan"] = st.session_state.weekly_plan

