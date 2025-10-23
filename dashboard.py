import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils import format_value, format_percentage, null_value

def show_dashboard():
    """Display the risk management dashboard"""

    # Check if data is loaded
    if st.session_state.df_summary is None or st.session_state.df_summary_present is None:
        st.error("No data loaded. Please upload data first.")
        return

    # Header
    st.title("Risk Management Dashboard")

    # Legend in horizontal layout
    with st.container(border=True):
        st.markdown("#### Legend")
        st.markdown('''
            <div style="display: flex; justify-content: space-around; align-items: center;">
                <span><span style="color: #90d050; font-size: 20px;">●</span> Low</span>
                <span><span style="color: #fff2cc; font-size: 20px;">●</span> Low to Moderate</span>
                <span><span style="color: #ffff00; font-size: 20px;">●</span> Moderate</span>
                <span><span style="color: #ffc001; font-size: 20px;">●</span> Moderate to High</span>
                <span><span style="color: #ff0000; font-size: 20px;">●</span> High</span>
            </div>
        ''', unsafe_allow_html=True)

    # Date selector
    date_col1, date_col2 = st.columns([1, 5])
    selected_date = None
    with date_col1:
        if st.session_state.latest_col_ytd_idx and st.session_state.df_ytd is not None:
            # Get columns up to latest_col_ytd_idx, excluding 'Parameter' and 'Unnamed' columns
            temp_col_position = st.session_state.df_ytd.columns.get_loc(st.session_state.latest_col_ytd_idx)
            available_dates = [col for col in st.session_state.df_ytd.columns[:temp_col_position+1]
                             if col != 'Parameter' and not str(col).startswith('Unnamed')]
            if available_dates:
                selected_date = st.selectbox(
                    "Select Date",
                    options=available_dates,
                    index=len(available_dates) - 1
                )
            else:
                st.warning("No dates available")
        else:
            st.warning("No dates available")

    # Get latest_col_ytd_idx from selected_date or session state
    if selected_date and st.session_state.df_ytd is not None:
        latest_col_ytd_idx = selected_date
        col_position = st.session_state.df_ytd.columns.get_loc(selected_date)
    elif st.session_state.latest_col_ytd_idx:
        latest_col_ytd_idx = st.session_state.latest_col_ytd_idx
        col_position = st.session_state.df_ytd.columns.get_loc(latest_col_ytd_idx)
    else:
        latest_col_ytd_idx = None
        col_position = None

    # Calculate latest_col_idx based on col_position
    # Map col_position from df_ytd to df_summary (assuming 3 columns per date in summary)
    if col_position is not None and st.session_state.df_summary is not None:
        # Find the column index in df_summary where column name contains selected_date
        # Handle abbreviated month names (e.g., Apr-2025 matches April-2025)
        month_mapping = {
            'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 'Apr': 'April',
            'May': 'May', 'Jun': 'June', 'Jul': 'July', 'Aug': 'August',
            'Sep': 'September', 'Oct': 'October', 'Nov': 'November', 'Dec': 'December'
        }

        def month_match(selected, col_name):
            """Check if selected_date matches col_name, handling abbreviated months"""
            selected_str = str(selected)
            col_str = str(col_name)

            # Direct substring match
            if selected_str in col_str:
                return True

            # Check for abbreviated month matching full month
            for abbr, full in month_mapping.items():
                if abbr in selected_str and full in col_str:
                    # Replace abbreviated month with full month and check
                    expanded = selected_str.replace(abbr, full)
                    if expanded in col_str:
                        return True
                # Also check reverse: if full month in selected and abbr in column
                if full in selected_str and abbr in col_str:
                    abbreviated = selected_str.replace(full, abbr)
                    if abbreviated in col_str:
                        return True

            return False

        matching_cols = np.where([month_match(selected_date, col) for col in st.session_state.df_summary.columns])[0]
        if len(matching_cols) > 0:
            latest_col_idx = int(matching_cols[-3])  # Get the last matching column
            prev_col_idx = latest_col_idx-3
        else:
            # Fallback calculation
            latest_col_idx = (col_position * 3) + 2
            prev_col_idx = latest_col_idx - 3

        # Ensure the index is within bounds
        if latest_col_idx >= len(st.session_state.df_summary.columns):
            latest_col_idx = len(st.session_state.df_summary.columns) - 1
            prev_col_idx = latest_col_idx - 3
    else:
        # Fallback: calculate from df_summary statically
        df_numpy = st.session_state.df_summary.to_numpy()
        row_0_numpy = df_numpy[0]
        nan_mask = row_0_numpy == '-'
        if nan_mask.any():
            nan_indices = int(np.where(nan_mask)[0][0])
            latest_col_idx = nan_indices - 3
            prev_col_idx = nan_indices - 6
        else:
            latest_col_idx = st.session_state.latest_col_idx if st.session_state.latest_col_idx else len(st.session_state.df_summary.columns) - 1
            prev_col_idx = latest_col_idx - 3

    # Calculate summary column indices based on selected date
    if st.session_state.df_summary is not None and latest_col_idx is not None:
        try:
            # Ensure indices are valid
            if prev_col_idx >= 0 and latest_col_idx < len(st.session_state.df_summary.columns):
                present_month_col = st.session_state.df_summary.columns[latest_col_idx]
                prev_month_col = st.session_state.df_summary.columns[prev_col_idx]

                # Check if 'Jenis Risiko' column exists
                if 'Jenis Risiko' in st.session_state.df_summary.columns:
                    df_summary_display = st.session_state.df_summary[['Jenis Risiko', prev_month_col, present_month_col]].copy()
                    df_summary_display.columns = ['Kategori Risiko', 'previous_month', 'present_month']
                else:
                    # Use first column as risk category
                    df_summary_display = st.session_state.df_summary.iloc[:, [0, prev_col_idx, latest_col_idx]].copy()
                    df_summary_display.columns = ['Kategori Risiko', 'previous_month', 'present_month']
            else:
                # Fallback to session state
                df_summary_display = st.session_state.df_summary_present
        except Exception as e:
            # Fallback to session state
            df_summary_display = st.session_state.df_summary_present
    else:
        # Fallback to session state
        df_summary_display = st.session_state.df_summary_present

    col_summary, col_nps= st.columns([3, 2])

    with col_summary:
        st.markdown('<div class="risk-table">', unsafe_allow_html=True)

        if df_summary_display is not None:
            def color_cells(val):
                try:
                    val_float = float(val)
                    if val_float <= 1.79:
                        return 'background-color: #90d050'
                    elif val_float <= 2.59:
                        return 'background-color: #fff2cc'
                    elif val_float <= 3.39:
                        return 'background-color: #ffff00'
                    elif val_float <= 4.19:
                        return 'background-color: #ffc001'
                    elif val_float <= 5:
                        return 'background-color: #ff0000'
                    else:
                        return ''
                except:
                    return ''

            # Format only numeric columns to 2 decimal places
            format_dict = {}
            for col in df_summary_display.columns:
                if col in ['previous_month', 'present_month']:
                    format_dict[col] = lambda x: f'{x:.2f}' if pd.notna(x) and isinstance(x, (int, float)) else '-'

            styled_df = df_summary_display[:9].style.map(
                color_cells,
                subset=['previous_month', 'present_month']
            ).format(
                format_dict
            ).set_properties(
                **{'text-align': 'center'}
            ).set_table_styles([
                {'selector': 'th', 'props': [('text-align', 'center')]}
            ])
            st.dataframe(styled_df, hide_index=True, use_container_width=True, height=350)
        else:
            st.warning("No data available. Please upload data first.")

        st.markdown('</div>', unsafe_allow_html=True)

    with col_nps:
        # Safely get the composite score from dynamic display data
        try:
            composite_score = float(df_summary_display['present_month'].iloc[10])
        except:
            composite_score = 0.0

        # Display selected date or latest date
        display_date = selected_date if selected_date else (st.session_state.latest_col_ytd_idx if st.session_state.latest_col_ytd_idx else "N/A")
        st.markdown(f"<p style='text-align: center;'><strong>Average Risk</strong><br>Composite Score in {display_date} is {composite_score:.2f}</p>", unsafe_allow_html=True)

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=composite_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={'font': {'size': 32}},
            gauge={
                'axis': {'range': [None, 5], 'tickwidth': 2},
                'bar': {'color': "black", 'thickness': 0.3},
                'bgcolor': "white",
                'borderwidth': 2,
                'steps': [
                    {'range': [0, 1.80], 'color': '#90d050'},
                    {'range': [1.80, 2.60], 'color': '#fff2cc'},
                    {'range': [2.60, 3.40], 'color': '#ffff00'},
                    {'range': [3.40, 4.20], 'color': '#ffc001'},
                    {'range': [4.20, 5], 'color': '#ff0000'}
                ],
            }
        ))
        fig.update_layout(height=280, margin=dict(l=20, r=20, t=0, b=20))
        st.plotly_chart(fig, use_container_width=True, key="nps_gauge")

    # Dropdown for risk type
    risk_types = ["Keseluruhan Risiko"]
    if 'Jenis Risiko' in st.session_state.df_summary.columns:
        risk_types.extend(st.session_state.df_summary['Jenis Risiko'][:9].tolist())

    st.selectbox("Select Risk Type", risk_types, label_visibility="collapsed")

    # Financial Metrics Section
    titles = ["Jumlah Aset", "Jumlah Utang", "Jumlah Ekuitas", "Jumlah Polis", "Kas dan Bank", "Aset Investasi", "RBC"]

    # Create 7 columns: 6 equal-sized, 1 larger for RBC
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1, 1, 1.5])
    cols = [col1, col2, col3, col4, col5, col6, col7]
    value_idx = [9,14,15,116,5,0,51]

    # Display all 7 containers
    for i, col in enumerate(cols):
        with col:
            with st.container(border=True):
                # Display title
                st.markdown(f"<div style='text-align: center; color: #999; font-size: 12px;'>{titles[i]}</div>", unsafe_allow_html=True)
                # Get value from df_ytd - need to access the data column (Unnamed: X) not the month column
                if st.session_state.df_ytd is not None and latest_col_ytd_idx:
                    try:
                        # Get the column position of the month name, then get the next column (data column)
                        col_position = st.session_state.df_ytd.columns.get_loc(latest_col_ytd_idx)
                        data_col = st.session_state.df_ytd.columns[col_position + 1]  # Next column contains the data
                        value = st.session_state.df_ytd[data_col].iloc[value_idx[i]]

                        # Format value for display (except RBC which stays as percentage)
                        if i == 6:  # RBC - display as percentage
                            formatted_value = format_percentage(value)
                            st.markdown(f"<div style='text-align: center; font-size: 32px; font-weight: bold; color: #ff6347; margin: 5px 0;'>{formatted_value}</div>", unsafe_allow_html=True)
                            st.markdown("<div style='text-align: center; color: #666; font-size: 11px; margin-top: 5px;'>Minimal 120% dari OJK</div>", unsafe_allow_html=True)
                        else:  # Format other values in mil/bil
                            formatted_value = format_value(value)
                            st.markdown(f"<div style='text-align: center; font-size: 24px; font-weight: bold; color: #333; margin: 5px 0;'>{formatted_value}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown("<div style='text-align: center; font-size: 24px; font-weight: bold; color: #333; margin: 5px 0;'>-</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='text-align: center; font-size: 24px; font-weight: bold; color: #333; margin: 5px 0;'>-</div>", unsafe_allow_html=True)

    # Line Graphs and Pie Charts Section
    col_graphs, col_pies = st.columns(2)

    # Fixed data for line charts (independent of month selection to prevent errors)
    fixed_line_data = {
        'months': ['Sep-2024', 'Oct-2024', 'Nov-2024', 'Dec-2024', 'Jan-2025', 'Feb-2025',
                   'Mar-2025', 'Apr-2025', 'May-2025', 'Jun-2025', 'Jul-2025', 'Aug-2025'],
        'Jumlah Pendapatan': [740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960],
        'Premi Bruto (All)': [670, 690, 710, 730, 750, 770, 790, 810, 830, 850, 870, 890],
        'Klaim Bruto (All)': [390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500],
        'Total Laba (Rugi) Komprehensif': [190, 195, 200, 205, 210, 215, 220, 225, 230, 235, 240, 245]
    }

    # Fixed data for pie charts (independent of month selection)
    fixed_pie_data = {
        'Deposito Berjangka': 1740.00,
        'Obligasi Korporasi': 970.00,
        'Surat Berharga yang Diterbitkan oleh Negara RI': 720.00,
        'Reksa Dana': 370.75
    }

    # First column - Line Graphs with Tabs
    with col_graphs:
        # Line graph titles
        line_titles = ["Jumlah Pendapatan", "Premi Bruto (All)", "Klaim Bruto (All)", "Total Laba (Rugi) Komprehensif"]

        # Create tabs
        tabs_line = st.tabs(["All Graphs", line_titles[0], line_titles[1], line_titles[2], line_titles[3]])

        # Use fixed data for line charts
        try:
            # Tab 0: All Graphs - 2x2 Grid Layout
            with tabs_line[0]:
                # First row - 2 columns
                col1_row1, col2_row1 = st.columns(2)

                # Graph 1: Jumlah Pendapatan (left column, row 1)
                with col1_row1:
                    try:
                        dates = fixed_line_data['months']
                        values = fixed_line_data['Jumlah Pendapatan']

                        fig_line = go.Figure()
                        fig_line.add_trace(go.Scatter(
                            x=dates, y=values, mode='lines+markers',
                            name=line_titles[0], line=dict(width=2), marker=dict(size=6)
                        ))
                        fig_line.update_layout(
                            title=line_titles[0], height=250,
                            margin=dict(l=40, r=20, t=40, b=30),
                            xaxis=dict(showgrid=True), yaxis=dict(showgrid=True),
                            plot_bgcolor='white'
                        )
                        st.plotly_chart(fig_line, use_container_width=True, key="line_all_0")
                    except Exception as e:
                        st.warning(f"Unable to load data for {line_titles[0]}: {str(e)}")

                # Graph 2: Premi Bruto (right column, row 1)
                with col2_row1:
                    try:
                        dates = fixed_line_data['months']
                        values = fixed_line_data['Premi Bruto (All)']

                        fig_line = go.Figure()
                        fig_line.add_trace(go.Scatter(
                            x=dates, y=values, mode='lines+markers',
                            name=line_titles[1], line=dict(width=2), marker=dict(size=6)
                        ))
                        fig_line.update_layout(
                            title=line_titles[1], height=250,
                            margin=dict(l=40, r=20, t=40, b=30),
                            xaxis=dict(showgrid=True), yaxis=dict(showgrid=True),
                            plot_bgcolor='white'
                        )
                        st.plotly_chart(fig_line, use_container_width=True, key="line_all_1")
                    except Exception as e:
                        st.warning(f"Unable to load data for {line_titles[1]}: {str(e)}")

                # Second row - 2 columns
                col1_row2, col2_row2 = st.columns(2)

                # Graph 3: Klaim Bruto (left column, row 2)
                with col1_row2:
                    try:
                        dates = fixed_line_data['months']
                        values = fixed_line_data['Klaim Bruto (All)']

                        fig_line = go.Figure()
                        fig_line.add_trace(go.Scatter(
                            x=dates, y=values, mode='lines+markers',
                            name=line_titles[2], line=dict(width=2), marker=dict(size=6)
                        ))
                        fig_line.update_layout(
                            title=line_titles[2], height=250,
                            margin=dict(l=40, r=20, t=40, b=30),
                            xaxis=dict(showgrid=True), yaxis=dict(showgrid=True),
                            plot_bgcolor='white'
                        )
                        st.plotly_chart(fig_line, use_container_width=True, key="line_all_2")
                    except Exception as e:
                        st.warning(f"Unable to load data for {line_titles[2]}: {str(e)}")

                # Graph 4: Laba Rugi Komprehensif (right column, row 2)
                with col2_row2:
                    try:
                        dates = fixed_line_data['months']
                        values = fixed_line_data['Total Laba (Rugi) Komprehensif']

                        fig_line = go.Figure()
                        fig_line.add_trace(go.Scatter(
                            x=dates, y=values, mode='lines+markers',
                            name=line_titles[3], line=dict(width=2), marker=dict(size=6)
                        ))
                        fig_line.update_layout(
                            title=line_titles[3], height=250,
                            margin=dict(l=40, r=20, t=40, b=30),
                            xaxis=dict(showgrid=True), yaxis=dict(showgrid=True),
                            plot_bgcolor='white'
                        )
                        st.plotly_chart(fig_line, use_container_width=True, key="line_all_3")
                    except Exception as e:
                        st.warning(f"Unable to load data for {line_titles[3]}: {str(e)}")

            # Tabs 1-4: Individual Graphs
            for tab_idx in range(1, 5):
                with tabs_line[tab_idx]:
                    try:
                        title = line_titles[tab_idx - 1]
                        dates = fixed_line_data['months']
                        values = fixed_line_data[title]

                        fig_line = go.Figure()
                        fig_line.add_trace(go.Scatter(
                            x=dates,
                            y=values,
                            mode='lines+markers',
                            name=title,
                            line=dict(width=3),
                            marker=dict(size=8)
                        ))
                        fig_line.update_layout(
                            title=title,
                            height=450,
                            margin=dict(l=40, r=20, t=40, b=30),
                            xaxis=dict(showgrid=True),
                            yaxis=dict(showgrid=True),
                            plot_bgcolor='white'
                        )
                        st.plotly_chart(fig_line, use_container_width=True, key=f"line_single_{tab_idx}")
                    except Exception as e:
                        st.warning(f"Unable to load data: {str(e)}")
        except Exception as e:
            st.warning(f"Unable to load line graph data: {str(e)}")

    # Second column - Pie Charts with Tabs
    with col_pies:
        # Pie chart titles
        pie_titles = ["Deposito Berjangka", "Obligasi Korporasi", "Surat Berharga yang Diterbitkan oleh Negara RI", "Reksa Dana"]

        # Create tabs
        tabs_pie = st.tabs(["All Graphs", pie_titles[0], pie_titles[1], pie_titles[2], pie_titles[3]])

        # Use fixed data for pie charts
        try:
            # Tab 0: All Graphs - Single Pie Chart with All Categories
            with tabs_pie[0]:
                try:
                    # Get values for all four categories from fixed data
                    labels = list(fixed_pie_data.keys())
                    values_pie = list(fixed_pie_data.values())

                    # Create pie chart with all four categories
                    fig_pie = go.Figure(data=[go.Pie(
                        labels=labels,
                        values=values_pie,
                        hole=0.3,
                        textinfo='label+percent',
                        textposition='auto'
                    )])
                    fig_pie.update_layout(
                        title="Distribusi Portfolio Investasi",
                        height=450,
                        margin=dict(l=10, r=10, t=40, b=120),
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.4,
                            xanchor="center",
                            x=0.5
                        )
                    )
                    st.plotly_chart(fig_pie, use_container_width=True, key="pie_all_combined")
                except Exception as e:
                    st.warning(f"Unable to load pie chart data: {str(e)}")

            # Tabs 1-4: Individual Pie Charts - Full portion of each investment type
            for tab_idx in range(1, 5):
                with tabs_pie[tab_idx]:
                    try:
                        title = pie_titles[tab_idx - 1]
                        value_float = fixed_pie_data[title]

                        # Create full pie chart showing 100% of this investment type
                        labels = [title]
                        values_pie = [100]  # Full 100% pie

                        fig_pie = go.Figure(data=[go.Pie(
                            labels=labels,
                            values=values_pie,
                            hole=0.3,
                            textinfo='label+value',
                            textposition='inside',
                            text=[f"{value_float}"]
                        )])
                        fig_pie.update_layout(
                            title=f"{title}: {value_float}",
                            height=450,
                            margin=dict(l=20, r=20, t=40, b=20),
                            showlegend=False
                        )
                        st.plotly_chart(fig_pie, use_container_width=True, key=f"pie_single_{tab_idx}")
                    except Exception as e:
                        st.warning(f"Unable to load data: {str(e)}")
        except Exception as e:
            st.warning(f"Unable to load pie chart data: {str(e)}")

    # Additional Metrics Section - 3 columns with multiple rows
    col_a, col_b, col_c = st.columns(3)
    value_idx = [139,141,143]

    # First column - 3 rows
    with col_a:
        titles_col_a = ["Jumlah Pengaduan", "Indak Lanjut Pengaduan", "Jumlah Pemberitaan Negatif Dalam 1 Tahun"]
        for i, title in enumerate(titles_col_a):
            with st.container(border=True):
                st.markdown(f"<div style='text-align: center; color: #999; font-size: 12px;'>{title}</div>", unsafe_allow_html=True)
                if st.session_state.df_ytd is not None and latest_col_ytd_idx:
                    try:
                        # Get the data column (next column after month name)
                        col_position = st.session_state.df_ytd.columns.get_loc(latest_col_ytd_idx)
                        data_col = st.session_state.df_ytd.columns[col_position + 1]
                        value = null_value(st.session_state.df_ytd[data_col].iloc[value_idx[i]])
                        st.markdown(f"<div style='text-align: center; font-size: 20px; font-weight: bold; color: #333; margin: 5px 0;'>{value}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown("<div style='text-align: center; font-size: 20px; font-weight: bold; color: #333; margin: 5px 0;'>0</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='text-align: center; font-size: 20px; font-weight: bold; color: #333; margin: 5px 0;'>0</div>", unsafe_allow_html=True)

    # Second column - 2 rows
    with col_b:
        titles_col_b = ["Jumlah Fraud","Jumlah Gugatan", "Jumlah Nominal Gugatan Yang Sedang Diajukan"]
        value_idx = [117,132,133]
        for i, title in enumerate(titles_col_b):
            with st.container(border=True):
                st.markdown(f"<div style='text-align: center; color: #999; font-size: 12px;'>{title}</div>", unsafe_allow_html=True)
                if st.session_state.df_ytd is not None and latest_col_ytd_idx:
                    try:
                        # Get the data column (next column after month name)
                        col_position = st.session_state.df_ytd.columns.get_loc(latest_col_ytd_idx)
                        data_col = st.session_state.df_ytd.columns[col_position + 1]
                        value = null_value(st.session_state.df_ytd[data_col].iloc[value_idx[i]])
                        st.markdown(f"<div style='text-align: center; font-size: 20px; font-weight: bold; color: #333; margin: 5px 0;'>{value}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown("<div style='text-align: center; font-size: 20px; font-weight: bold; color: #333; margin: 5px 0;'>0</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='text-align: center; font-size: 20px; font-weight: bold; color: #333; margin: 5px 0;'>0</div>", unsafe_allow_html=True)

    # Third column - 2 rows
    with col_c:
        titles_col_c = ["Jumlah Pelanggaran Atas Ketentuan", "Jumlah Denda"]
        value_idx = [134,137]
        for i, title in enumerate(titles_col_c):
            with st.container(border=True):
                st.markdown(f"<div style='text-align: center; color: #999; font-size: 12px;'>{title}</div>", unsafe_allow_html=True)
                if st.session_state.df_ytd is not None and latest_col_ytd_idx:
                    try:
                        # Get the data column (next column after month name)
                        col_position = st.session_state.df_ytd.columns.get_loc(latest_col_ytd_idx)
                        data_col = st.session_state.df_ytd.columns[col_position + 1]
                        value = null_value(st.session_state.df_ytd[data_col].iloc[value_idx[i]])
                        st.markdown(f"<div style='text-align: center; font-size: 20px; font-weight: bold; color: #333; margin: 5px 0;'>{value}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown("<div style='text-align: center; font-size: 20px; font-weight: bold; color: #333; margin: 5px 0;'>0</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='text-align: center; font-size: 20px; font-weight: bold; color: #333; margin: 5px 0;'>0</div>", unsafe_allow_html=True)