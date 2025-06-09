import streamlit as st
import pandas as pd

st.set_page_config(page_title="Shopping List", page_icon="🛒", layout="centered")

st.title("🛒 Shopping List")

# Check required session state data
if "weekly_plan" not in st.session_state or "recipes_df" not in st.session_state:
    st.error("Meal planner or recipe data not found. Please fill out the Meal Planner first.")
    st.stop()

meal_plan = st.session_state["weekly_plan"]
recipes_df = st.session_state["recipes_df"]

# Collect all selected recipes from the planner
selected_recipes = set()
for day_meals in meal_plan.values():
    for meal in day_meals.values():
        if meal and meal != "-":
            selected_recipes.add(meal)

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
