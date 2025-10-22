import streamlit as st
import os
import pandas as pd
import numpy as np
from dashboard import show_dashboard

# Page configuration
st.set_page_config(page_title="Risk Management Dashboard", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    header {
        visibility: visible !important;
    }
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: white;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .risk-table {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .summary-box {
        background-color: #e8e8e8;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .survey-card {
        background-color: white;
        padding: 8px;
        border-radius: 6px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 8px;
    }
    .grc-card {
        background-color: white;
        padding: 8px;
        border-radius: 6px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 8px;
    }
    .grc-number {
        font-size: 32px;
        color: #ff6347;
        font-weight: bold;
        margin: 5px 0;
    }
    .survey-number {
        font-size: 24px;
        font-weight: bold;
        color: #333;
        margin: 5px 0;
    }
    .survey-label {
        color: #999;
        font-size: 12px;
    }
    h1 {
        font-size: 28px !important;
        margin-bottom: 0.5rem !important;
        padding: 0 !important;
    }
    h3 {
        font-size: 18px !important;
        margin: 0.5rem 0 !important;
    }
    h4 {
        font-size: 14px !important;
        margin: 0.3rem 0 !important;
    }
    .stButton button {
        width: 100%;
        height: 35px;
        padding: 5px;
        font-size: 13px;
    }
    div[data-testid="stSelectbox"] {
        margin-bottom: 0.5rem;
    }
    .element-container {
        margin-bottom: 0.3rem;
    }
    [data-testid="stTextArea"] textarea {
        height: 100px !important;
        min-height: 100px !important;
    }
    .nav-button {
        background-color: #20B2AA;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'menu'
if 'df_ytd' not in st.session_state:
    st.session_state.df_ytd = None
if 'df_summary' not in st.session_state:
    st.session_state.df_summary = None
if 'df_summary_present' not in st.session_state:
    st.session_state.df_summary_present = None
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'latest_col_ytd_idx' not in st.session_state:
    st.session_state.latest_col_ytd_idx = None
if 'latest_col_idx' not in st.session_state:
    st.session_state.latest_col_idx = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Auto-load dummy data on first run
if not st.session_state.data_loaded:
    dummy_file_path = "dummy_data_2024_2025.xlsx"

    if os.path.exists(dummy_file_path):
        try:
            # Read Data_YTD sheet
            df_ytd = pd.read_excel(dummy_file_path, sheet_name="Data_YTD")

            # Set Parameter column
            if 'Unnamed: 1' in df_ytd.columns:
                df_ytd = df_ytd.rename(columns={'Unnamed: 1': 'Parameter'})

            # Find the latest non-empty column
            first_row = df_ytd.iloc[0]
            non_null_cols = [col for col in df_ytd.columns if col != 'Parameter' and col != 'Unnamed: 0' and pd.notna(first_row[col])]

            if non_null_cols:
                latest_col_ytd_idx = non_null_cols[-1]
            else:
                latest_col_ytd_idx = None

            # Read Summary sheet
            df_summary = pd.read_excel(dummy_file_path, sheet_name="Summary")

            # Find the latest data columns in summary
            if 'Jenis Risiko' in df_summary.columns:
                # Get the last 6 columns (2 months x 3 columns each)
                summary_cols = [col for col in df_summary.columns if col not in ['Unnamed: 0', 'Jenis Risiko']]

                if len(summary_cols) >= 6:
                    latest_col_idx = len(df_summary.columns) - 3
                    prev_col_idx = len(df_summary.columns) - 6

                    latest_col = df_summary.columns[latest_col_idx]
                    previous_col = df_summary.columns[prev_col_idx]

                    df_summary_present = df_summary[['Jenis Risiko', previous_col, latest_col]].copy()
                    df_summary_present.columns = ['Kategori Risiko', 'previous_month', 'present_month']
                else:
                    df_summary_present = None
                    latest_col_idx = None
            else:
                df_summary_present = None
                latest_col_idx = None

            # Store in session state
            st.session_state.df_ytd = df_ytd
            st.session_state.df_summary = df_summary
            st.session_state.df_summary_present = df_summary_present
            st.session_state.latest_col_idx = latest_col_idx
            st.session_state.latest_col_ytd_idx = latest_col_ytd_idx
            st.session_state.data_loaded = True

        except Exception as e:
            # Show error for debugging
            st.session_state.load_error = str(e)

def main():
    """Main function to control navigation"""

    # Sidebar navigation
    with st.sidebar:
        st.image("Logo.png")

        st.title("Navigation")

        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'menu'
            st.rerun()

        if st.button("📊 View Dashboard", use_container_width=True):
            if st.session_state.df_ytd is not None and st.session_state.df_summary_present is not None:
                st.session_state.page = 'dashboard'
                st.rerun()
            else:
                st.warning("Please upload data first!")

        st.divider()

        # Data status
        st.subheader("Data Status")
        if st.session_state.df_ytd is not None and st.session_state.df_summary is not None:
            st.success("✅ Data loaded")
        else:
            st.warning("⚠️ No data loaded")

    # Main content area
    if st.session_state.page == 'menu':
        st.title("🏠 Risk Management System")
        st.write("Welcome to the Risk Management Dashboard")
        st.write("")

        # Auto-navigate to dashboard if data is loaded
        if st.session_state.df_ytd is not None and st.session_state.df_summary_present is not None:
            if st.button("📊 View Dashboard", use_container_width=True, key="menu_dashboard"):
                st.session_state.page = 'dashboard'
                st.rerun()
        else:
            st.error("⚠️ Data not loaded. Please ensure 'dummy_data_2024_2025.xlsx' exists in the application directory.")
            st.info("Expected file: dummy_data_2024_2025.xlsx")
            if hasattr(st.session_state, 'load_error'):
                st.error(f"Load Error: {st.session_state.load_error}")

    elif st.session_state.page == 'dashboard':
        show_dashboard()

if __name__ == "__main__":
    main()
