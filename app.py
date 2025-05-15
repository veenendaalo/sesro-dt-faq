import streamlit as st
import pandas as pd
import os
import time

# 1) Page config (first Streamlit call)
st.set_page_config(
    page_title="Digital Twins FAQ",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2) (Optional) load custom CSS if you have it
def local_css(path):
    try:
        with open(path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css(".streamlit/styles.css")

# 3) Header
st.image(
    "https://www.thameswater.co.uk/media-library/assets/images/logo-blue.svg",
    width=120,
)
st.markdown("<h1>Digital Twins FAQ</h1>", unsafe_allow_html=True)
st.markdown(
    '<p class="subheader">Your guide to digital twin technology and best practices</p>',
    unsafe_allow_html=True,
)
st.markdown("---")

# 4) Load data on every run so changes show up immediately
def load_faq(path="faq.xlsx"):
    return pd.read_excel(path)

df = load_faq()

# 5) Sidebar controls
st.sidebar.header("🔎 Filter FAQs")
# a) search box
search_term = st.sidebar.text_input("Search questions")
# b) category multiselect
all_categories = df["Category"].dropna().unique().tolist()
selected_cats = st.sidebar.multiselect(
    "Categories", options=all_categories, default=all_categories
)

# 6) Apply filters
if search_term:
    df = df[df["Question"].str.contains(search_term, case=False, na=False)]
if selected_cats:
    df = df[df["Category"].isin(selected_cats)]

# 7) Render grouped by category
if df.empty:
    st.warning("No matching FAQs. Try a different search or category.")
else:
    for cat in selected_cats:
        subset = df[df["Category"] == cat]
        if subset.empty:
            continue
        st.header(cat)
        for _, row in subset.iterrows():
            with st.expander(row["Question"], expanded=False):
                st.write(row["Answer"])
