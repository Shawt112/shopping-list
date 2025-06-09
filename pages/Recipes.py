import streamlit as st
import pandas as pd
import os

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
    
    st.markdown("### 📝 Ingredients")
    subset = recipes_df[recipes_df["Recipe"] == selected]
    for _, row in subset.iterrows():
        label = f"{row['Ingredient']} ({row['Quantity']} {row['Unit']})" if row['Quantity'] else row['Ingredient']
        st.checkbox(label)

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
    label="📥 Download Recipes as CSV",
    data=recipes_df.to_csv(index=False),
    file_name="my_recipes.csv",
    mime="text/csv"
)

# ===========================
# 🛠 Edit/Delete Recipes
# ===========================
st.subheader("🛠 Edit or Delete Ingredients")

edit_df = recipes_df.copy()
edit_df["Index"] = edit_df.index

# Display editable table with unique index
selected_row = st.selectbox("Select a row to edit/delete", options=edit_df["Index"], format_func=lambda i: f"{edit_df.loc[i, 'Recipe']} - {edit_df.loc[i, 'Ingredient']}")

selected_data = edit_df.loc[selected_row]

# Edit form
with st.form("edit_form"):
    new_recipe = st.text_input("Recipe", value=selected_data["Recipe"])
    new_ingredient = st.text_input("Ingredient", value=selected_data["Ingredient"])
    new_quantity = st.text_input("Quantity", value=selected_data["Quantity"])
    new_unit = st.text_input("Unit", value=selected_data["Unit"])

    col1, col2 = st.columns(2)
    with col1:
        save_btn = st.form_submit_button("💾 Save Changes")
    with col2:
        delete_btn = st.form_submit_button("🗑️ Delete")

    if save_btn:
        recipes_df.loc[selected_row] = [new_recipe, new_ingredient, new_quantity, new_unit]
        recipes_df.to_csv(CSV_FILE, index=False)
        st.success("Changes saved.")
        st.experimental_rerun()

    if delete_btn:
        recipes_df = recipes_df.drop(index=selected_row).reset_index(drop=True)
        recipes_df.to_csv(CSV_FILE, index=False)
        st.success("Ingredient deleted.")
        st.experimental_rerun()

# ===========================
# 📊 Separate Tables Per Recipe
# ===========================
if not recipes_df.empty:
    st.subheader("📊 Ingredients by Recipe")

    grouped = recipes_df.copy()
    grouped["Ingredient Detail"] = grouped.apply(
        lambda row: f"{row['Ingredient']} ({row['Quantity']} {row['Unit']})" if row['Quantity'] else row['Ingredient'],
        axis=1
    )

    for recipe in grouped["Recipe"].unique():
        st.markdown(f"### 🍽️ {recipe}")
        table_df = grouped[grouped["Recipe"] == recipe][["Ingredient Detail"]].rename(columns={"Ingredient Detail": "Ingredient"})
        st.table(table_df.reset_index(drop=True))

