
import streamlit as st
import openai
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Telecom LLM Demo")
st.markdown("""
### Company X LLM-Powered Sales & Marketing Assistant
This tool analyzes prospects, monitors customer health, automates campaigns, and optimizes construction strategy.
""")

task = st.sidebar.selectbox("Select Task", [
    "Generate Sales Pitch",
    "Analyze Prospects",
    "KPI Dashboard",
    "Campaign Automation",
    "Churn/Upgrade Monitoring",
    "Route Build Optimization",
    "Direct Mail Optimization",
    "Marketing Collateral"
])

# Load sample datasets
sample_files = {
    "Residential": "data/sample_residential.csv",
    "MDU": "data/sample_mdu.csv",
    "Commercial": "data/sample_commercial.csv",
    "All Combined": "data/sample_all_properties.csv"
}

segment = st.sidebar.selectbox("Choose Property Segment", list(sample_files.keys()))
use_custom = st.sidebar.checkbox("Upload Your Own Data")

if use_custom:
    uploaded_file = st.file_uploader("Upload Your Data (CSV)")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("Please upload a CSV file to proceed.")
        st.stop()
else:
    df = pd.read_csv(sample_files[segment])

# KPI Dashboard with Salesforce + Website Integration

def analyze_kpi(df):
    additional_metrics = st.checkbox("Enrich with Contact & Demographic Data")
    if additional_metrics:
        st.info("Simulating API integration: Pulling demographics, income, ownership profiles from a 3rd party website.")
        df["Median Income"] = pd.Series([65000 + (i * 1000) % 20000 for i in range(len(df))])
        df["Owner Occupied %"] = pd.Series([60 + (i * 3) % 40 for i in range(len(df))])
        df["Email Contacts"] = pd.Series([2 + i % 4 for i in range(len(df))])
        st.write("Enriched Data:", df.head())

    if "Region" in df.columns:
        st.subheader("Opportunities by Region")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x="Region", ax=ax)
        st.pyplot(fig)

    if "Stage" in df.columns:
        st.subheader("Opportunities by Stage")
        fig2, ax2 = plt.subplots()
        sns.countplot(data=df, x="Stage", order=df["Stage"].value_counts().index, ax=ax2)
        plt.xticks(rotation=45)
        st.pyplot(fig2)

    prompt = f"""
You are a telecom marketing strategist. Review this CRM and Salesforce data. Identify strong performers, bottlenecks, and campaign readiness. Include demographic impact where applicable.\n\n{df.head(10).to_string()}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a telecom marketing strategist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=600
    )
    st.markdown("### KPI Insights:")
    st.write(response["choices"][0]["message"]["content"])

# Campaign Automation w/ Salesforce Context

def run_campaign_gpt(campaign_name, campaign_description):
    enrichment_prompt = f"""
You are an AI campaign assistant based on CampaignsGPT by SmarterX. Use internal Salesforce deal data and external contact demographics to build a multichannel campaign for:

Campaign: {campaign_name}
Description: {campaign_description}

Tasks:
1. Break campaign into subtasks
2. Assess AI exposure (E0–E3)
3. Recommend tool stack (CRM, email, ads)
4. Prioritize rollout with Salesforce follow-up
5. Add demographic tailoring tips
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are CampaignsGPT—specialist in AI-enhanced marketing execution."},
            {"role": "user", "content": enrichment_prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )
    st.markdown("### CampaignGPT Strategy")
    st.write(response.choices[0].message.content)

# Task Selector Routing
if task == "KPI Dashboard":
    st.subheader("Salesforce & Marketing KPI Analysis")
    st.write("Data Preview:", df.head())
    analyze_kpi(df)

elif task == "Campaign Automation":
    st.subheader("SmarterX CampaignsGPT Integration")
    campaign_name = st.text_input("Campaign Name", "Fiber Rollout Target 2025")
    campaign_description = st.text_area("Campaign Overview", "Engage commercial and MDU properties to increase upgrades, using Salesforce opportunity data.")
    if st.button("Generate Campaign Strategy"):
        run_campaign_gpt(campaign_name, campaign_description)

# Fall-through for all other tasks
else:
    st.info("Please return to Generate Sales Pitch, Prospect Analysis, Churn Monitoring, or Route Optimization to continue using the assistant. This module is actively focused on KPI and Campaign logic enhancements.")
