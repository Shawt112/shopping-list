import streamlit as st
import pandas as pd
import os
import json

st.set_page_config(page_title="Shopping List", page_icon="🛒", layout="centered")

st.title("🛒 Shopping List")

# Restore weekly_plan if not in session
if "weekly_plan" not in st.session_state:
    if os.path.exists("weekly_plan.json"):
        with open("weekly_plan.json") as f:
            st.session_state["weekly_plan"] = json.load(f)
    else:
        st.error("No meal plan data found. Please use the Meal Planner first.")
        st.stop()

# Restore recipes_df if not in session
if "recipes_df" not in st.session_state:
    if os.path.exists("recipes_cache.csv"):
        st.session_state["recipes_df"] = pd.read_csv("recipes_cache.csv")
    else:
        st.error("No recipe data found. Please use the Recipes page first.")
        st.stop()

meal_plan = st.session_state["weekly_plan"]
recipes_df = st.session_state["recipes_df"]

# Collect all selected recipes from the planner
selected_recipes = set()
for day_meals in meal_plan.values():
    selected_recipes.update([m for m in day_meals.values() if m and m != "-"])

# Filter and collect ingredients
ingredients = recipes_df[recipes_df["Recipe"].isin(selected_recipes)]

# Aggregate duplicate ingredients
ingredients["Quantity"] = pd.to_numeric(ingredients["Quantity"], errors="coerce").fillna(0)
grouped = ingredients.groupby(["Ingredient", "Unit"], as_index=False)["Quantity"].sum()
grouped = grouped.sort_values(by="Ingredient")

# Display the shopping list
st.subheader("🧾 Combined Shopping List")
if grouped.empty:
    st.info("No ingredients to show. Make sure you've selected meals in the planner.")
else:
    grouped["Quantity"] = grouped["Quantity"].astype(str)  # Ensure it's printable
    grouped["Item"] = grouped.apply(lambda row: f"{row['Ingredient']} - {row['Quantity']} {row['Unit']}", axis=1)
    st.table(grouped[["Item"]].rename(columns={"Item": "Shopping Item"}))

    # Optionally download
    csv = grouped.to_csv(index=False)
    st.download_button("📥 Download Shopping List as CSV", csv, "shopping_list.csv", "text/csv")
