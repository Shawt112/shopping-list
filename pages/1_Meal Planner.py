import streamlit as st
import pandas as pd
import os
import json

st.set_page_config(page_title="Meal Planner", page_icon="🗓️", layout="centered")
st.title("🗓️ Weekly Meal Planner")

RECIPE_FILE = "recipes.csv"
PLAN_FILE = "meal_plan.json"
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

# Load persisted plan
def load_plan():
    if os.path.exists(PLAN_FILE):
        with open(PLAN_FILE, "r") as f:
            return json.load(f)
    return {day: {meal: "" for meal in MEALS} for day in DAYS}

# Save plan to file
def save_plan(plan):
    with open(PLAN_FILE, "w") as f:
        json.dump(plan, f)

# Session state
if "weekly_plan" not in st.session_state:
    st.session_state.weekly_plan = load_plan()

# Ensure all selected days exist
for day in selected_days:
    if day not in st.session_state.weekly_plan:
        st.session_state.weekly_plan[day] = {meal: "" for meal in MEALS}

# Remove days not in selection
for day in list(st.session_state.weekly_plan.keys()):
    if day not in selected_days:
        st.session_state.weekly_plan.pop(day)

# Planner UI
st.subheader("👜 Plan Your Meals")
updated = False
for day in selected_days:
    with st.expander(f"🌐 {day}", expanded=False):
        for meal in MEALS:
            current = st.session_state.weekly_plan[day].get(meal, "")
            index = recipe_names.index(current) + 1 if current in recipe_names else 0
            choice = st.selectbox(
                f"{meal}",
                ["-"] + recipe_names,
                index=index,
                key=f"{day}_{meal}"
            )
            if st.session_state.weekly_plan[day][meal] != choice:
                st.session_state.weekly_plan[day][meal] = choice
                updated = True

if updated:
    save_plan(st.session_state.weekly_plan)

# Weekly summary
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
    save_plan(st.session_state.weekly_plan)
    st.experimental_rerun()

# Share with other pages
selected_recipes = {
    meal for meals in st.session_state.weekly_plan.values()
    for meal in meals.values() if meal and meal != "-"
}
st.session_state["selected_recipes"] = list(selected_recipes)
st.session_state["recipes_df"] = recipes_df
st.session_state["meal_plan"] = st.session_state.weekly_plan

# Save weekly_plan persistently
with open("weekly_plan.json", "w") as f:
    json.dump(st.session_state.weekly_plan, f)

# Also persist recipe data (optional, to avoid CSV reload elsewhere)
recipes_df.to_csv("recipes_cache.csv", index=False)
