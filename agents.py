import pandas as pd
import random
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# --- Generative AI Insight Engine (Rule-Based Simulation) ---
def generate_ai_insight(df, kpis):
    """Simulates an AI agent generating business insight."""
    sales_growth = kpis.get('growth', 0)
    top_region = df.groupby('Region')['Sales'].sum().idxmax()
    low_profit_product = df.loc[df['Profit'].idxmin(), 'Product']

    if sales_growth > 0.10:
        recommendation = f"Maintain high volume focus; explore expansion in the top-performing {top_region} region."
    elif sales_growth < -0.05:
        recommendation = f"Urgent action: Investigate profitability issues with product '{low_profit_product}' and consider targeted promotions."
    else:
        recommendation = "Performance is stable. Focus on increasing profitability margins across all regions and optimize logistics."

    summary = (
        f"**AI Insight Summary:** Total sales growth is **{sales_growth:+.2%}** compared to the previous period. "
        f"The top performing region is **{top_region}**, and the system recommends: *{recommendation}*"
    )
    return summary

# --- Agentic Functions (Orchestrated Steps) ---
def DataAgent(file_path):
    """Agent 1: Reads data from the specified path."""
    print("Agent Log: DataAgent: Reading sales data...")
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')
    return df

def AnalyticsAgent(df):
    """Agent 2: Calculates Key Performance Indicators (KPIs)."""
    print("Agent Log: AnalyticsAgent: Calculating core KPIs...")
    kpis = {}
    
    current_sales = df['Sales'].sum()
    # Simulate a previous period's sales figure (for growth KPI)
    prev_sales = df['Sales'].sample(frac=0.5, random_state=42).sum() 
    
    kpis['Total Sales'] = f"₹{current_sales:,.0f}"
    kpis['Average Profit'] = f"₹{df['Profit'].mean():,.0f}"
    kpis['Sales Growth'] = (current_sales - prev_sales) / prev_sales
    kpis['Growth Text'] = f"{kpis['Sales Growth']:+.2%}"
    
    return kpis

def VisualizationAgent(df):
    """Agent 3: Generates visual charts and encodes them for the web app."""
    print("Agent Log: VisualizationAgent: Generating web charts...")
    
    charts_data = {}
    
    # Chart 1: Sales by Region (Bar Chart)
    fig, ax = plt.subplots(figsize=(6, 4))
    region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    region_sales.plot(kind='bar', ax=ax, color='#054ADA')
    ax.set_title("Sales by Region", fontsize=14)
    ax.set_xlabel("Region")
    ax.set_ylabel("Total Sales (₹)")
    plt.xticks(rotation=0)
    
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png', bbox_inches='tight')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    charts_data['RegionChart'] = encoded
    plt.close(fig)

    # Chart 2: Product Profitability (Pie Chart)
    fig, ax = plt.subplots(figsize=(6, 4))
    product_profit = df.groupby('Product')['Profit'].sum()
    ax.pie(product_profit, labels=product_profit.index, autopct='%1.1f%%', startangle=90)
    ax.set_title("Product Profit Share", fontsize=14)
    
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png', bbox_inches='tight')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    charts_data['ProductChart'] = encoded
    plt.close(fig)
    
    return charts_data

def InsightAgent(df, kpis):
    """Agent 4: Generates the Final AI Insight."""
    print("Agent Log: InsightAgent: Generating AI summary...")
    insight = generate_ai_insight(df, kpis)
    return insight

def ReportAgent():
    """Agent 5: Simulates final report assembly."""
    print("Agent Log: ReportAgent: Final report assembled and ready for dispatch.")
    return "Process Completed! Data ready for download."