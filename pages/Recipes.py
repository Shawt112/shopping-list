import streamlit as st
import pandas as pd
import os
import re

st.set_page_config(page_title="Recipes", page_icon="🍽️", layout="centered")

st.title("🍽️ Recipes")
st.write("View, import, or add your own recipes with detailed ingredients.")

# File to store recipes persistently
CSV_FILE = "recipes.csv"

# Load existing recipes
if os.path.exists(CSV_FILE):
    recipes_df = pd.read_csv(CSV_FILE)
else:
    recipes_df = pd.DataFrame(columns=["Recipe", "Ingredient", "Quantity", "Unit"])

# ===========================
# 📚 Show Recipe Viewer
# ===========================
if not recipes_df.empty:
    st.subheader("📚 Available Recipes")
    recipe_names = recipes_df["Recipe"].unique().tolist()
    selected = st.selectbox("Choose a recipe to view ingredients", recipe_names)

# ===========================
# 📂 Upload CSV of Recipes
# ===========================
st.subheader("📂 Upload Recipes from CSV")
uploaded_file = st.file_uploader("Upload a CSV file with 'Recipe', 'Ingredient', 'Quantity', and 'Unit' columns", type=["csv"])
if uploaded_file:
    new_data = pd.read_csv(uploaded_file)
    if all(col in new_data.columns for col in ["Recipe", "Ingredient", "Quantity", "Unit"]):
        recipes_df = pd.concat([recipes_df, new_data], ignore_index=True).drop_duplicates()
        recipes_df.to_csv(CSV_FILE, index=False)
        st.success("Recipes uploaded and saved!")
        st.experimental_rerun()
    else:
        st.error("CSV must include 'Recipe', 'Ingredient', 'Quantity', and 'Unit' columns")

# ===========================
# ✍️ Add Recipe Form
# ===========================
st.subheader("✍️ Add a Custom Recipe")
with st.form("add_recipe_form"):
    custom_recipe = st.text_input("Recipe name")
    st.markdown("Enter ingredients one by one below:")

    ingredient_name = st.text_input("Ingredient")
    quantity = st.text_input("Quantity (e.g., 250)")
    unit = st.text_input("Unit (e.g., g, ml, tbsp)")

    submitted = st.form_submit_button("Add Ingredient to Recipe")

    if submitted:
        if not all([custom_recipe.strip(), ingredient_name.strip()]):
            st.warning("Recipe name and ingredient are required.")
        else:
            new_row = pd.DataFrame([{
                "Recipe": custom_recipe.strip(),
                "Ingredient": ingredient_name.strip(),
                "Quantity": quantity.strip(),
                "Unit": unit.strip()
            }])
            recipes_df = pd.concat([recipes_df, new_row], ignore_index=True).drop_duplicates()
            recipes_df.to_csv(CSV_FILE, index=False)
            st.success(f"Added ingredient to recipe: {custom_recipe}")
            st.experimental_rerun()

# ===========================
# 💾 Export Recipes to CSV
# ===========================
st.subheader("💾 Export Your Recipes")
st.download_button(
    label="📅 Download Recipes as CSV",
    data=recipes_df.to_csv(index=False),
    file_name="my_recipes.csv",
    mime="text/csv"
)

# ===========================
# 🍽️ Display Each Recipe with Edit/Delete Buttons
# ===========================
if not recipes_df.empty:
    st.subheader("📋 Manage Recipes")

    for recipe in recipes_df["Recipe"].unique():
        st.markdown(f"### 🍽️ {recipe}")

        recipe_data = recipes_df[recipes_df["Recipe"] == recipe].copy()
        recipe_data["Ingredient Detail"] = recipe_data.apply(
            lambda row: f"{row['Ingredient']} ({row['Quantity']} {row['Unit']})" if row["Quantity"] else row["Ingredient"],
            axis=1
        )
        display_table = recipe_data[["Ingredient Detail"]].reset_index(drop=True)
        st.table(display_table)

        col1, col2 = st.columns([1, 1])
        safe_recipe = re.sub(r'\W+', '_', recipe)

        with col1:
            if st.button(f"✏️ Edit {recipe}", key=f"edit_{safe_recipe}"):
                with st.expander(f"Edit ingredients for {recipe}", expanded=True):
                    ingredients = recipe_data["Ingredient"].tolist()
                    selected_ingredient = st.selectbox("Choose ingredient to edit", ingredients, key=f"dropdown_{safe_recipe}")

                    target_row = recipe_data[recipe_data["Ingredient"] == selected_ingredient]
                    if not target_row.empty:
                        idx = target_row.index[0]
                        row = target_row.iloc[0]
                        safe_ing = re.sub(r'\W+', '_', selected_ingredient)

                        with st.form(f"edit_form_{safe_recipe}_{safe_ing}"):
                            new_ing = st.text_input("Ingredient", value=row["Ingredient"])
                            new_qty = st.text_input("Quantity", value=str(row["Quantity"]))
                            new_unit = st.text_input("Unit", value=row["Unit"])
                            save = st.form_submit_button("📅 Save Changes")

                            if save:
                                recipes_df.loc[idx, ["Ingredient", "Quantity", "Unit"]] = [
                                    new_ing,
                                    new_qty,
                                    new_unit
                                ]
                                recipes_df.to_csv(CSV_FILE, index=False)
                                st.success(f"Updated '{new_ing}' in '{recipe}'")
                                st.experimental_rerun()

        with col2:
            if st.button(f"🗑️ Delete {recipe}", key=f"delete_{safe_recipe}"):
                recipes_df = recipes_df[recipes_df["Recipe"] != recipe]
                recipes_df.to_csv(CSV_FILE, index=False)
                st.warning(f"Deleted recipe: {recipe}")
                st.experimental_rerun()
