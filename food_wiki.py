# food_wiki.py
import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image

# --- Configuration (Updated to read from Excel file) ---
EXCEL_FILE = "Food Wiki.xlsx"
FOOD_SHEET = "Food"
BEVERAGES_SHEET = "Beverages"
TAGLINE_SHEET = "Tagline"

BASE_IMAGE_FOLDER = Path(__file__).parent / "images" 


@st.cache
def load_data():
    """Loads data from the Excel file with three sheets."""
    try:
        # Load from Excel file sheets
        food_df = pd.read_excel(EXCEL_FILE, sheet_name=FOOD_SHEET)
        beverages_df = pd.read_excel(EXCEL_FILE, sheet_name=BEVERAGES_SHEET)
        tagline_df = pd.read_excel(EXCEL_FILE, sheet_name=TAGLINE_SHEET)
        
        # Prepare the Tagline lookup table
        tagline_lookup = tagline_df.set_index('Tag ID')
        
        # Set Category_Key to match your exact image folder names (Food, Beverage)
        food_df['Category_Key'] = 'Food'
        beverages_df['Category_Key'] = 'Beverage' 
        
        all_items = pd.concat([food_df, beverages_df], ignore_index=True)
        
        return all_items, tagline_lookup
    
    except FileNotFoundError as e:
        st.error(f"Error: Excel file '{EXCEL_FILE}' was not found. Please ensure it's in the same directory as this script.")
        return pd.DataFrame(), pd.DataFrame()
    except ValueError as e:
        st.error(f"Error: Sheet not found in Excel file. Check that sheets are named '{FOOD_SHEET}', '{BEVERAGES_SHEET}', and '{TAGLINE_SHEET}'. Error: {e}")
        return pd.DataFrame(), pd.DataFrame()
    except KeyError as e:
        st.error(f"Error: A required column or index was missing: {e}. Check your data columns (expecting 'Tag ID', 'Item', 'Type').")
        return pd.DataFrame(), pd.DataFrame()


def get_example_image_path(row, image_filename):
    """Constructs the full path for a product example image using the Category_Key (Food/Beverage)."""
    if pd.isna(image_filename):
        return None
    
    category = row.get('Category_Key', 'general') 
    return BASE_IMAGE_FOLDER / category / image_filename


def show_food_wiki():
    
    all_items, TAGLINE_LOOKUP = load_data()

    if all_items.empty and TAGLINE_LOOKUP.empty:
        return

    st.title("Food Wiki POC 🧪")
    st.write("Search for an item or category to view its labels and product examples.")
    
    # Debug info (remove this later)
    with st.expander("🔍 Debug Info - Click to see file paths"):
        st.write(f"Base image folder: `{BASE_IMAGE_FOLDER}`")
        st.write(f"Folder exists: {BASE_IMAGE_FOLDER.exists()}")
        if BASE_IMAGE_FOLDER.exists():
            st.write("Subfolders found:")
            for subfolder in BASE_IMAGE_FOLDER.iterdir():
                if subfolder.is_dir():
                    st.write(f"  - `{subfolder.name}/` ({len(list(subfolder.glob('*')))} files)")
        st.write(f"Total items loaded: {len(all_items)}")

    query = st.text_input("Search food or category:")

    if query:
        filtered = all_items[
            all_items['Item'].astype(str).str.contains(query, case=False, na=False) |
            all_items['Type'].astype(str).str.contains(query, case=False, na=False)
        ]
    else:
        filtered = all_items

    if filtered.empty:
        st.error("No results found. Try a different search term.")
        return

    # Display list of results
    for idx, row in filtered.iterrows():
        item_type = row.get('Type') if pd.notna(row.get('Type')) else 'N/A'
        st.subheader(f"{row['Item']} ({item_type})")
        
        # Debug: Show what we're looking for
        with st.expander("🐛 Debug - Image paths for this item"):
            st.write(f"Category_Key: {row.get('Category_Key')}")
            st.write(f"Tag ID raw: {row.get('Tag ID')}")
            st.write(f"Example 1: {row.get('Example 1')}")
            st.write(f"Example 2: {row.get('Example 2')}")
            st.write(f"Example 3: {row.get('Example 3')}") 
        
        # --- 1. Display Tagline(s) and Icon(s) ---
        tag_ids_str = row.get('Tag ID')
        if pd.notna(tag_ids_str):
            # Split by comma and strip whitespace
            tag_ids = [tid.strip() for tid in str(tag_ids_str).split(',') if tid.strip()]
            
            if tag_ids:
                st.write("**Health Labels:**")
                cols = st.columns(len(tag_ids))
                
                for i, tag_id in enumerate(tag_ids):
                    # Convert tag_id to string to match index
                    tag_id_str = str(tag_id)
                    if tag_id_str in TAGLINE_LOOKUP.index.astype(str):
                        tag_details = TAGLINE_LOOKUP.loc[tag_id_str]
                        tagline = tag_details['Tagline']
                        
                        # Tagline images are in the 'Signs' subfolder
                        tagline_image_file = BASE_IMAGE_FOLDER / "Signs" / tag_details['Tagline Image']
                        
                        with cols[i]:
                            if tagline_image_file.exists():
                                try:
                                    img = Image.open(tagline_image_file)
                                    st.image(img, caption=tagline, width=70)
                                except Exception as e:
                                    st.error(f"Error: {e}")
                            else:
                                st.markdown(f"**[{tagline}]** ❌")


        # --- 2. Display 3 Product Examples in a collapsible section ---
        with st.expander("Click to see 3 Product Examples"):
            
            col1, col2, col3 = st.columns(3)
            image_cols = ['Example 1', 'Example 2', 'Example 3']
            
            for i, col in enumerate([col1, col2, col3]):
                image_file = row.get(image_cols[i])
                
                with col:
                    if pd.notna(image_file):
                        full_path = get_example_image_path(row, image_file)
                        
                        if full_path and full_path.exists():
                            try:
                                img = Image.open(full_path)
                                st.image(img, caption=f"Example {i+1}", width=150)
                            except Exception as e:
                                st.error(f"Cannot load image: {type(e).__name__}: {e}")
                                st.write(f"File: `{image_file}`")
                        else:
                            st.markdown(f"❌ Missing: `{image_file}`")
                    else:
                        st.write(f"No example")

        # Display other nutrition info
        item_category = row.get('Category_Key')
        
        st.markdown("### Other Nutrition Info")
        col1, col2 = st.columns(2)
        
        # Define a dictionary to hold the data labels and values
        data = {}

        if item_category == 'Food':
            # Food-specific nutrition data
            data = {
                "Calories/Serving:": row.get('Calories/Serving', 'N/A'),
                "Fat (g/100g):": row.get('Fat (g/100g)', 'N/A'),
                "Sugar (g/100mg):": row.get('Sugar (g/100mg)', 'N/A'),
                "Saturated Fat (g/100mg):": row.get('Saturated fat (g/100mg)', 'N/A'),
                "Sodium (mg/100mg):": row.get('Sodium (mg/100mg)', 'N/A'),
                "Dietary Fibre (g/100g):": row.get('Dietary Fibre (g/100g)', 'N/A'),
                "Calcium (mg/100mg):": row.get('Calcium (mg/100mg)', 'N/A'),
                "Potassium (mg/100g):": row.get('Potassium (mg/100g)', 'N/A'),
                "% Wholegrain:": row.get('% Wholegrain', 'N/A')
            }
        
        elif item_category == 'Beverage':
            # Beverage-specific nutrition data
            data = {
                "Sugar (g/100ml):": row.get('Sugar (g/100ml)', 'N/A'),
                "Saturated Fat (g/100ml):": row.get('Saturated fat (g/100ml)', 'N/A'),
                "Sodium (mg/100ml):": row.get('Sodium (mg/100ml)', 'N/A'),
                "Calcium (mg/100ml):": row.get('Calcium (mg/100ml)', 'N/A'),
                "% Wholegrain:": row.get('% Wholegrain', 'N/A')
            }
        
        else:
            # Fallback for unknown category
            st.warning(f"Nutrition data not defined for category: {item_category}")
            
        
        # Display the selected data using the two columns (for right alignment)
        if data:
            with col1:
                # Print all labels in the first column (left-aligned by default)
                for label in data.keys():
                    st.write(label)

            with col2:
                # Print all values in the second column, using HTML to right-align the text
                for value in data.values():
                    # Using st.markdown with HTML for right alignment
                    st.markdown(f"<p style='text-align: right;'>{value}</p>", unsafe_allow_html=True)
                
        st.markdown("---")

if __name__ == "__main__":
    show_food_wiki()