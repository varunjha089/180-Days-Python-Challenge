import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ---------- CONFIG ----------
DATA_FILE = 'gate_progress.csv'
WEIGHT_FILE = 'subject_weights.csv'
SUBJECTS = ['Engineering Mathematics', 'Discrete Mathematics', 'Data Structure', 'Algorithms', 'Digital Logic', 'Computer Org', 
            'OS', 'DBMS', 'TOC', 'Compiler', 'CN', 'General Aptitude']

# ---------- HELPERS ----------
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, parse_dates=['Target Date'])
    else:
        df = pd.DataFrame(columns=['Subject', 'Topic', 'Completed', 'Target Date', 'Notes'])
    return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def load_weights():
    if os.path.exists(WEIGHT_FILE):
        return pd.read_csv(WEIGHT_FILE, index_col='Subject')['Weight']
    else:
        return pd.Series({s: 1 for s in SUBJECTS}, name='Weight')

def save_weights(weights):
    weights_df = weights.reset_index()
    weights_df.columns = ['Subject', 'Weight']
    weights_df.to_csv(WEIGHT_FILE, index=False)

def get_weighted_progress(df, weights):
    subject_completion = df.groupby('Subject')['Completed'].mean().fillna(0)
    weighted_score = (subject_completion * weights).sum()
    total_weight = weights.sum()
    return round((weighted_score / total_weight) * 100, 2)

# ---------- UI START ----------
st.set_page_config("🎯 GATE Tracker", layout="wide")
st.title("🎯 GATE Exam Preparation Tracker")

df = load_data()
weights = load_weights()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("🔍 Filters")
selected_subjects = st.sidebar.multiselect("Filter by Subject", SUBJECTS, default=SUBJECTS)
status_filter = st.sidebar.radio("Status", ["All", "Completed", "Pending"])
date_range = st.sidebar.date_input("Target Date Range", [])

filtered_df = df[df['Subject'].isin(selected_subjects)]

if status_filter == "Completed":
    filtered_df = filtered_df[filtered_df['Completed'] == True]
elif status_filter == "Pending":
    filtered_df = filtered_df[filtered_df['Completed'] == False]

if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range)
    filtered_df = filtered_df[(df['Target Date'] >= start_date) & (df['Target Date'] <= end_date)]

# ---------- TABS ----------
tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Topic", "📈 Progress", "📅 Deadlines", "⚖️ Set Subject Weights"])

# ---------- TAB 1: Add Topic ----------
with tab1:
    st.subheader("➕ Add New Topic")
    with st.form("add_topic_form"):
        subject = st.selectbox("Subject", SUBJECTS)
        topic = st.text_input("Topic")
        completed = st.checkbox("Completed")
        target_date = st.date_input("Target Date")
        notes = st.text_area("Notes", height=100)
        submitted = st.form_submit_button("Add Topic")

        if submitted:
            new_row = pd.DataFrame({
                'Subject': [subject],
                'Topic': [topic],
                'Completed': [completed],
                'Target Date': [pd.to_datetime(target_date)],
                'Notes': [notes]
            })
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success(f"Added topic: {topic}")

# ---------- TAB 2: Progress ----------
with tab2:
    st.subheader("📊 Progress Overview")

    weighted_progress = get_weighted_progress(df, weights)
    st.metric("Weighted Progress", f"{weighted_progress:.2f}%")
    st.progress(weighted_progress / 100)

    for subject in SUBJECTS:
        subject_df = df[df['Subject'] == subject]
        if not subject_df.empty:
            pct = subject_df['Completed'].mean() * 100
            st.write(f"**{subject}** - {pct:.1f}% complete")
            st.progress(pct / 100)

# ---------- TAB 3: Calendar Deadlines ----------
with tab3:
    st.subheader("📅 Upcoming Deadlines")

    upcoming = df[df['Completed'] == False].sort_values("Target Date")
    if not upcoming.empty:
        st.dataframe(upcoming[['Subject', 'Topic', 'Target Date']], use_container_width=True)
    else:
        st.info("✅ No pending topics with deadlines.")

# ---------- TAB 4: Set Subject Weights ----------
with tab4:
    st.subheader("⚖️ Assign Weights to Subjects")

    weight_input = {}
    for subj in SUBJECTS:
        weight_input[subj] = st.number_input(f"{subj}", value=int(weights.get(subj, 1)), step=1, min_value=1)

    if st.button("💾 Save Weights"):
        weights = pd.Series(weight_input)
        save_weights(weights)
        st.success("Weights updated successfully.")

# ---------- Edit Table Below Tabs ----------
st.markdown("### 📝 Edit Your Topics Below")
if not filtered_df.empty:
    edited_df = st.data_editor(filtered_df, num_rows="dynamic", key="editor")
    if st.button("Save Changes to Table"):
        full_df = df.copy()
        full_df.update(edited_df)
        save_data(full_df)
        st.success("Changes saved.")
else:
    st.info("No topics to display with current filters.")
