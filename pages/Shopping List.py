import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Shopping List", page_icon="🛒", layout="centered")
st.title("🛒 Shopping List Generator")

# Constants
RECIPES_CSV = "recipes.csv"

# Load Recipes
if os.path.exists(RECIPES_CSV):
    recipes_df = pd.read_csv(RECIPES_CSV)
else:
    st.warning("No recipes found. Please add recipes first on the Recipes page.")
    st.stop()

# ------------------------------
# Meal Planner Session Handling
# ------------------------------
if "meal_plan" not in st.session_state:
    st.warning("No meal plan found. Please create your meal plan first.")
    st.stop()

meal_plan = st.session_state.meal_plan

# ------------------------------
# Ingredient Aggregation
# ------------------------------
all_ingredients = []

for day, meals in meal_plan.items():
    for meal_name, recipe_name in meals.items():
        if recipe_name:
            matching = recipes_df[recipes_df["Recipe"] == recipe_name]
            all_ingredients.append(matching)

if not all_ingredients:
    st.info("Your meal plan doesn't contain any recipes yet.")
    st.stop()

full_df = pd.concat(all_ingredients, ignore_index=True)

# Clean and normalize
full_df["Ingredient"] = full_df["Ingredient"].str.strip().str.lower()
full_df["Quantity"] = pd.to_numeric(full_df["Quantity"], errors="coerce").fillna(0)

# Combine duplicates
grouped = full_df.groupby(["Ingredient", "Unit"], as_index=False)["Quantity"].sum()

# ------------------------------
# Display Shopping List
# ------------------------------
st.subheader("📋 Consolidated Shopping List")

if grouped.empty:
    st.info("Nothing to show yet.")
else:
    grouped = grouped.sort_values(by="Ingredient").reset_index(drop=True)
    st.table(grouped.rename(columns={"Ingredient": "Item", "Quantity": "Total", "Unit": "Unit"}))

# ------------------------------
# Export
# ------------------------------
csv_data = grouped.to_csv(index=False)
st.download_button(
    label="⬇️ Download Shopping List",
    data=csv_data,
    file_name="shopping_list.csv",
    mime="text/csv"
)
