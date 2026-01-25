import streamlit as st
import pandas as pd
import os
import json

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Meal Planner", page_icon="🗓️", layout="centered")
st.title("🗓️ Weekly Meal Planner")

RECIPE_FILE = "recipes.csv"
PLAN_FILE = "meal_plan.json"

# Removed "Snacks"
MEALS = ["Breakfast", "Lunch", "Tea"]
# Fixed 7 days
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# ------------------ HELPERS ------------------
def empty_plan(days):
    return {day: {meal: "" for meal in MEALS} for day in days}

def load_plan():
    if os.path.exists(PLAN_FILE):
        with open(PLAN_FILE, "r") as f:
            return json.load(f)
    return empty_plan(DAYS)

def save_plan(plan):
    with open(PLAN_FILE, "w") as f:
        json.dump(plan, f)

# ------------------ LOAD RECIPES ------------------
if not os.path.exists(RECIPE_FILE):
    st.error("No recipes found. Please add recipes first.")
    st.stop()

recipes_df = pd.read_csv(RECIPE_FILE)
recipe_names = sorted(recipes_df["Recipe"].dropna().unique().tolist())

# ------------------ SESSION STATE ------------------
if "weekly_plan" not in st.session_state:
    st.session_state.weekly_plan = load_plan()

# 🔑 Reset counter (for dropdown keys)
if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

# ------------------ FIXED 7 DAYS ------------------
selected_days = DAYS

# Keep only selected days in plan
st.session_state.weekly_plan = {
    day: st.session_state.weekly_plan.get(day, {meal: "" for meal in MEALS})
    for day in selected_days
}

# ------------------ PLANNER UI ------------------
st.subheader("👜 Plan Your Meals")
updated = False

for day in selected_days:
    with st.expander(f"🌐 {day}", expanded=False):
        for meal in MEALS:
            stored_value = st.session_state.weekly_plan[day][meal]
            index = recipe_names.index(stored_value) + 1 if stored_value in recipe_names else 0

            choice = st.selectbox(
                meal,
                ["-"] + recipe_names,
                index=index,
                key=f"{day}_{meal}_{st.session_state.reset_counter}",
            )

            # Normalize "-" to empty string
            choice = "" if choice == "-" else choice

            if stored_value != choice:
                st.session_state.weekly_plan[day][meal] = choice
                updated = True

if updated:
    save_plan(st.session_state.weekly_plan)

# ------------------ SUMMARY ------------------
st.subheader("📄 Weekly Overview")
summary_df = pd.DataFrame(
    [{"Day": day, **st.session_state.weekly_plan[day]} for day in selected_days]
)
st.dataframe(summary_df, use_container_width=True)

# ------------------ CLEAR PLAN ------------------
if st.button("🔄 Clear Plan"):
    st.session_state.weekly_plan = empty_plan(selected_days)
    save_plan(st.session_state.weekly_plan)

    # Force dropdown recreation
    st.session_state.reset_counter += 1
    st.rerun()

# ------------------ SHARE STATE ------------------
selected_recipes = {
    recipe
    for day in st.session_state.weekly_plan.values()
    for recipe in day.values()
    if recipe
}

st.session_state["selected_recipes"] = list(selected_recipes)
st.session_state["recipes_df"] = recipes_df
st.session_state["meal_plan"] = st.session_state.weekly_plan
