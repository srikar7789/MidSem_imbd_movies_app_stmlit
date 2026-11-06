import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="IMDb Movie Analytics Dashboard", page_icon="🎬", layout="wide"
)

with st.sidebar:
  st.markdown("### 🟡 **IMDb**")
  st.markdown("### **Movie Analytics Dashboard**")
  st.divider()

  nav = st.radio(
      "Navigation",
      ["Dashboard", "Movie Explorer", "Movie Search (Form + Session State)"],
  )

  st.divider()
  with st.expander("📊 Dataset Information", expanded=True):
    st.markdown("**Top 250 Movies on IMDb (2026)**")
    st.markdown("**Rows:** 250")
    st.markdown("**Columns:** 12")
    st.markdown(
        "This dataset contains information about the top 250 movies,"
        " including titles, rating, votes, genres and worldwide gross."
    )


@st.cache_data
def load_data():
  try:
    df = pd.read_csv("movies_csv.csv")
  except FileNotFoundError:
    df = pd.read_csv("movies_csv")

  df = df.drop_duplicates()
  return df


try:
  df = load_data()
except Exception:
  data = {
      "primaryTitle": [
          "Avatar",
          "Avengers: Endgame",
          "The Dark Knight",
          "Titanic",
          "Star Wars: The Force Awakens",
          "Avengers: Infinity War",
      ],
      "genres": [
          "Action,Adventure,Sci-Fi",
          "Action,Adventure,Drama",
          "Action,Crime,Drama",
          "Drama,Romance",
          "Action,Adventure,Sci-Fi",
          "Action,Adventure,Sci-Fi",
      ],
      "country": ["USA", "USA", "USA, UK", "USA", "USA", "USA"],
      "averageRating": [8.8, 8.4, 9.0, 7.9, 7.8, 8.5],
      "numVotes": [1590770, 1397522, 2748449, 1200000, 950000, 1100000],
      "grossWorldwide": [
          2920000000,
          2800000000,
          1005000000,
          2200000000,
          2070000000,
          2050000000,
      ],
  }
  df = pd.DataFrame(data)

st.markdown(
    """
    <div style='background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba"); background-size: cover; padding: 30px; border-radius: 10px; text-align: center; color: white;'>
        <h1>🎬 IMDb Movie Analytics Dashboard</h1>
        <p style='font-size: 18px;'>Explore. Analyze. Discover.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")

col1, col2, col3, col4 = st.columns(4)
total_movies = df.shape[0]
avg_rating = round(df["averageRating"].mean(), 1)
max_rating = df["averageRating"].max()
total_votes = int(df["numVotes"].sum())

col1.metric("Total Movies", f"{total_movies}")
col2.metric("Average IMDb Rating", f"{avg_rating}")
col3.metric("Highest Rating", f"{max_rating}")
col4.metric("Total Votes", f"{total_votes:,}")

st.divider()

tab1, tab2, tab3 = st.tabs(
    ["📊 Genre Analysis", "📈 Rating Analysis", "💰 Gross Collection"]
)

with tab1:
  pass
with tab2:
  pass
with tab3:
  pass

c1, c2 = st.columns(2)

with c1:
  st.subheader("📊 Movies by Genre")
  if "genres" in df.columns:
    genre_counts = (
        df["genres"].str.split(",").explode().str.strip().value_counts().head(6)
    )
    st.bar_chart(genre_counts)

with c2:
  st.subheader("📈 IMDb Rating Distribution")
  if "averageRating" in df.columns:
    rating_counts = df["averageRating"].value_counts().sort_index()
    st.bar_chart(rating_counts)

c3, c4 = st.columns(2)

with c3:
  st.subheader("📉 Rating vs Number of Votes")
  if "averageRating" in df.columns and "numVotes" in df.columns:
    st.scatter_chart(df, x="averageRating", y="numVotes")

with c4:
  st.subheader("🏆 Top 10 Movies by Worldwide Gross")
  if "grossWorldwide" in df.columns and "primaryTitle" in df.columns:
    top_gross = (
        df.sort_values(by="grossWorldwide", ascending=False)
        .head(5)
        .set_index("primaryTitle")
    )
    st.bar_chart(top_gross["grossWorldwide"], horizontal=True)

st.success(
    "Dashboard loaded successfully! Enjoy exploring the top 250 movies on IMDb."
)
st.divider()

left_col, right_col = st.columns([2, 1])

with left_col:
  st.subheader("🔍 Interactive Movie Explorer")

  f_col1, f_col2, f_col3 = st.columns(3)
  with f_col1:
    all_genres = sorted(
        df["genres"].str.split(",").explode().str.strip().dropna().unique()
    )
    selected_genre = st.selectbox("Genre", ["Action"] + list(all_genres))
  with f_col2:
    selected_countries = st.multiselect("Countries", ["USA", "UK"], default=[])
  with f_col3:
    rating_range = st.slider(
        "IMDb Rating",
        float(df["averageRating"].min()),
        float(df["averageRating"].max()),
        (7.0, 9.5),
    )

  f_col4, f_col5, f_col6 = st.columns(3)
  with f_col4:
    min_votes = st.number_input("Min Votes", value=100000)
  with f_col5:
    search_title = st.text_input("Search Title", placeholder="Enter movie title...")
  with f_col6:
    sort_order = st.radio("Sort Order", ["Ascending", "Descending"], index=1)

  filtered_df = df.copy()
  if selected_genre != "All":
    filtered_df = filtered_df[
        filtered_df["genres"].str.contains(selected_genre, na=False)
    ]
  filtered_df = filtered_df[
      (filtered_df["averageRating"] >= rating_range[0])
      & (filtered_df["averageRating"] <= rating_range[1])
  ]
  filtered_df = filtered_df[filtered_df["numVotes"] >= min_votes]
  if search_title:
    filtered_df = filtered_df[
        filtered_df["primaryTitle"]
        .str.contains(search_title, case=False, na=False)
    ]

  ascending_bool = True if sort_order == "Ascending" else False
  filtered_df = filtered_df.sort_values(
      by="averageRating", ascending=ascending_bool
  )

  b_col1, b_col2 = st.columns([1, 3])
  with b_col1:
    st.info(f"Filtered Movies: {len(filtered_df)}")
  with b_col2:
    if st.button("Reset Filters"):
      st.rerun()

  display_cols = [
      c
      for c in [
          "primaryTitle",
          "genres",
          "country",
          "averageRating",
          "numVotes",
          "grossWorldwide",
      ]
      if c in filtered_df.columns
  ]
  st.dataframe(filtered_df[display_cols].head(10), use_container_width=True)

with right_col:
  st.subheader("🔎 Movie Search (Form + Session State)")

  if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = df.iloc[0].to_dict()

  with st.form("movie_search_form"):
    st.text_input("Movie Title", value="Inception")
    st.selectbox("Preferred Genre", ["Sci-Fi", "Action", "Drama"])
    st.slider("Minimum IMDb Rating", 0.0, 10.0, 8.0)
    submitted = st.form_submit_button("🔍 Search Movie")

    if submitted:
      st.session_state.selected_movie = df.iloc[0].to_dict()

  mov = st.session_state.selected_movie
  st.markdown(
      f"""
        <div style='background-color: #1e293b; padding: 15px; border-radius: 8px; border: 1px solid #334155;'>
            <h4>{mov.get('primaryTitle', 'Inception')}</h4>
            <p style='color: #94a3b8; font-size: 14px;'>Genre: {mov.get('genres', 'Sci-Fi')} | IMDb Rating: {mov.get('averageRating', 8.8)} | Votes: {mov.get('numVotes', 2206251):,}</p>
        </div>
        """,
      unsafe_allow_html=True,
  )