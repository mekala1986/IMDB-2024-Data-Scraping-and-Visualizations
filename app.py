import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="IMDb 2024 Analytics", layout="wide")
st.title("🎬 IMDb 2024 Movie Data Insights")

# Load Data
try:
    conn = sqlite3.connect('imdb_2024.db')
    df = pd.read_sql('SELECT * FROM movies', conn)
except:
    st.error("Database not found! Please run scraper.py and database.py first.")
    st.stop()

# Sidebar
st.sidebar.header("Filter Options")
genre_list = st.sidebar.multiselect("Select Genre", df['Genre'].unique(), default=df['Genre'].unique())
rating_slider = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 5.0)

filtered_df = df[
    (df['Genre'].isin(genre_list)) & 
    (df['Ratings'] >= rating_slider)
]

# Layout: KPIs
col1, col2, col3 = st.columns(3)

if not filtered_df.empty:
    col1.metric("Total Movies", len(filtered_df))
    col2.metric("Avg Rating", round(filtered_df['Ratings'].mean(), 2))
    col3.metric("Avg Duration (Min)", int(filtered_df['Duration_Minutes'].mean()))

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Top Movies by Rating")
        fig1 = px.bar(filtered_df.nlargest(10, 'Ratings'), x='Ratings', y='Movie Name', orientation='h', color='Ratings')
        st.plotly_chart(fig1, width="stretch")

    with c2:
        st.subheader("Rating vs Popularity")
        fig2 = px.scatter(filtered_df, x='Ratings', y='Votes_Numeric', size='Duration_Minutes', hover_name='Movie Name')
        st.plotly_chart(fig2, width="stretch")

    st.subheader("Filtered Movie List")
    st.dataframe(filtered_df[['Movie Name', 'Genre', 'Ratings', 'Votes_Numeric', 'Duration']], width="stretch")
    
    # Download Button
    st.markdown("---")
    st.subheader("📥 Export Data")
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download CSV", data=csv_data, file_name='imdb_2024.csv', mime='text/csv')
else:
    st.warning("No movies found matching filters.")