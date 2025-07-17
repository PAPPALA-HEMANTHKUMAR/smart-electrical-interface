import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Connect to your database
engine = create_engine("sqlite:///electrical.db")

st.title("🔧 Smart Electrical Interface Dashboard")

# Load service requests
requests = pd.read_sql("SELECT * FROM service_request", engine)
electricians = pd.read_sql("SELECT * FROM electrician", engine)
feedbacks = pd.read_sql("SELECT * FROM feedback", engine)

# 📌 Job Requests by Location
st.subheader("Service Requests by Location")
loc_count = requests['location'].value_counts()
st.bar_chart(loc_count)

# 🧲 Top Rated Electricians
st.subheader("Top Rated Electricians")
top_electricians = electricians.sort_values(by='rating', ascending=False).head(5)
st.table(top_electricians[['name', 'skills', 'rating', 'location']])

# 🔥 Urgency Breakdown
st.subheader("Requests by Urgency")
urgency_chart = requests['urgency'].value_counts()
st.bar_chart(urgency_chart)