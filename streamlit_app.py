import streamlit as st
import json

# --- Basic Auth ---
st.title("Private n8n Workflow Classifier")

password = st.text_input("Enter password to continue", type="password")
if password != "0123":
    st.warning("Access denied. Please enter the correct password.")
    st.stop()

st.success("Access granted.")

# --- Upload and Process Workflow ---
uploaded_file = st.file_uploader("Upload a n8n workflow (.json)", type="json")

def classify_workflow(nodes):
    services = [node['type'].lower() for node in nodes]
    if any("slack" in s for s in services):
        return "Internal Communication"
    elif any("hubspot" in s or "crm" in s for s in services):
        return "Sales"
    elif any("mailchimp" in s or "email" in s for s in services):
        return "Marketing"
    elif any("zendesk" in s or "support" in s for s in services):
        return "Customer Support"
    else:
        return "Uncategorized"

if uploaded_file:
    workflow = json.load(uploaded_file)
    nodes = workflow.get("nodes", [])
    
    st.subheader("Workflow Summary")
    st.write(f"📦 Nodes: {len(nodes)}")
    for node in nodes:
        st.write(f"- {node['name']} ({node['type']})")
    
    category = classify_workflow(nodes)
    st.success(f"Predicted Category: **{category}**")
