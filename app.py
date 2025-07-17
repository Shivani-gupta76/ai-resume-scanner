# app.py
import streamlit as st
from parser import extract_resume_text
from matcher import calculate_similarity
import tempfile
import pandas as pd  # for bar chart

# --------------------------
# Skill matching helper
# --------------------------
def highlight_skills(resume_text, jd_text):
    jd_keywords = [word.lower() for word in jd_text.split() if len(word) > 2]
    matched = []
    missing = []

    for keyword in set(jd_keywords):
        if keyword in resume_text.lower():
            matched.append(keyword)
        else:
            missing.append(keyword)

    return matched, missing

# --------------------------
# Streamlit Config
# --------------------------
st.set_page_config(page_title="AI Resume Scanner", layout="centered")

st.title("🤖 AI Resume Scanner")
st.markdown("Upload resumes and paste the job description to see match scores.")

# --------------------------
# Job Description Input
# --------------------------
jd_text = st.text_area("Paste Job Description Here", height=200)

# --------------------------
# File Uploader
# --------------------------
uploaded_files = st.file_uploader("Upload Resumes (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

# --------------------------
# Analyze Button
# --------------------------
if st.button("Analyze Resumes"):
    if not jd_text.strip():
        st.warning("Please enter a job description.")
    elif not uploaded_files:
        st.warning("Please upload at least one resume.")
    else:
        results = []

        for uploaded_file in uploaded_files:
            # Save uploaded file to a temp path
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name

            # Extract text
            resume_text = extract_resume_text(tmp_path, uploaded_file.name)

            # Match score
            score = calculate_similarity(jd_text, [resume_text])[0]  # Single resume

            # Skill matching
            matched_skills, missing_skills = highlight_skills(resume_text, jd_text)

            # Store everything
            results.append({
                "filename": uploaded_file.name,
                "score": score * 100,  # Convert to %
                "matched": matched_skills,
                "missing": missing_skills
            })

        # Sort by score
        sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

        # --------------------------
        # Display Results
        # --------------------------
        st.subheader("📊 Resume Match Results")

        for res in sorted_results:
            st.markdown(f"### 📄 {res['filename']}")
            st.success(f"✅ Match Score: {res['score']:.2f}%")

            st.markdown("**🟢 Matched Skills:**")
            st.markdown(", ".join([f"`{skill}`" for skill in res["matched"]]) or "None")

            st.markdown("**🔴 Missing Skills:**")
            st.markdown(", ".join([f"`{skill}`" for skill in res["missing"]]) or "None")

            st.markdown("---")

        # --------------------------
        # Bar Chart Visualization
        # --------------------------
        st.subheader("📈 Match Score Comparison")
        chart_data = pd.DataFrame({
            'Resume': [res['filename'] for res in sorted_results],
            'Match Score (%)': [res['score'] for res in sorted_results]
        })

        st.bar_chart(chart_data.set_index('Resume'))
