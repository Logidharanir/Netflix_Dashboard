
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Netflix Analytics | Pro Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
CSS_PATH = BASE_DIR / "style.css"

ACCENT = "#E50914"
PINK = "#FF5263"
BLUE = "#4F8CFF"
PURPLE = "#9B6DFF"
GREEN = "#20C997"
ORANGE = "#FF9F43"


# =========================================================
# 2. CUSTOM CSS
# =========================================================
CUSTOM_CSS = """
<style>
.stApp {
    background: radial-gradient(ellipse at top left, #241015 0%, #101010 45%, #090909 100%);
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111111, #191012);
    border-right: 1px solid rgba(229,9,20,.25);
}

.hero {
    padding: 32px 34px;
    margin-bottom: 24px;
    border: 1px solid rgba(229,9,20,.35);
    border-radius: 20px;
    background:
        radial-gradient(circle at 90% 15%, rgba(229,9,20,.24), transparent 35%),
        linear-gradient(120deg, #171717, #111111 70%);
    box-shadow: 0 12px 40px rgba(0,0,0,.28);
}

.hero-eyebrow {
    color: #ff6974;
    font-size: 12px;
    letter-spacing: 3px;
    font-weight: 700;
}

.hero-title {
    color: #ffffff;
    font-size: clamp(30px, 4vw, 48px);
    font-weight: 900;
    letter-spacing: -1.5px;
    margin-top: 10px;
}

.hero-title span {
    color: #E50914;
}

.hero-subtitle {
    color: #b5b5b5;
    font-size: 15px;
    margin-top: 8px;
}

.section-heading {
    color: #ffffff;
    font-size: 17px;
    font-weight: 800;
    letter-spacing: 1.2px;
    border-left: 4px solid #E50914;
    padding-left: 12px;
    margin: 28px 0 16px;
}

.section-heading span {
    color: #999999;
    font-size: 10px;
    letter-spacing: 1px;
    margin-left: 8px;
}

.metric-card {
    background: linear-gradient(145deg, #1b1b1b, #121212);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 16px;
    padding: 19px;
    min-height: 145px;
    transition: transform .2s ease, border-color .2s ease;
    box-shadow: 0 8px 25px rgba(0,0,0,.18);
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: rgba(229,9,20,.65);
}

.metric-icon {
    font-size: 23px;
}

.metric-label {
    color: #a7a7a7;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-top: 15px;
}

.metric-value {
    color: #ffffff;
    font-size: clamp(20px, 2vw, 29px);
    font-weight: 800;
    margin-top: 5px;
    overflow-wrap: anywhere;
}

.metric-foot {
    color: #8e8e8e;
    font-size: 11px;
    margin-top: 6px;
}

.panel-title {
    font-size: 17px;
    font-weight: 750;
    color: #ffffff;
    margin-bottom: 4px;
}

.panel-subtitle {
    color: #999999;
    font-size: 12px;
    margin-bottom: 12px;
}

.result-line {
    color: #bdbdbd;
    font-size: 12px;
    padding: 12px 0;
}

.result-line b {
    color: #ffffff;
}

.footer {
    text-align: center;
    color: #777777;
    padding: 28px 0 15px;
    font-size: 12px;
}

.footer span {
    color: #E50914;
    font-weight: 800;
    letter-spacing: 2px;
}

.footer-note {
    margin-top: 7px;
    font-size: 11px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: rgba(255,255,255,.09) !important;
    border-radius: 16px !important;
    background: rgba(18,18,18,.58);
}

div[data-testid="stPlotlyChart"] {
    transition: transform .18s ease;
}

div[data-testid="stPlotlyChart"]:hover {
    transform: translateY(-2px);
}

.stButton button, .stDownloadButton button {
    border-radius: 10px;
    transition: all .2s ease;
}

.stButton button:hover, .stDownloadButton button:hover {
    border-color: #E50914;
    color: #ff6974;
}

div[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 12px;
}

#MainMenu, footer {
    visibility: hidden;
}
</style>
"""


def load_css():
    if CSS_PATH.exists():
        st.markdown(
            f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


load_css()


# =========================================================
# 3. LOAD AND VALIDATE DATA
# =========================================================
@st.cache_data(show_spinner=False)
def read_excel_file(file_path, modified_time):
    return pd.read_excel(
        file_path,
        sheet_name="Netflix_Data",
        engine="openpyxl",
    )


@st.cache_data(show_spinner=False)
def read_csv_file(file_path, modified_time):
    return pd.read_csv(file_path)


@st.cache_data(show_spinner=False)
def prepare_data(data):
    data = data.copy()
    data.columns = [str(c).strip() for c in data.columns]

    required_columns = [
        "date_added",
        "genre",
        "country",
        "content_type",
        "content_id",
        "views",
        "watch_hours",
        "estimated_revenue_usd",
        "title",
        "release_year",
        "rating",
    ]

    missing = [c for c in required_columns if c not in data.columns]

    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing)
        )

    data["date_added"] = pd.to_datetime(
        data["date_added"], errors="coerce"
    )

    for col in [
        "release_year",
        "views",
        "watch_hours",
        "estimated_revenue_usd",
    ]:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    for col in [
        "genre",
        "country",
        "content_type",
        "content_id",
        "title",
        "rating",
    ]:
        data[col] = data[col].astype("string")

    return data


def load_data(uploaded_file):
    if uploaded_file is not None:
        filename = uploaded_file.name.lower()

        if filename.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        elif filename.endswith((".xlsx", ".xls")):
            data = pd.read_excel(uploaded_file, engine=None)
        else:
            raise ValueError("Please upload a CSV or Excel file.")

        return prepare_data(data)

    candidates = [
        BASE_DIR / "netflix_dashboard_dataset.xlsx",
        BASE_DIR / "netflix_dashboard_dataset.csv",
        BASE_DIR / "netflix_dashboard_dataset.xls",
        BASE_DIR / "netflix_dashboard_500000_records.xlsx",
        BASE_DIR / "netflix_dashboard_500000_records.csv",
        BASE_DIR / "netflix_dashboard_500000_records.xls",
    ]

    data_path = next((p for p in candidates if p.exists()), None)

    if data_path is None:
        return None

    if data_path.suffix.lower() == ".csv":
        data = read_csv_file(
            str(data_path), data_path.stat().st_mtime
        )
    else:
        data = read_excel_file(
            str(data_path), data_path.stat().st_mtime
        )

    return prepare_data(data)


# =========================================================
# 4. HEADER
# =========================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">● STREAMING INTELLIGENCE</div>
        <div class="hero-title">NETFLIX <span>ANALYTICS</span></div>
        <div class="hero-subtitle">
            Explore content performance, audience activity,
            engagement and estimated revenue.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 5. SIDEBAR AND DATASET
# =========================================================
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🎨 Appearance")

    theme = st.selectbox(
        "Dashboard theme",
        ["Midnight Red", "Carbon Blue", "Light"],
    )

    chart_style = st.selectbox(
        "Chart style",
        ["Neon", "Minimal"],
    )

    st.markdown("---")
    st.markdown("### 🔎 Data filters")

try:
    df = load_data(None)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

if df is None:
    st.warning(
        "Dataset not found. Put netflix_dashboard_dataset.xlsx "
        "in the same folder as app.py."
    )
    st.stop()

if df.empty:
    st.warning("The dataset contains no records.")
    st.stop()

valid_dates = df["date_added"].dropna()

if valid_dates.empty:
    st.error("The date_added column contains no valid dates.")
    st.stop()


# =========================================================
# 6. THEME SETTINGS
# =========================================================
if theme == "Carbon Blue":
    accent = BLUE
    second_accent = PURPLE
    chart_template = "plotly_dark"
    grid_color = "rgba(255,255,255,.10)"
    background_color = "rgba(0,0,0,0)"
    font_color = "#f4f4f5"
elif theme == "Light":
    accent = ACCENT
    second_accent = ORANGE
    chart_template = "plotly_white"
    grid_color = "rgba(30,40,60,.12)"
    background_color = "rgba(255,255,255,0)"
    font_color = "#252a35"
    st.markdown(
        """
        <style>
        .stApp {background: #f3f5f9 !important; color: #202533;}
        .hero, .metric-card {
            background: #ffffff !important;
            border-color: #dfe3ec !important;
        }
        .hero-title, .panel-title, .metric-value {
            color: #202533 !important;
        }
        .hero-subtitle, .metric-label, .metric-foot,
        .panel-subtitle, .result-line {
            color: #606b7b !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    accent = ACCENT
    second_accent = PINK
    chart_template = "plotly_dark"
    grid_color = "rgba(255,255,255,.10)"
    background_color = "rgba(0,0,0,0)"
    font_color = "#f4f4f5"


# =========================================================
# 7. FILTERS
# =========================================================
with st.sidebar:
    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    date_range = st.date_input(
        "Date added",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="date_filter",
    )

    genres = sorted(df["genre"].dropna().unique().tolist())
    countries = sorted(df["country"].dropna().unique().tolist())
    content_types = sorted(
        df["content_type"].dropna().unique().tolist()
    )

    selected_genres = st.multiselect(
        "Genre",
        genres,
        default=genres,
        key="genre_filter",
    )

    selected_countries = st.multiselect(
        "Country",
        countries,
        default=countries,
        key="country_filter",
    )

    selected_types = st.multiselect(
        "Content type",
        content_types,
        default=content_types,
        key="type_filter",
    )

    if st.button("↻ Reset filters", use_container_width=True):
        st.session_state["date_filter"] = (min_date, max_date)
        st.session_state["genre_filter"] = genres
        st.session_state["country_filter"] = countries
        st.session_state["type_filter"] = content_types
        st.rerun()


# =========================================================
# 8. APPLY FILTERS
# =========================================================
filtered_df = df.copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])

    filtered_df = filtered_df[
        (filtered_df["date_added"] >= start_date)
        & (
            filtered_df["date_added"]
            < end_date + pd.Timedelta(days=1)
        )
    ]

filtered_df = filtered_df[
    filtered_df["genre"].isin(selected_genres)
    & filtered_df["country"].isin(selected_countries)
    & filtered_df["content_type"].isin(selected_types)
]

if filtered_df.empty:
    st.warning("No records match your filters. Change your selections.")
    st.stop()


# =========================================================
# 9. CHART HELPERS
# =========================================================
def style_chart(fig, height=360):
    fig.update_layout(
        template=chart_template,
        height=height,
        paper_bgcolor=background_color,
        plot_bgcolor=background_color,
        font=dict(
            family="Inter, Arial, sans-serif",
            color=font_color,
            size=12,
        ),
        margin=dict(l=18, r=18, t=35, b=25),
        hoverlabel=dict(
            bgcolor="#191919",
            font_size=13,
            font_family="Arial",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        transition=dict(duration=350, easing="cubic-in-out"),
    )

    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(
        showgrid=True,
        gridcolor=grid_color,
        zeroline=False,
    )

    return fig


def show_panel_title(title, subtitle):
    st.markdown(
        f'<div class="panel-title">{title}</div>'
        f'<div class="panel-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )


def format_number(value):
    if pd.isna(value):
        return "0"
    return f"{value:,.0f}"


# =========================================================
# 10. KPI CARDS
# =========================================================
total_content = filtered_df["content_id"].nunique()
total_views = filtered_df["views"].sum()
total_watch_hours = filtered_df["watch_hours"].sum()
total_revenue = filtered_df["estimated_revenue_usd"].sum()

st.markdown(
    '<div class="section-heading">OVERVIEW '
    '<span>• LIVE FILTERED RESULTS</span></div>',
    unsafe_allow_html=True,
)

kpi_cols = st.columns(4)

kpis = [
    (
        "CONTENT TITLES",
        format_number(total_content),
        "🎬",
        "Unique content IDs",
    ),
    (
        "TOTAL VIEWS",
        format_number(total_views),
        "▶️",
        "Simulated audience activity",
    ),
    (
        "WATCH HOURS",
        format_number(total_watch_hours),
        "◷",
        "Estimated viewing time",
    ),
    (
        "EST. REVENUE",
        f"${total_revenue:,.2f}",
        "💰",
        "Synthetic practice estimate",
    ),
]

for col, (label, value, icon, footnote) in zip(kpi_cols, kpis):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">{icon}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-foot">{footnote}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    f'<div class="result-line">Showing <b>{len(filtered_df):,}</b> '
    f'of <b>{len(df):,}</b> records · '
    f'<b>{filtered_df["genre"].nunique()}</b> genres · '
    f'<b>{filtered_df["country"].nunique()}</b> countries</div>',
    unsafe_allow_html=True,
)


# =========================================================
# 11. CONTENT TRENDS AND CONTENT TYPE
# =========================================================
st.markdown(
    '<div class="section-heading">CONTENT PERFORMANCE '
    '<span>• TRENDS & BREAKDOWNS</span></div>',
    unsafe_allow_html=True,
)

left, right = st.columns(2, gap="large")

with left:
    with st.container(border=True):
        show_panel_title(
            "Monthly content trend",
            "Number of unique titles added each month",
        )

        monthly = (
            filtered_df.dropna(subset=["date_added"])
            .assign(
                month=lambda x: (
                    x["date_added"].dt.to_period("M").astype(str)
                )
            )
            .groupby("month", as_index=False)["content_id"]
            .nunique()
            .rename(columns={"content_id": "titles"})
        )

        fig = px.area(
            monthly,
            x="month",
            y="titles",
            markers=True,
        )

        fig.update_traces(
            line=dict(color=accent, width=3),
            marker=dict(size=5),
            fillcolor=(
                "rgba(229,9,20,.18)"
                if theme != "Carbon Blue"
                else "rgba(79,140,255,.18)"
            ),
            hovertemplate=(
                "<b>%{x}</b><br>Titles: %{y:,}<extra></extra>"
            ),
        )

        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Unique titles",
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True,
            config={"displaylogo": False},
        )

with right:
    with st.container(border=True):
        show_panel_title(
            "Views by content type",
            "Compare movies and TV shows",
        )

        type_views = (
            filtered_df.groupby("content_type", as_index=False)["views"]
            .sum()
            .sort_values("views", ascending=False)
        )

        fig = px.bar(
            type_views,
            x="content_type",
            y="views",
            color="content_type",
            color_discrete_sequence=[accent, second_accent],
            hover_data={"views": ":,.0f"},
        )

        fig.update_traces(
            hovertemplate=(
                "<b>%{x}</b><br>Views: %{y:,.0f}<extra></extra>"
            )
        )

        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Total views",
            showlegend=False,
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True,
            config={"displaylogo": False},
        )


# =========================================================
# 12. TOP TITLES AND GENRE PERFORMANCE
# =========================================================
left, right = st.columns(2, gap="large")

with left:
    with st.container(border=True):
        show_panel_title(
            "Top 10 titles by views",
            "Highest-viewed titles in the filtered dataset",
        )

        top_content = (
            filtered_df.groupby("title", as_index=False)["views"]
            .sum()
            .nlargest(10, "views")
            .sort_values("views", ascending=True)
        )

        fig = px.bar(
            top_content,
            x="views",
            y="title",
            orientation="h",
            color="views",
            color_continuous_scale=["#401016", accent],
            hover_data={"views": ":,.0f"},
        )

        fig.update_traces(
            hovertemplate=(
                "<b>%{y}</b><br>Views: %{x:,.0f}<extra></extra>"
            )
        )

        fig.update_layout(
            xaxis_title="Views",
            yaxis_title=None,
            coloraxis_showscale=False,
        )

        st.plotly_chart(
            style_chart(fig, 420),
            use_container_width=True,
            config={"displaylogo": False},
        )

with right:
    with st.container(border=True):
        show_panel_title(
            "Genre performance",
            "Compare views across genres",
        )

        genre_views = (
            filtered_df.groupby("genre", as_index=False)["views"]
            .sum()
            .sort_values("views", ascending=False)
        )

        fig = px.bar(
            genre_views,
            x="genre",
            y="views",
            color="views",
            color_continuous_scale=["#401016", accent],
            hover_data={"views": ":,.0f"},
        )

        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Views",
            coloraxis_showscale=False,
        )
        fig.update_xaxes(tickangle=-35)

        st.plotly_chart(
            style_chart(fig, 420),
            use_container_width=True,
            config={"displaylogo": False},
        )


# =========================================================
# 13. COUNTRY AND RATING ANALYSIS
# =========================================================
left, right = st.columns(2, gap="large")

with left:
    with st.container(border=True):
        show_panel_title(
            "Top 10 countries",
            "Ranked by total views",
        )

        country_views = (
            filtered_df.groupby("country", as_index=False)["views"]
            .sum()
            .nlargest(10, "views")
            .sort_values("views", ascending=True)
        )

        fig = px.bar(
            country_views,
            x="views",
            y="country",
            orientation="h",
            color="views",
            color_continuous_scale=["#401016", accent],
            hover_data={"views": ":,.0f"},
        )

        fig.update_layout(
            xaxis_title="Views",
            yaxis_title=None,
            coloraxis_showscale=False,
        )

        st.plotly_chart(
            style_chart(fig, 400),
            use_container_width=True,
            config={"displaylogo": False},
        )

with right:
    with st.container(border=True):
        show_panel_title(
            "Content rating mix",
            "Share of records by age rating",
        )

        rating_count = (
            filtered_df["rating"]
            .fillna("Unknown")
            .value_counts()
            .rename_axis("rating")
            .reset_index(name="titles")
        )

        fig = px.pie(
            rating_count,
            names="rating",
            values="titles",
            hole=0.62,
            color_discrete_sequence=[
                accent, "#ff6b75", "#ff9a70",
                "#8d98aa", "#c6ccd5", "#6b7280",
                "#9b6dff", "#20c997",
            ],
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b><br>Records: %{value:,}"
                "<br>Share: %{percent}<extra></extra>"
            ),
            marker=dict(line=dict(color="#111111", width=2)),
        )

        fig.update_layout(showlegend=True)

        st.plotly_chart(
            style_chart(fig, 400),
            use_container_width=True,
            config={"displaylogo": False},
        )


# =========================================================
# 14. ADVANCED INTERACTIVE ANALYTICS
# =========================================================
st.markdown(
    '<div class="section-heading">ADVANCED INSIGHTS '
    '<span>• EXPLORE THE DATA</span></div>',
    unsafe_allow_html=True,
)

metric_options = {
    "Total Views": "views",
    "Watch Hours": "watch_hours",
    "Estimated Revenue": "estimated_revenue_usd",
}

metric_label = st.selectbox(
    "Choose a metric to analyse",
    list(metric_options.keys()),
    key="advanced_metric",
)

metric = metric_options[metric_label]

left, right = st.columns(2, gap="large")

with left:
    with st.container(border=True):
        show_panel_title(
            f"{metric_label} by genre",
            "Updates when you change the metric",
        )

        genre_metric = (
            filtered_df.groupby("genre", as_index=False)[metric]
            .sum()
            .sort_values(metric, ascending=False)
        )

        fig = px.bar(
            genre_metric,
            x="genre",
            y=metric,
            color=metric,
            color_continuous_scale=["#401016", accent, "#ff6974"],
            hover_data={metric: ":,.2f"},
        )

        fig.update_layout(
            xaxis_title="Genre",
            yaxis_title=metric_label,
            coloraxis_showscale=False,
        )
        fig.update_xaxes(tickangle=-35)

        st.plotly_chart(
            style_chart(fig, 420),
            use_container_width=True,
            config={"displaylogo": False},
        )

with right:
    with st.container(border=True):
        show_panel_title(
            f"{metric_label} by country",
            "Top 10 countries for the selected metric",
        )

        country_metric = (
            filtered_df.groupby("country", as_index=False)[metric]
            .sum()
            .nlargest(10, metric)
            .sort_values(metric, ascending=True)
        )

        fig = px.bar(
            country_metric,
            x=metric,
            y="country",
            orientation="h",
            color=metric,
            color_continuous_scale=["#401016", accent, "#ff6974"],
            hover_data={metric: ":,.2f"},
        )

        fig.update_layout(
            xaxis_title=metric_label,
            yaxis_title=None,
            coloraxis_showscale=False,
        )

        st.plotly_chart(
            style_chart(fig, 420),
            use_container_width=True,
            config={"displaylogo": False},
        )


# =========================================================
# 15. CONTENT UNIVERSE AND ENGAGEMENT SCATTER
# =========================================================
left, right = st.columns(2, gap="large")

with left:
    with st.container(border=True):
        show_panel_title(
            "Content universe",
            "Explore country, genre and content type",
        )

        hierarchy = (
            filtered_df.groupby(
                ["country", "genre", "content_type"],
                as_index=False,
            )
            .agg(
                titles=("content_id", "nunique"),
                views=("views", "sum"),
            )
        )

        fig = px.sunburst(
            hierarchy,
            path=["country", "genre", "content_type"],
            values="titles",
            color="views",
            color_continuous_scale=["#401016", accent, "#ff6974"],
        )

        fig.update_layout(coloraxis_showscale=False)

        st.plotly_chart(
            style_chart(fig, 460),
            use_container_width=True,
            config={"displaylogo": False},
        )

with right:
    with st.container(border=True):
        show_panel_title(
            "Views vs watch hours",
            "Explore audience activity and engagement",
        )

        scatter_data = filtered_df[
            ["title", "content_type", "genre", "views", "watch_hours"]
        ].dropna()

        if len(scatter_data) > 5000:
            scatter_data = scatter_data.sample(
                n=5000, random_state=42
            )

        fig = px.scatter(
            scatter_data,
            x="views",
            y="watch_hours",
            color="content_type",
            hover_name="title",
            hover_data=["genre"],
            opacity=0.7,
            color_discrete_sequence=[accent, second_accent],
        )

        fig.update_layout(
            xaxis_title="Views",
            yaxis_title="Watch hours",
        )

        st.plotly_chart(
            style_chart(fig, 460),
            use_container_width=True,
            config={"displaylogo": False},
        )


# =========================================================
# 16. RELEASE YEAR DISTRIBUTION
# =========================================================
with st.container(border=True):
    show_panel_title(
        "Release-year distribution",
        "Number of unique titles by original release year",
    )

    yearly = (
        filtered_df.dropna(subset=["release_year"])
        .groupby("release_year", as_index=False)["content_id"]
        .nunique()
        .rename(columns={"content_id": "titles"})
        .sort_values("release_year")
    )

    fig = px.area(
        yearly,
        x="release_year",
        y="titles",
        markers=True,
    )

    fig.update_traces(
        line=dict(color=accent, width=2),
        fillcolor=(
            "rgba(229,9,20,.14)"
            if theme != "Carbon Blue"
            else "rgba(79,140,255,.14)"
        ),
        hovertemplate=(
            "Year: %{x:.0f}<br>Unique titles: %{y:,}<extra></extra>"
        ),
    )

    fig.update_layout(
        xaxis_title="Release year",
        yaxis_title="Unique titles",
    )

    st.plotly_chart(
        style_chart(fig, 350),
        use_container_width=True,
        config={"displaylogo": False},
    )


# =========================================================
# 17. DATA EXPLORER AND EXPORT
# =========================================================
st.markdown(
    '<div class="section-heading">DATA EXPLORER '
    '<span>• SEARCH, INSPECT & EXPORT</span></div>',
    unsafe_allow_html=True,
)

with st.expander("🔎 Open filtered records", expanded=False):
    search_text = st.text_input(
        "Search titles, countries or genres",
        placeholder="Type to search...",
    )

    display_df = filtered_df

    if search_text.strip():
        term = search_text.strip()

        mask = (
            display_df["title"].fillna("").str.contains(
                term, case=False, regex=False
            )
            | display_df["country"].fillna("").str.contains(
                term, case=False, regex=False
            )
            | display_df["genre"].fillna("").str.contains(
                term, case=False, regex=False
            )
        )

        display_df = display_df[mask]

    st.caption(
        f"{len(display_df):,} matching records. "
        "The preview is limited to 1,000 rows for performance."
    )

    st.dataframe(
        display_df.head(1000),
        use_container_width=True,
        hide_index=True,
    )

    csv_data = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download filtered data (CSV)",
        data=csv_data,
        file_name="filtered_netflix_data.csv",
        mime="text/csv",
        use_container_width=True,
    )


# =========================================================
# 18. FOOTER
# =========================================================
st.markdown(
    """
    <div class="footer">
        <span>NETFLIX ANALYTICS</span>
        · Built with Python, Pandas, Streamlit & Plotly
        <div class="footer-note">
            Synthetic practice dataset — not official Netflix business data.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

