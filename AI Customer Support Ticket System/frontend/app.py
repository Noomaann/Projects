import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import os

BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="AI Support Desk",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 100%);
    font-family: 'Inter', sans-serif;
    color: #1e293b;
}
[data-testid="stHeader"]      { background: transparent; }
[data-testid="stDecoration"]  { display: none; }
.main .block-container        { padding: 2rem 3rem; max-width: 1450px; }

.hero-wrap {
    background: linear-gradient(135deg, #312e81 0%, #4f46e5 100%);
    border-radius: 20px; padding: 40px; margin-bottom: 30px; color: white;
    box-shadow: 0 10px 30px rgba(79, 70, 229, 0.2);
}
.hero-badge {
    display: inline-block; background: rgba(255,255,255,0.2); font-size: 0.75rem; font-weight: 700;
    padding: 4px 12px; border-radius: 50px; margin-bottom: 16px; text-transform: uppercase;
}
.hero-title { font-size: 2.4rem; font-weight: 700; margin: 0 0 8px 0; letter-spacing: -0.5px; }
.hero-sub { font-size: 1rem; opacity: 0.9; margin: 0; }

.cards-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
.metric-card {
    background: white; border-radius: 16px; padding: 30px 24px; text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid rgba(255,255,255,0.5);
}
.card-val { font-size: 2.4rem; font-weight: 800; color: #0f172a; margin: 0 0 8px 0; line-height: 1; }
.card-label { font-size: 0.8rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }

.sec-title { font-size: 1.2rem; font-weight: 700; color: #0f172a; margin: 15px 0 15px; text-transform: uppercase; letter-spacing: 0.5px; }
.chart-wrap {
    background: white; border-radius: 16px; padding: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid rgba(255,255,255,0.5); margin-bottom: 30px;
}

[data-testid="stExpander"] {
    background: white !important; border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.02) !important; margin-bottom: 16px !important;
}
[data-testid="stExpander"] summary { font-family: 'Inter', sans-serif !important; font-weight: 600 !important; color: #0f172a !important; padding: 12px 16px !important; }

.badges { display: flex; gap: 8px; margin-bottom: 15px; }
.badge { padding: 4px 14px; border-radius: 50px; font-size: 0.75rem; font-weight: 600; }
.b-high { background: #fee2e2; color: #ef4444; border: 1px solid #fca5a5; }
.b-med { background: #fef3c7; color: #d97706; border: 1px solid #fcd34d; }
.b-low { background: #dcfce3; color: #16a34a; border: 1px solid #86efac; }
.b-pos { background: #dcfce3; color: #16a34a; border: 1px solid #86efac; }
.b-neg { background: #fee2e2; color: #ef4444; border: 1px solid #fca5a5; }
.b-neu { background: #e0f2fe; color: #0284c7; border: 1px solid #7dd3fc; }

.t-msg { background: #f8fafc; border-left: 4px solid #cbd5e1; padding: 16px; color: #334155; font-style: italic; border-radius: 0 8px 8px 0; margin-bottom: 15px; }
.error-box { text-align: center; padding: 30px; background: #fee2e2; border-radius: 16px; color: #ef4444; border: 1px solid #fca5a5;}
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("<h3 style='color: #0f172a;'>Add New Ticket</h3>", unsafe_allow_html=True)
    st.markdown("Simulate a customer sending a message.")
    
    with st.form("new_ticket_form", clear_on_submit=True):
        new_msg = st.text_area("Customer Message", placeholder="Type customer message here...", height=150)
        submit_btn = st.form_submit_button("Submit Ticket")

        if submit_btn and new_msg:
            try:
                # ডকার ফ্রেন্ডলি URL ব্যবহার করা হয়েছে
                res = requests.post(f"{BASE_URL}/tickets/", json={"customer_message": new_msg})
                if res.status_code == 200:
                    st.success("Ticket added successfully!")
                    st.rerun() 
                else:
                    st.error("Failed to add ticket.")
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")


st.markdown("""
<div class="hero-wrap">
    <span class="hero-badge">Live · AI-Powered</span>
    <div class="hero-title">Customer Support Desk</div>
    <p class="hero-sub">Real-time ticket classification · Sentiment analysis · AI reply drafts</p>
</div>
""", unsafe_allow_html=True)

try:
    # ডকার ফ্রেন্ডলি URL ব্যবহার করা হয়েছে
    response = requests.get(f"{BASE_URL}/tickets/all", timeout=5)

    if response.status_code == 200:
        tickets = response.json()

        if not tickets:
            st.info("No tickets yet — submit your first one from the sidebar.")
        else:
            df = pd.DataFrame(tickets)
            df["category"] = df["category"].fillna("Unknown")
            df["sentiment"] = df["sentiment"].fillna("Neutral")
            df["priority_score"] = df["priority_score"].fillna("Medium")

            total = len(df)
            high_pri = len(df[df["priority_score"] == "High"])
            neg_sent = len(df[df["sentiment"] == "Negative"])
            top_cat = df["category"].mode()[0]


            st.markdown(f"""
            <div class="cards-row">
                <div class="metric-card"><div class="card-val">{total}</div><div class="card-label">Total Tickets</div></div>
                <div class="metric-card"><div class="card-val">{high_pri}</div><div class="card-label">High Priority</div></div>
                <div class="metric-card"><div class="card-val">{neg_sent}</div><div class="card-label">Negative Sentiment</div></div>
                <div class="metric-card"><div class="card-val" style="font-size:1.6rem; margin:10px 0;">{top_cat}</div><div class="card-label">Top Category</div></div>
            </div>
            """, unsafe_allow_html=True)


            st.markdown('<div class="sec-title">Website Stats</div>', unsafe_allow_html=True)
            c1, c2 = st.columns([6, 4], gap="large")

            LIGHT_LAYOUT = dict(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#64748b", size=12),
                margin=dict(l=10, r=10, t=40, b=10),
                title=dict(font=dict(color="#0f172a", size=16), x=0.01, y=0.98),
            )

    
            with c1:
                cat_df = df["category"].value_counts().reset_index()
                bar_colors = ["#29B6F6", "#42A5F5", "#81D4FA", "#039BE5", "#00ACC1", "#4DD0E1"]
                fig1 = go.Figure(go.Bar(
                    x=cat_df["category"], y=cat_df["count"],
                    marker=dict(color=bar_colors[:len(cat_df)])
                ))
                fig1.update_layout(**LIGHT_LAYOUT, title_text="Tickets by Category", yaxis=dict(gridcolor="rgba(0,0,0,0.05)"), height=320)
                st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
                st.plotly_chart(fig1, width="stretch")
                st.markdown('</div>', unsafe_allow_html=True)

           
            with c2:
                pri_df = df["priority_score"].value_counts().reset_index()
                donut_colors = ["#9C27B0" if p=="High" else "#FFCA28" if p=="Medium" else "#66BB6A" for p in pri_df["priority_score"]]
                fig2 = go.Figure(go.Pie(
                    labels=pri_df["priority_score"], values=pri_df["count"], hole=0.55,
                    marker=dict(colors=donut_colors)
                ))
                fig2.update_layout(**LIGHT_LAYOUT, title_text="Priority Distribution", height=320)
                st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
                st.plotly_chart(fig2, width="stretch")
                st.markdown('</div>', unsafe_allow_html=True)

          
            st.markdown('<div class="sec-title">Recent Tickets</div>', unsafe_allow_html=True)
            
            for t in tickets:
                p = t.get("priority_score", "Medium")
                s = t.get("sentiment", "Neutral")
                c = t.get("category", "Unknown")
                msg = t.get("customer_message", "")
                reply = t.get("ai_reply_draft", "") if t.get("ai_reply_draft") else ""
                
                p_cls = "b-high" if p == "High" else "b-med" if p == "Medium" else "b-low"
                s_cls = "b-pos" if s == "Positive" else "b-neg" if s == "Negative" else "b-neu"
                
                preview = msg[:65] + "..." if len(msg) > 65 else msg
                expander_label = f"Ticket #{t['id']} | Category: {c} | Priority: {p}"
                
                with st.expander(expander_label):
                    st.markdown(f"""
                    <div style="padding-top: 5px;">
                        <div class="badges">
                            <span class="badge {s_cls}">Sentiment: {s}</span>
                            <span class="badge {p_cls}">Priority: {p}</span>
                        </div>
                        <div style="font-size:0.8rem; font-weight:700; color:#64748b; margin-bottom:5px; text-transform:uppercase;">Customer Message</div>
                        <div class="t-msg">"{msg}"</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    edited_reply = st.text_area(
                        "AI Reply Draft (Edit if needed):", 
                        value=reply, 
                        key=f"reply_{t['id']}",
                        height=100
                    )
                    
                    if st.button("Approve & Send Reply", key=f"btn_{t['id']}"):
                        st.success(f"Reply sent successfully for Ticket #{t['id']}!")

except Exception as e:
    st.markdown(f"""
    <div class="error-box">
        <div style="font-size:1.5rem; font-weight: 700; margin-bottom:10px">Backend Error</div>
        Ensure FastAPI is running! (Details: {e})
    </div>""", unsafe_allow_html=True)
