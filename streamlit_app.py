import streamlit as st
import json
from collections import defaultdict

# --- App Title and Password ---
st.set_page_config(page_title="n8n Workflow Classifier", layout="wide")
st.title("🧠 n8n Workflow Classifier (Private)")

# --- Authentication ---
password = st.text_input("Enter password", type="password")
if password != "0123":
    st.warning("Access denied.")
    st.stop()

st.success("Access granted ✅")

# --- Initialize session storage ---
if "workflows" not in st.session_state:
    st.session_state.workflows = []

# --- Upload Section ---
uploaded_files = st.file_uploader("Upload one or more n8n workflows (.json)", type="json", accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        try:
            wf = json.load(file)
            nodes = wf.get("nodes", [])
            file_info = {
                "filename": file.name,
                "nodes": nodes,
                "category": "Uncategorized",
                "subcategory": "Other"
            }

            # --- Rule-based Classification ---
            services = [node["type"].lower() for node in nodes]
            if any("slack" in s for s in services):
                file_info["category"] = "Internal Tools"
                file_info["subcategory"] = "Communication"
            elif any("hubspot" in s or "crm" in s for s in services):
                file_info["category"] = "Sales"
                file_info["subcategory"] = "CRM Sync"
            elif any("mailchimp" in s or "email" in s for s in services):
                file_info["category"] = "Marketing"
                file_info["subcategory"] = "Email Campaigns"
            elif any("zendesk" in s or "support" in s for s in services):
                file_info["category"] = "Customer Support"
                file_info["subcategory"] = "Ticketing"
            elif any("airtable" in s or "notion" in s for s in services):
                file_info["category"] = "Internal Tools"
                file_info["subcategory"] = "Data Tools"

            st.session_state.workflows.append(file_info)

        except Exception as e:
            st.error(f"❌ Error reading {file.name}: {str(e)}")

# --- Group and Display by Category/Subcategory ---
workflow_data = st.session_state.workflows
if not workflow_data:
    st.info("No workflows uploaded yet.")
else:
    st.subheader("📂 Browse Workflows by Category")

    category_tree = defaultdict(lambda: defaultdict(list))
    for wf in workflow_data:
        category_tree[wf["category"]][wf["subcategory"]].append(wf)

    for category, subcats in category_tree.items():
        with st.expander(f"📁 {category} ({sum(len(v) for v in subcats.values())} workflows)"):
            for subcat, files in subcats.items():
                with st.expander(f"📂 {subcat} ({len(files)} files)"):
                    for wf in files:
                        with st.expander(f"📄 {wf['filename']}"):
                            st.write(f"🔢 **Node Count**: {len(wf['nodes'])}")
                            st.write("🧩 **Nodes:**")
                            for node in wf["nodes"]:
                                st.markdown(f"- **{node['name']}** (`{node['type']}`)")
