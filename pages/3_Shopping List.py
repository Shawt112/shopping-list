import streamlit as st
import pandas as pd
import os
import json

# -------------------- Page Config --------------------
st.set_page_config(page_title="Shopping List", page_icon="🛒", layout="centered")
st.title("🛒 Shopping List")

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
        recipes_df = pd.read_csv("recipes_cache.csv")
    else:
        st.error("No recipe data found. Please use the Recipes page first.")
        st.stop()

    # Ensure Notes column exists
    if "Notes" not in recipes_df.columns:
        recipes_df["Notes"] = ""

    st.session_state["recipes_df"] = recipes_df

recipes_df = st.session_state["recipes_df"]

# -------------------- Upload Existing Shopping List --------------------
st.subheader("📤 Upload Existing Shopping List (Optional)")
uploaded_file = st.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx"]
)

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        uploaded_df = pd.read_csv(uploaded_file)
    else:
        uploaded_df = pd.read_excel(uploaded_file)

    # Ensure Notes column exists
    if "Notes" not in uploaded_df.columns:
        uploaded_df["Notes"] = ""

    st.session_state["uploaded_items"] = uploaded_df

# -------------------- Collect Selected Recipes --------------------
selected_recipes = set()
for day_meals in meal_plan.values():
    selected_recipes.update(
        [m for m in day_meals.values() if m and m != "-"]
    )

# -------------------- Aggregate Ingredients --------------------
ingredients = recipes_df[
    recipes_df["Recipe"].isin(selected_recipes)
]

ingredients["Quantity"] = pd.to_numeric(
    ingredients["Quantity"], errors="coerce"
).fillna(0)

grouped = (
    ingredients
    .groupby(["Ingredient", "Unit"], as_index=False)["Quantity"]
    .sum()
    .sort_values(by="Ingredient")
)

# Add Notes column for recipe-based items
grouped["Notes"] = ""

# -------------------- Add Custom Items --------------------
st.subheader("➕ Add Your Own Item")

custom_ingredient = st.text_input("Ingredient")
custom_quantity = st.text_input("Quantity")
custom_unit = st.text_input("Unit")
custom_notes = st.text_input("Notes (optional)")

if st.button("Add Item"):
    if "custom_items" not in st.session_state:
        st.session_state["custom_items"] = []

    if custom_ingredient:
        st.session_state["custom_items"].append({
            "Ingredient": custom_ingredient,
            "Quantity": custom_quantity,
            "Unit": custom_unit,
            "Notes": custom_notes
        })
        st.success(f"Added {custom_ingredient}!")

# -------------------- Merge Custom Items --------------------
if "custom_items" in st.session_state and st.session_state["custom_items"]:
    custom_df = pd.DataFrame(st.session_state["custom_items"])

    custom_df["Quantity"] = pd.to_numeric(
        custom_df["Quantity"], errors="coerce"
    ).fillna(custom_df["Quantity"])

    grouped = pd.concat([grouped, custom_df], ignore_index=True)

# -------------------- Merge Uploaded Items --------------------
if "uploaded_items" in st.session_state:
    upload_df = st.session_state["uploaded_items"]

    for col in ["Ingredient", "Quantity", "Unit", "Notes"]:
        if col not in upload_df.columns:
            upload_df[col] = ""

    grouped = pd.concat([grouped, upload_df], ignore_index=True)

# -------------------- Display Shopping List --------------------
st.subheader("🧾 Combined Shopping List")

if grouped.empty:
    st.info("No items yet — add meals, upload a list, or add custom items.")
else:
    st.data_editor(
        grouped[["Ingredient", "Quantity", "Unit", "Notes"]],
        use_container_width=True,
        num_rows="dynamic"
    )

    # -------------------- Download CSV --------------------
    csv = grouped.to_csv(index=False)
    st.download_button(
        "📥 Download Shopping List as CSV",
        csv,
        "shopping_list.csv",
        "text/csv"
    )
