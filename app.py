
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    page_icon="🎬",
    layout="wide"
)

# ==========================================
# 2. LOAD DATA
# ==========================================
@st.cache_data
def load_data():

    # Read CSV file using UTF-8 encoding
    df = pd.read_csv(
        "netflix_dashboard_500000_records.xlsx",
        encoding="utf-8"
    )

    # Convert date column into date format
    df["date_added"] = pd.to_datetime(
        df["date_added"],
        errors="coerce"
    )

    # Convert numeric columns into numbers
    numeric_columns = [
        "release_year",
        "views",
        "watch_hours",
        "estimated_revenue_usd"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# Load the data
df = load_data()

# ==========================================
# 3. DASHBOARD TITLE
# ==========================================
st.title("🎬 Netflix Analytics Dashboard")

st.caption(
    "Analyze Netflix content, views, watch hours and revenue."
)

st.info(
    "This project uses synthetic practice data, "
    "not actual Netflix business data."
)

# ==========================================
# 4. SIDEBAR FILTERS
# ==========================================
st.sidebar.header("🔍 Dashboard Filters")

# Date filter
valid_dates = df["date_added"].dropna()

if valid_dates.empty:
    st.error("No valid dates found in the dataset.")
    st.stop()

min_date = valid_dates.min().date()
max_date = valid_dates.max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Genre filter
genres = sorted(df["genre"].dropna().unique().tolist())

selected_genres = st.sidebar.multiselect(
    "Select Genre",
    genres,
    default=genres
)

# Country filter
countries = sorted(df["country"].dropna().unique().tolist())

selected_countries = st.sidebar.multiselect(
    "Select Country",
    countries,
    default=countries
)

# Content type filter
content_types = sorted(
    df["content_type"].dropna().unique().tolist()
)

selected_types = st.sidebar.multiselect(
    "Select Content Type",
    content_types,
    default=content_types
)

# ==========================================
# 5. FILTER THE DATA
# ==========================================
if len(date_range) == 2:

    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    # Apply all selected filters
    filtered_df = df[
        (df["date_added"] >= start_date) &
        (df["date_added"] < end_date + pd.Timedelta(days=1)) &
        (df["genre"].isin(selected_genres)) &
        (df["country"].isin(selected_countries)) &
        (df["content_type"].isin(selected_types))
    ]

else:
    filtered_df = df.iloc[0:0]

# Stop if no data matches the filters
if filtered_df.empty:
    st.warning("No records found. Please change the filters.")
    st.stop()

# ==========================================
# 6. KPI CARDS
# ==========================================
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

# Total content
col1.metric(
    "🎞️ Total Content",
    f"{filtered_df['content_id'].nunique():,}"
)

# Total views
col2.metric(
    "👀 Total Views",
    f"{filtered_df['views'].sum():,.0f}"
)

# Total watch hours
col3.metric(
    "⏱️ Watch Hours",
    f"{filtered_df['watch_hours'].sum():,.0f}"
)

# Total estimated revenue
col4.metric(
    "💰 Estimated Revenue",
    f"${filtered_df['estimated_revenue_usd'].sum():,.2f}"
)

st.divider()

# ==========================================
# 7. MONTHLY CONTENT TREND
# ==========================================
col1, col2 = st.columns(2)

with col1:

    st.subheader("📈 Monthly Content Trend")

    # Count content added in each month
    monthly_content = (
        filtered_df.dropna(subset=["date_added"])
        .assign(
            month=lambda x:
            x["date_added"].dt.to_period("M").astype(str)
        )
        .groupby("month")["content_id"]
        .nunique()
    )

    fig, ax = plt.subplots(figsize=(9, 4))

    monthly_content.plot(
        ax=ax,
        marker="o"
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Content Count")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ==========================================
# 8. VIEWS BY CONTENT TYPE
# ==========================================
with col2:

    st.subheader("🎥 Movie vs TV Show Views")

    type_views = (
        filtered_df.groupby("content_type")["views"]
        .sum()
    )

    fig, ax = plt.subplots(figsize=(8, 4))

    type_views.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Content Type")
    ax.set_ylabel("Total Views")
    ax.ticklabel_format(style="plain", axis="y")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()

# ==========================================
# 9. TOP 10 CONTENT BY VIEWS
# ==========================================
col1, col2 = st.columns(2)

with col1:

    st.subheader("🔥 Top 10 Content by Views")

    top_content = (
        filtered_df.groupby("title")["views"]
        .sum()
        .nlargest(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    top_content.plot(
        kind="barh",
        ax=ax
    )

    ax.set_xlabel("Total Views")
    ax.set_ylabel("Title")
    ax.ticklabel_format(style="plain", axis="x")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ==========================================
# 10. VIEWS BY GENRE
# ==========================================
with col2:

    st.subheader("🎭 Views by Genre")

    genre_views = (
        filtered_df.groupby("genre")["views"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    genre_views.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Genre")
    ax.set_ylabel("Total Views")
    ax.tick_params(axis="x", rotation=45)
    ax.ticklabel_format(style="plain", axis="y")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()

# ==========================================
# 11. TOP 10 COUNTRIES BY VIEWS
# ==========================================
col1, col2 = st.columns(2)

with col1:

    st.subheader("🌍 Top 10 Countries by Views")

    country_views = (
        filtered_df.groupby("country")["views"]
        .sum()
        .nlargest(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    country_views.plot(
        kind="barh",
        ax=ax
    )

    ax.set_xlabel("Total Views")
    ax.set_ylabel("Country")
    ax.ticklabel_format(style="plain", axis="x")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ==========================================
# 12. CONTENT RATING DISTRIBUTION
# ==========================================
with col2:

    st.subheader("🔞 Content Rating Distribution")

    rating_count = filtered_df["rating"].value_counts()

    fig, ax = plt.subplots(figsize=(7, 5))

    rating_count.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax
    )

    ax.set_ylabel("")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()

# ==========================================
# 13. YEAR-WISE CONTENT ANALYSIS
# ==========================================
st.subheader("🗓️ Content by Release Year")

yearly_content = (
    filtered_df.groupby("release_year")["content_id"]
    .nunique()
    .sort_index()
)

fig, ax = plt.subplots(figsize=(12, 4))

yearly_content.plot(ax=ax)

ax.set_xlabel("Release Year")
ax.set_ylabel("Number of Content Items")

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# ==========================================
# 14. FILTERED DATA TABLE
# ==========================================
with st.expander("📄 View Filtered Dataset"):

    st.write(
        f"Total filtered records: {len(filtered_df):,}"
    )

    # Show only the first 1,000 rows for better performance
    st.dataframe(
        filtered_df.head(1000),
        use_container_width=True
    )

    st.caption(
        "Showing up to 1,000 rows. Download to access all filtered records."
    )

    # Download all filtered data
    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_netflix_data.csv",
        mime="text/csv"
    )

# ==========================================
# 15. FOOTER
# ==========================================
st.divider()

st.caption(
    "Netflix Analytics Dashboard | "
    "Built using Python, Pandas, Streamlit and Matplotlib"
)
