import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Recipes", page_icon="🍽️", layout="centered")

st.title("🍽️ Recipes")
st.write("View, import, or add your own recipes with ingredients.")

# File to store recipes persistently
CSV_FILE = "recipes.csv"

# Load existing recipes
if os.path.exists(CSV_FILE):
    recipes_df = pd.read_csv(CSV_FILE)
else:
    recipes_df = pd.DataFrame(columns=["Recipe", "Ingredient"])

# ===========================
# 📚 Show Recipe Viewer
# ===========================
if not recipes_df.empty:
    st.subheader("📚 Available Recipes")
    recipe_names = recipes_df["Recipe"].unique().tolist()
    selected = st.selectbox("Choose a recipe to view ingredients", recipe_names)
    
    st.markdown("### 📝 Ingredients")
    for ing in recipes_df[recipes_df["Recipe"] == selected]["Ingredient"]:
        st.checkbox(ing)

# ===========================
# 📂 Upload CSV of Recipes
# ===========================
st.subheader("📂 Upload Recipes from CSV")
uploaded_file = st.file_uploader("Upload a CSV file with 'Recipe' and 'Ingredient' columns", type=["csv"])
if uploaded_file:
    new_data = pd.read_csv(uploaded_file)
    if "Recipe" in new_data.columns and "Ingredient" in new_data.columns:
        recipes_df = pd.concat([recipes_df, new_data], ignore_index=True).drop_duplicates()
        recipes_df.to_csv(CSV_FILE, index=False)
        st.success("Recipes uploaded and saved!")
        st.experimental_rerun()
    else:
        st.error("CSV must have 'Recipe' and 'Ingredient' columns")

# ===========================
# ✍️ Add Recipe Form
# ===========================
st.subheader("✍️ Add a Custom Recipe")
with st.form("add_recipe_form"):
    custom_recipe = st.text_input("Recipe name")
    custom_ingredients = st.text_area("Ingredients (one per line)")
    submitted = st.form_submit_button("Add Recipe")

    if submitted:
        if not custom_recipe or not custom_ingredients.strip():
            st.warning("Please provide both recipe name and at least one ingredient.")
        else:
            ingredients = [i.strip() for i in custom_ingredients.splitlines() if i.strip()]
            new_rows = pd.DataFrame({
                "Recipe": [custom_recipe] * len(ingredients),
                "Ingredient": ingredients
            })
            recipes_df = pd.concat([recipes_df, new_rows], ignore_index=True).drop_duplicates()
            recipes_df.to_csv(CSV_FILE, index=False)
            st.success(f"Added recipe: {custom_recipe}")
            st.experimental_rerun()
