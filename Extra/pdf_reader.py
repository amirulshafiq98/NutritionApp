import camelot
import pandas as pd
import sys
import os

# --- FILE DEFINITIONS ---
# Ensure 'diet.pdf' is inside a folder named 'PDFs'
PDF_FILE_PATH = "PDFs/diet.pdf" 
EXCEL_OUTPUT_PATH = "HPB_Nutrient_Guidelines_Tables_FINAL.xlsx" 


def extract_all_tables_to_excel(pdf_path, output_excel_path):
    """
    Extracts all tables from a PDF using Camelot and saves them.
    Tries multiple flavors if one doesn't work.
    """
    try:
        print(f"-> Starting extraction from {pdf_path}...")
        
        tables = None
        flavors = ['stream', 'lattice']
        
        for flavor in flavors:
            print(f"   Trying flavor: {flavor}...")
            try:
                tables = camelot.read_pdf(
                    pdf_path, 
                    pages='3-29',
                    flavor=flavor,
                    strip_text='\n'
                )
                
                if tables and len(tables) > 0:
                    print(f"   ✅ Success with {flavor} flavor!")
                    break
            except Exception as e:
                print(f"   ❌ {flavor} failed: {e}")
                continue

        if not tables or len(tables) == 0:
            print("❌ Extraction failed: 0 tables found with any method.")
            return

        print(f"✅ Found {len(tables)} tables across the PDF.")

        # Create a Pandas Excel Writer object
        with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
            for i, table in enumerate(tables):
                page_number = table.page
                sheet_name = f'Page {page_number} - Table {i+1}'
                
                df = table.df
                df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
                print(f"    Saved Table {i+1} to sheet: {sheet_name}")

        print(f"\n✨ Successfully saved all tables to: {output_excel_path}")

    except Exception as e:
        print(f"\n🚨 A FATAL ERROR occurred: {e}")
        # Check for the PDF path as a common failure point
        if not os.path.exists(pdf_path):
            print(f"Error Detail: The input file '{pdf_path}' was not found. Please check the 'PDFs/' subfolder.")


if __name__ == "__main__":
    extract_all_tables_to_excel(PDF_FILE_PATH, EXCEL_OUTPUT_PATH)