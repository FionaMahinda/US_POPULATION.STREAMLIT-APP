import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="US Population Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Enable dark theme in Altair
alt.themes.enable("dark")

# Load data
try:
    df_reshaped = pd.read_csv('us-population-2010-2019-reshaped.csv')
except FileNotFoundError:
    st.error("The file 'us-population-2010-2019-reshaped.csv' was not found.")
    st.stop()

# Clean up column names
df_reshaped = df_reshaped.rename(columns={'year': 'Year', 'population': 'Population'})
if 'Unnamed: 0' in df_reshaped.columns:
    df_reshaped = df_reshaped.drop(columns=['Unnamed: 0'])

# Sidebar
with st.sidebar:
    st.title('🏂 US Population Dashboard')
    
    # Year selection
    year_list = list(df_reshaped.Year.unique())[::-1]
    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    df_selected_year = df_reshaped[df_reshaped.Year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="Population", ascending=False)

    # Color theme selection
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

# Description
st.write("""
This dashboard visualizes US population data from 2010 to 2019. 
Use the sidebar to select a year and customize the color theme for the charts.
""")

# Main content
st.header(f"US Population in {selected_year}")

# Altair visualization
alt_chart = alt.Chart(df_selected_year_sorted).mark_bar().encode(
    x=alt.X('Population:Q', title='Population'),
    y=alt.Y('states:N', sort='-x', title='State'),  # Ensure correct column name
    color=alt.Color('Population:Q', scale=alt.Scale(scheme=selected_color_theme))
).properties(
    title=f'US Population in {selected_year}',
    width=700,
    height=500
)

# Plotly visualization
fig = px.bar(
    df_selected_year_sorted,
    x="Population",
    y="states",  # Correct column name
    orientation="h",
    color="Population",
    color_continuous_scale=selected_color_theme,
    title=f'US Population in {selected_year}'
)

# Display visualizations side-by-side
col1, col2 = st.columns(2)
with col1:
    st.altair_chart(alt_chart, use_container_width=True)
with col2:
    st.plotly_chart(fig, use_container_width=True)

# Download data button
st.download_button(
    label="Download Data",
    data=df_selected_year_sorted.to_csv(index=False),
    file_name=f'us_population_{selected_year}.csv',
    mime='text/csv'
)
