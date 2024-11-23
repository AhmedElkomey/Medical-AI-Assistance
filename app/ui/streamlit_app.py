# streamlit_app.py
import streamlit as st
import requests
import json

API_URL = "http://localhost:8000"

def main():
    st.title("Medical AI Interface")

    menu = ["Home", "Process Document", "Query System"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to the Medical AI Interface")

    elif choice == "Process Document":
        st.subheader("Upload and Process a Medical Document")
        doc_id = st.text_input("Document ID")
        content = st.text_area("Content")
        source = st.text_input("Source")
        publication_date = st.date_input("Publication Date")
        medical_categories = st.text_input("Medical Categories (comma-separated)")
        confidence_score = st.slider("Confidence Score", 0.0, 1.0, 0.5)
        verified_by_medical_professional = st.checkbox("Verified by Medical Professional")
        citations = st.text_area("Citations (JSON format)")

        if st.button("Process Document"):
            try:
                citations_json = json.loads(citations) if citations else []
            except json.JSONDecodeError:
                st.error("Invalid JSON format for citations")
                return

            doc = {
                "doc_id": doc_id,
                "content": content,
                "source": source,
                "publication_date": publication_date.isoformat(),
                "medical_categories": [cat.strip() for cat in medical_categories.split(',')],
                "confidence_score": confidence_score,
                "verified_by_medical_professional": verified_by_medical_professional,
                "citations": citations_json
            }
            response = requests.post(f"{API_URL}/process_document/", json=doc)
            if response.status_code == 200:
                st.success("Document processed successfully")
            else:
                st.error(f"Error: {response.json().get('detail')}")

    elif choice == "Query System":
        st.subheader("Query the Medical AI System")
        query = st.text_input("Enter your query")
        if st.button("Search"):
            response = requests.post(f"{API_URL}/query/", json={"query": query})
            if response.status_code == 200:
                results = response.json().get("results", [])
                for res in results:
                    st.write(f"**Score**: {res['score']}")
                    st.write(f"**Content**: {res['content']}")
                    st.write("---")
            else:
                st.error(f"Error: {response.json().get('detail')}")

if __name__ == '__main__':
    main()
