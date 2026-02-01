import streamlit as st
import pandas as pd
import os
import json

# -------------------- Page Config --------------------
st.set_page_config(page_title="Shopping List", page_icon="🛒", layout="centered")
st.title("🛒 Shopping List")

# -------------------- Session State Init --------------------
if "custom_items" not in st.session_state:
    st.session_state["custom_items"] = []

# -------------------- Load Weekly Plan --------------------
if "weekly_plan" not in st.session_state:
    if os.path.exists("weekly_plan.json"):
        with open("weekly_plan.json") as f:
            st.session_state["weekly_plan"] = json.load(f)
    else:
        st.error("No meal plan data found. Please use the Meal Planner first.")
        st.stop()

meal_plan = st.session_state["weekly_plan"]

# -------------------- Load Recipes --------------------
if "recipes_df" not in st.session_state:
    if os.path.exists("recipes_cache.csv"):
        st.session_state["recipes_df"] = pd.read_csv("recipes_cache.csv")
    else:
        st.error("No recipe data found. Please use the Recipes page first.")
        st.stop()

recipes_df = st.session_state["recipes_df"]

# -------------------- Collect Selected Recipes --------------------
selected_recipes = set()
for day_meals in meal_plan.values():
    selected_recipes.update(
        [m for m in day_meals.values() if m and m != "-"]
    )

# -------------------- Aggregate Ingredients --------------------
ingredients = recipes_df[recipes_df["Recipe"].isin(selected_recipes)]
ingredients["Quantity"] = pd.to_numeric(
    ingredients["Quantity"], errors="coerce"
).fillna(0)

grouped = (
    ingredients
    .groupby(["Ingredient", "Unit"], as_index=False)["Quantity"]
    .sum()
    .sort_values(by="Ingredient")
)

# -------------------- Add Custom Items (FORM) --------------------
st.subheader("➕ Add Your Own Item")

with st.form("add_item_form", clear_on_submit=True):
    custom_ingredient = st.text_input("Ingredient", key="ingredient_input")
    custom_quantity = st.text_input("Quantity", key="quantity_input")
    custom_unit = st.text_input("Unit", key="unit_input")

    submitted = st.form_submit_button("Add Item")

    if submitted and custom_ingredient:
        st.session_state["custom_items"].append({
            "Ingredient": custom_ingredient,
            "Quantity": custom_quantity,
            "Unit": custom_unit
        })
        st.success(f"Added {custom_ingredient} to your list!")

# -------------------- Merge Custom Items --------------------
if st.session_state["custom_items"]:
    custom_df = pd.DataFrame(st.session_state["custom_items"])

    custom_df["Quantity"] = pd.to_numeric(
        custom_df["Quantity"], errors="coerce"
    ).fillna(custom_df["Quantity"])

    grouped = pd.concat([grouped, custom_df], ignore_index=True)

# -------------------- Display Shopping List with Checkboxes --------------------
st.subheader("🧾 Combined Shopping List")

if grouped.empty:
    st.info("No ingredients to show.")
else:
    # Initialize checkbox state
    if "checked_items" not in st.session_state:
        st.session_state["checked_items"] = {}

    for idx, row in grouped.iterrows():
        item_name = f"{row['Ingredient']} - {row['Quantity']} {row['Unit']}"
        key = f"item_{idx}"  # unique key for each item

        # Get previous checkbox state
        checked = st.session_state["checked_items"].get(key, False)

        # Create checkbox
        checked_now = st.checkbox(
            "",  # empty label, we'll display the item with strikethrough
            value=checked,
            key=key
        )

        st.session_state["checked_items"][key] = checked_now

        # Display item name inline with strikethrough if checked
        if checked_now:
            st.markdown(f"~~{item_name}~~")
        else:
            st.markdown(item_name)
