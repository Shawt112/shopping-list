iimport pandas as pd
import streamlit as st
from collections import defaultdict

# Sample: Replace this with your actual recipes_df from your app
recipes_df = pd.read_csv("recipes.csv")  # or keep this from your state in Streamlit

# Sample: Simulated meal plan dictionary
meal_plan = {
    "Monday": {"Breakfast": "Porridge", "Lunch": "Salad", "Tea": "Pasta", "Snacks": "Fruit"},
    "Tuesday": {"Breakfast": "Toast", "Lunch": "Soup", "Tea": "Curry", "Snacks": "Yogurt"},
    # Extend as needed
}

# 🧠 Build shopping list
shopping_dict = defaultdict(lambda: defaultdict(float))  # {ingredient: {unit: total_quantity}}

for day_meals in meal_plan.values():
    for meal in day_meals.values():
        if not meal:
            continue
        matched_ingredients = recipes_df[recipes_df["Recipe"].str.strip().str.lower() == meal.strip().lower()]
        for _, row in matched_ingredients.iterrows():
            ingredient = row["Ingredient"].strip().lower()
            unit = row["Unit"].strip().lower()
            try:
                qty = float(row["Quantity"])
            except:
                qty = 0  # Handle non-numeric gracefully
            shopping_dict[ingredient][unit] += qty

# 🔄 Flatten to DataFrame
shopping_list = []
for ingredient, units in shopping_dict.items():
    for unit, total_qty in units.items():
        shopping_list.append({
            "Ingredient": ingredient.title(),
            "Quantity": total_qty,
            "Unit": unit
        })

shopping_df = pd.DataFrame(shopping_list).sort_values("Ingredient")

# 📋 Display shopping list
st.subheader("🛒 Generated Shopping List")
st.table(shopping_df.reset_index(drop=True))
