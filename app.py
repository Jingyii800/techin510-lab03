from datetime import datetime
import streamlit as st

import os
from dataclasses import dataclass, field

import streamlit as st
import psycopg2
from dotenv import load_dotenv

load_dotenv()

con = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = con.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS prompts (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        prompt TEXT NOT NULL,
        type TEXT NOT NULL,
        is_favorite BOOL DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
)

@dataclass
class Prompt:
    title: str
    prompt: str
    type: str = field(default="General")  # Default type if not specified
    is_favorite: bool = field(default=False)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

def prompt_form(prompt=Prompt("","", "General")):
    with st.form(key="prompt_form", clear_on_submit=True):
        title = st.text_input("Title", value=prompt.title)
        prompt = st.text_area("Prompt", height=200, value=prompt.prompt)
        type = st.selectbox("Type", ("Job Hunting", "Academic Practice", "Daily Life", "Work Tool", "Just For Fun", "General"), index=0)
        submitted = st.form_submit_button("Submit")
        if submitted:
            # validation
            if title and prompt and type:
                return Prompt(title, prompt, type)
            else:
                st.warning("Please fill in all required fields!")

if 'edit_prompt_id' not in st.session_state:
    st.session_state.edit_prompt_id = None
def edit_prompt_form(id):
    # Fetch prompt details from the database
    cur.execute("SELECT * FROM prompts WHERE id = %s", (id,))
    data = cur.fetchone()
    with st.form("edit_form", clear_on_submit=False):
        title = st.text_input("Title", value=data[1])
        prompt_text = st.text_area("Prompt", value=data[2])
        submit_button = st.form_submit_button(label="Update Prompt")
        
        if submit_button:
            cur.execute("UPDATE prompts SET title = %s, prompt = %s WHERE id = %s", 
                        (title, prompt_text, id))
            con.commit()
            st.session_state.edit_prompt_id = None  # Clear edit state
            st.success('Prompt updated successfully.')
            return True
    return False

with st.sidebar:
    st.header("Create a New Prompt")
    prompt = prompt_form()
    if prompt:
        cur.execute("INSERT INTO prompts (title, prompt, type) VALUES (%s, %s, %s)", (prompt.title, prompt.prompt,prompt.type))
        con.commit()
        st.success("Prompt added successfully!")

st.title("Prompt Library")
st.subheader("Assists you to store and retrieve prompts")

# Add a search bar
search_query = st.text_input("Search Prompts")

# Add a sort by date
sort_order = st.radio("Sort by", ("Newest", "Oldest"))

# Create the base SQL query
sql_query = "SELECT * FROM prompts"
sql_params = []

# Add search to the SQL query if there's a search query
if search_query:
    sql_query += " WHERE title ILIKE %s OR prompt ILIKE %s"
    sql_params.extend(['%' + search_query + '%', '%' + search_query + '%'])

# Add sorting to the SQL query based on the sort order
if sort_order == "Newest":
    sql_query += " ORDER BY created_at DESC"
else:
    sql_query += " ORDER BY created_at ASC"

# Execute the combined SQL query
cur.execute(sql_query, sql_params)
prompts = cur.fetchall()

for p in prompts:
     with st.expander(f"{p[1]} - {p[3]}"):
        st.code(p[2])
        col1, col2, col3 = st.columns(3)
        # Add favorite button
        with col1:
            fav_text = "Unfavorite" if p[4] else "Favorite"
            if st.button(fav_text, key=f"fav-{p[0]}"):
                cur.execute("UPDATE prompts SET is_favorite = NOT is_favorite WHERE id = %s", (p[0],))
                con.commit()
                st.rerun()
        # Delete Button
        with col2:
            if st.button("Delete", key=f"del-{p[0]}"):
                cur.execute("DELETE FROM prompts WHERE id = %s", (p[0],))
                con.commit()
                st.rerun()
        # Edit button
        with col3:
            if st.button("Edit", key =f"edt-{p[0]}"):
                st.session_state.edit_prompt_id = p[0]

if st.session_state.edit_prompt_id:
    if edit_prompt_form(st.session_state.edit_prompt_id):
        # If the form was submitted, rerun the app to refresh the state
        st.rerun()