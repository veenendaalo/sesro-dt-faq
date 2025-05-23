import streamlit as st
import pandas as pd
import os, time

# --- 1) Page configuration (must be first) ---
st.set_page_config(
    page_title="Digital Twins FAQ",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 2) Header with Thames Water logo and styled titles ---
st.image(
    "https://www.thameswater.co.uk/media-library/assets/images/logo-blue.svg",
    width=120,
)
st.markdown(
    "<h1 style='color:#0057A7; margin-bottom:0.25rem;'>Digital Twins FAQ</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='font-size:1.1rem; color:#333333; margin-top:0; margin-bottom:1rem;'>Your guide to digital twin technology and best practices</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# --- 3) Display last-updated timestamp in sidebar ---
last_mod_ts = os.path.getmtime("faq.xlsx")
last_mod = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_mod_ts))
st.sidebar.markdown(f"**Last updated:** {last_mod}")

# --- 4) Load FAQ data on every run ---
def load_faq(path="faq.xlsx"):
    return pd.read_excel(path)

df = load_faq()

# --- 5) Sidebar search box ---
st.sidebar.header("🔎 Search FAQs")
search_term = st.sidebar.text_input("Enter keywords to filter questions", "")
if search_term:
    df = df[df["Question"].str.contains(search_term, case=False, na=False)]

# --- 6) Define desired category order per user ---
desired_order = [
    "Overview & Purpose",
    "Functionality & Use-Cases",
    "Architecture & Components",
    "Data, Integration & Standards",
    "Benefits, Timeline & Access",
    "Support & Next Steps",
]
# Include only categories present in the data, in order
categories = [cat for cat in desired_order if cat in df['Category'].unique()]
# Append any additional categories at the end (if any)
for cat in df['Category'].unique():
    if cat not in categories:
        categories.append(cat)

# --- 7) Sidebar: jump-to links for categories ---) Sidebar: jump-to links for categories ---
st.sidebar.header("📑 Jump to Category")
for cat in categories:
    anchor = cat.lower().replace(" & ", " and ").replace(" ", "-")
    st.sidebar.markdown(f"- [{cat}](#{anchor})", unsafe_allow_html=True)
st.sidebar.markdown("---")

# --- 8) Render FAQs grouped by category ---
if df.empty:
    st.warning("No FAQs match your search. Try different keywords.")
else:
    for cat in categories:
        anchor = cat.lower().replace(" & ", " and ").replace(" ", "-")
        # Anchor for direct linking
        st.markdown(f'<a id="{anchor}"></a>', unsafe_allow_html=True)
        # Styled category header
        st.markdown(
            f"<h2 style='color:#0057A7; border-bottom:3px solid #65C2D5; padding-bottom:0.25rem; margin-top:2rem;'>{cat}</h2>",
            unsafe_allow_html=True,
        )
        # Render questions under this category
        for _, row in df[df['Category'] == cat].iterrows():
            with st.expander(row['Question'], expanded=False):
                st.write(row['Answer'])
