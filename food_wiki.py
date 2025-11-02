# food_wiki.py

import streamlit as st
import pandas as pd
from pathlib import Path

DATA_FILE = "Food Wiki.xlsx"
# IMAGE_FOLDER = Path("data/images")

def show_food_wiki():
    st.header("Food Wiki")
    st.write("Search by food item or category to see nutrition info and labels.")

    # Load both sheets
    sheets = pd.read_excel(DATA_FILE, sheet_name=None)  # returns dict
    all_items = pd.concat(sheets.values(), ignore_index=True)

    # Search box
    query = st.text_input("Search food or category:")

    if query:
        # Filter where either 'Item' or 'Category' contains the query (case-insensitive)
        filtered = all_items[
            all_items['Item'].str.contains(query, case=False, na=False) |
            all_items['Category'].str.contains(query, case=False, na=False)
        ]
    else:
        filtered = all_items

    if filtered.empty:
        st.write("No results found.")
        return

    # Display list of results
    for idx, row in filtered.iterrows():
        st.subheader(f"{row['Item']} ({row['Category']})")
        st.write(f"Calories: {row.get('Calories', 'N/A')}")
        st.write(f"Sugar: {row.get('Sugar', 'N/A')}")
        st.write(f"Sodium: {row.get('Sodium', 'N/A')}")

        # Display image if exists
        # image_file = IMAGE_FOLDER / f"{row.get('Image', '')}.png"
        # if image_file.exists():
        #     st.image(str(image_file), width=100)
        # else:
        #     st.write("_No image available_")
