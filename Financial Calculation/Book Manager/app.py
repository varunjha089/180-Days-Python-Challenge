import streamlit as st
import pandas as pd
from database import init_db, add_book, get_books, update_book, delete_book

# Initialize DB
init_db()

st.set_page_config(page_title="📚 Book Manager", layout="wide")
st.title("📚 Personal Book Manager")

# Add Book
# with st.form("add_form"):
#     st.subheader("➕ Add a New Book")
#     col1, col2, col3 = st.columns(3)
#     title = col1.text_input("Title")
#     author = col2.text_input("Author")
#     genre = col3.text_input("Genre")
#     purchase_date = col1.date_input("Purchase Date")
#     cost = col2.number_input("Cost", min_value=0.0)
#     audiobook_link = col3.text_input("Audiobook Link")
#     status = col1.selectbox("Status", ["To Read", "Reading", "Completed"])
#     notes = st.text_area("Notes")

with st.form("add_book_form"):
    st.subheader("➕ Add a New Book")
    title = st.text_input("Title", key="title_input")
    author = st.text_input("Author", key="author_input")
    genre = st.text_input("Genre", key="genre_input")
    purchase_date = st.date_input("Purchase Date", key="date_input")
    cost = st.number_input("Cost", min_value=0.0, format="%.2f", key="cost_input")
    audiobook_link = st.text_input("Link to Audiobook", key="link_input")
    status = st.selectbox("Status", ["To Read", "Reading", "Completed"], key="status_input")
    notes = st.text_area("Notes", key="notes_input")
    submit = st.form_submit_button("💾 Save")

    if st.form_submit_button("Add Book"):
        add_book((title, author, genre, str(purchase_date), cost, audiobook_link, status, notes))
        # st.success(f"Book '{title}' added!")
        if submit:
            if title and author:
                add_book(title, author, genre, str(purchase_date), cost, audiobook_link, status, notes)
                st.success("✅ Book added successfully!")

                # Clear form fields
                for key in ["title_input", "author_input", "genre_input", "date_input", "cost_input", "link_input", "status_input", "notes_input"]:
                    if key in st.session_state:
                        del st.session_state[key]

                st.rerun()  # Refresh the app to reload with cleared form
            else:
                st.warning("⚠️ Title and Author are required!")

# Display Books
# st.subheader("📖 Your Book Collection")
# books = get_books()

# df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Purchase Date", "Cost", "Audiobook", "Status", "Notes"])
# search = st.text_input("Search by Title or Author")
# filtered_df = df[df["Title"].str.contains(search, case=False) | df["Author"].str.contains(search, case=False)]


# st.subheader("📖 Your Book Collection")
# books = get_books()
# df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Purchase Date", "Cost", "Audiobook", "Status", "Notes"])
# search = st.text_input("Search by Title or Author")
# filtered_df = df[df["Title"].str.contains(search, case=False) | df["Author"].str.contains(search, case=False)]

# st.dataframe(filtered_df.drop(columns=["ID"]), use_container_width=True)

st.subheader("📖 Your Book Collection")
books = get_books()
df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Purchase Date", "Cost", "Audiobook", "Status", "Notes"])

search = st.text_input("🔍 Search by Title or Author")
filtered_df = df[df["Title"].str.contains(search, case=False) | df["Author"].str.contains(search, case=False)]

for _, row in filtered_df.iterrows():
    status = row["Status"]
    color = {
        "To Read": "red",
        "Reading": "green",
        "Completed": "blue"
    }.get(status, "gray")

    st.markdown(
        f"""
        <div style="border:1px solid #ddd; border-radius:8px; padding:10px; margin-bottom:10px;">
            <h4>{row['Title']} <span style="background-color:{color}; color:white; padding:2px 6px; border-radius:5px; font-size:0.8em;">{status}</span></h4>
            <b>Author:</b> {row['Author']}<br>
            <b>Genre:</b> {row['Genre']}<br>
            <b>Purchase Date:</b> {row['Purchase Date']}<br>
            <b>Cost:</b> ₹{row['Cost']}<br>
            <b>Audiobook:</b> <a href="{row['Audiobook']}" target="_blank">{row['Audiobook']}</a><br>
            <b>Notes:</b> {row['Notes']}<br>
        </div>
        """,
        unsafe_allow_html=True
    )


# Export
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Export as CSV", data=csv, file_name="books.csv", mime="text/csv")

for _, row in filtered_df.iterrows():
    with st.expander(f"📘 {row['Title']} by {row['Author']}"):
        col1, col2, col3 = st.columns(3)
        new_title = col1.text_input("Title", row["Title"], key=f"title_{row['ID']}")
        new_author = col2.text_input("Author", row["Author"], key=f"author_{row['ID']}")
        new_genre = col3.text_input("Genre", row["Genre"], key=f"genre_{row['ID']}")
        new_date = col1.date_input("Purchase Date", pd.to_datetime(row["Purchase Date"]), key=f"date_{row['ID']}")
        new_cost = col2.number_input("Cost", value=row["Cost"], key=f"cost_{row['ID']}")
        new_link = col3.text_input("Audiobook Link", row["Audiobook"], key=f"link_{row['ID']}")
        new_status = col1.selectbox("Status", ["To Read", "Reading", "Completed"], index=["To Read", "Reading", "Completed"].index(row["Status"]), key=f"status_{row['ID']}")
        new_notes = st.text_area("Notes", row["Notes"], key=f"notes_{row['ID']}")

        col_save, col_delete = st.columns([1, 1])
        if col_save.button("💾 Save Changes", key=f"save_{row['ID']}"):
            update_book(row["ID"], (new_title, new_author, new_genre, str(new_date), new_cost, new_link, new_status, new_notes))
            st.success("✅ Book updated!")
            st.rerun()

        if col_delete.button("🗑️ Delete Book", key=f"delete_{row['ID']}"):
            delete_book(row["ID"])
            st.warning("⚠️ Book deleted!")
            st.rerun()

# # === Summary Tab at the Bottom ===
# st.markdown("---")  # Horizontal separator

# total_books_read = df[df["Status"] == "Completed"].shape[0]
# total_spent = df["Cost"].sum()

# st.markdown(
#     f"""
#     <div style="background-color:#f0f2f6; padding: 15px; border-radius: 10px; text-align: center;">
#         <h4>📊 Summary</h4>
#         <p><b>✅ Books Completed:</b> {total_books_read}</p>
#         <p><b>💸 Total Spent:</b> ₹{total_spent:.2f}</p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# === Summary Tab at the Bottom ===
st.markdown("---")  # Horizontal separator

total_books = df.shape[0]
total_books_read = df[df["Status"] == "Completed"].shape[0]
total_books_unread = df[df["Status"] == "To Read"].shape[0]
total_spent = df["Cost"].sum()

st.markdown(
    f"""
    <div style="background-color:#f0f2f6; padding: 15px; border-radius: 10px; text-align: center;">
        <h4>📊 Summary</h4>
        <p><b>📚 Total Books in Inventory:</b> {total_books}</p>
        <p><b>✅ Books Completed:</b> {total_books_read}</p>
        <p><b>📖 Books To Read:</b> {total_books_unread}</p>
        <p><b>💸 Total Spent:</b> ₹{total_spent:.2f}</p>
    </div>
    """,
    unsafe_allow_html=True
)