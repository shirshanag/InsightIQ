from dotenv import load_dotenv  
load_dotenv()  
from langchain_groq import ChatGroq  
from langchain.agents import create_agent  
from langgraph.checkpoint.memory import InMemorySaver  
from langchain.tools import tool   
import pandas as pd  
import plotly.express as px  

import streamlit as st  

st.set_page_config(page_title="InsightIQ | AI data analyst", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Manrope:wght@400;500;600;700&display=swap');
:root{--ink:#0a0e1c;--panel:#131a30;--panel2:#1a2242;--line:#28324f;--text:#e9ecf8;--muted:#8d97ba;--violet:#7c6cff;--aqua:#35d0ba;}
html,body,[class*="css"],.stApp{font-family:'Manrope',sans-serif;color:var(--text);}
.stApp{background:radial-gradient(1000px 600px at 90% -10%,rgba(124,108,255,.22),transparent 60%),radial-gradient(800px 500px at -10% 5%,rgba(53,208,186,.12),transparent 60%),linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px) 0 0/44px 44px,linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px) 0 0/44px 44px,var(--ink);}
header[data-testid="stHeader"],#MainMenu,footer,[data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none!important;}
.block-container{max-width:1180px;padding-top:1.4rem;}

/* nav */
.brand{display:flex;align-items:center;gap:10px;font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:1.35rem;letter-spacing:-.02em;padding-top:4px;}
.logo{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:linear-gradient(135deg,var(--violet),var(--aqua));color:#0a0e1c;font-size:1.05rem;}
div[role="radiogroup"]{gap:4px;background:rgba(255,255,255,.04);border:1px solid var(--line);padding:5px;border-radius:999px;width:fit-content;margin-left:auto;backdrop-filter:blur(8px);}
div[role="radiogroup"] label{padding:6px 20px;border-radius:999px;cursor:pointer;margin:0;transition:background .2s;}
div[role="radiogroup"] label>div:first-child{display:none;}
div[role="radiogroup"] label p{font-weight:600;font-size:.93rem;color:var(--muted);}
div[role="radiogroup"] label:has(input:checked){background:linear-gradient(90deg,var(--violet),#5a8cff);}
div[role="radiogroup"] label:has(input:checked) p{color:#fff;}
.navline{height:1px;background:var(--line);margin:14px 0 30px;}

/* hero */
.badge{display:inline-flex;gap:8px;align-items:center;padding:6px 14px;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.04);font-size:.85rem;color:var(--muted);}
.dot{width:8px;height:8px;border-radius:50%;background:var(--aqua);box-shadow:0 0 10px var(--aqua);}
.h1{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:4rem;line-height:1.02;letter-spacing:-.04em;margin:18px 0 16px;}
.grad{background:linear-gradient(90deg,var(--violet),var(--aqua));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.lead{color:var(--muted);font-size:1.12rem;line-height:1.6;max-width:34rem;margin-bottom:22px;}
.mock{position:relative;background:linear-gradient(160deg,var(--panel2),var(--panel));border:1px solid var(--line);border-radius:22px;padding:18px;box-shadow:0 30px 80px rgba(0,0,0,.5),0 0 0 1px rgba(124,108,255,.15);}
.mock:before{content:"";position:absolute;inset:-60px;z-index:-1;background:radial-gradient(circle,rgba(124,108,255,.35),transparent 60%);animation:drift 9s ease-in-out infinite alternate;}
@keyframes drift{from{transform:translate(-20px,10px)}to{transform:translate(25px,-15px)}}
.bar3{display:flex;gap:6px;margin-bottom:14px}.bar3 i{width:10px;height:10px;border-radius:50%;background:#33406a}
.q{background:var(--panel2);border:1px solid var(--line);border-radius:14px 14px 14px 4px;padding:10px 14px;font-size:.92rem;width:fit-content;margin-bottom:10px;}
.a{background:rgba(124,108,255,.12);border:1px solid rgba(124,108,255,.35);border-radius:14px;padding:14px;font-size:.92rem;}
.bars{display:flex;align-items:flex-end;gap:10px;height:110px;margin-top:12px;}
.bars b{flex:1;border-radius:6px 6px 2px 2px;background:linear-gradient(180deg,var(--aqua),var(--violet));}

/* sections */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line);border:1px solid var(--line);border-radius:16px;overflow:hidden;margin:46px 0 10px;}
.stats div{background:var(--panel);padding:18px 20px;}
.stats strong{display:block;font-family:'Space Grotesk',sans-serif;font-size:1.5rem;}
.stats span{color:var(--muted);font-size:.9rem;}
.h2{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:2.1rem;letter-spacing:-.03em;margin:54px 0 6px;}
.sub{color:var(--muted);margin-bottom:22px;max-width:40rem;}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}
.card{background:linear-gradient(160deg,var(--panel2),var(--panel));border:1px solid var(--line);border-radius:18px;padding:22px;transition:border-color .2s,transform .2s;}
.card:hover{border-color:var(--violet);transform:translateY(-3px);}
.ico{width:42px;height:42px;border-radius:12px;display:grid;place-items:center;background:rgba(124,108,255,.16);font-size:1.2rem;margin-bottom:14px;}
.card h4{font-family:'Space Grotesk',sans-serif;font-size:1.15rem;margin:0 0 6px;}
.card p{color:var(--muted);font-size:.94rem;line-height:1.55;margin:0;}
.step{font-family:'Space Grotesk',sans-serif;font-size:1.9rem;font-weight:700;color:var(--violet);margin-bottom:6px;}
.cta{margin-top:56px;padding:40px;border-radius:24px;text-align:center;border:1px solid rgba(124,108,255,.4);background:linear-gradient(120deg,rgba(124,108,255,.25),rgba(53,208,186,.14));}
.cta h3{font-family:'Space Grotesk',sans-serif;font-size:2rem;letter-spacing:-.03em;margin:0 0 6px;}
.foot{color:var(--muted);text-align:center;font-size:.85rem;margin:50px 0 10px;padding-top:18px;border-top:1px solid var(--line);}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 6px;}
.chip{padding:7px 14px;border-radius:999px;border:1px solid var(--line);background:var(--panel);font-size:.88rem;color:var(--muted);}

/* buttons */
button[kind="primary"],[data-testid="stBaseButton-primary"]{background:linear-gradient(90deg,var(--violet),#5a8cff)!important;border:0!important;border-radius:12px!important;padding:.6rem 1.5rem!important;font-weight:700!important;box-shadow:0 10px 30px rgba(124,108,255,.4);}
button[kind="secondary"],[data-testid="stBaseButton-secondary"]{background:transparent!important;border:1px solid var(--line)!important;border-radius:12px!important;padding:.6rem 1.5rem!important;color:var(--text)!important;font-weight:600!important;}

/* app widgets */
[data-testid="stFileUploader"] section{background:var(--panel);border:1.5px dashed var(--line);border-radius:16px;}
[data-testid="stFileUploader"] section:hover{border-color:var(--violet);background:var(--panel2);}
[data-testid="stMetric"]{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--violet);padding:14px 18px;border-radius:14px;}
[data-testid="stMetricLabel"]{color:var(--muted);}
[data-testid="stExpander"]{background:var(--panel);border:1px solid var(--line);border-radius:14px;}
[data-testid="stChatMessage"]{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:14px 18px;margin-bottom:10px;}
[data-testid="stChatInput"]{border-radius:16px;border:1px solid var(--line);}
[data-testid="stChatInput"]:focus-within{border-color:var(--violet);box-shadow:0 0 0 3px rgba(124,108,255,.25);}
[data-testid="stVerticalBlockBorderWrapper"]{border-radius:16px;border-color:var(--line);background:var(--panel);}
@media(max-width:900px){.grid3,.stats{grid-template-columns:1fr 1fr}.h1{font-size:2.6rem}}
@media(max-width:600px){.grid3,.stats{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>
""", unsafe_allow_html=True)

_df:pd.DataFrame=None  
 
_chart_data = None                         
_chart_type = None                         
_chart_color = None
 
def set_df(df:pd.DataFrame):  
    global _df  
    _df=df 
 
if "messages" not in st.session_state:  
    st.session_state.messages=[]  
if "chart_data" not in st.session_state:  
    st.session_state.chart_data = None  
  
if "chart_type" not in st.session_state:  
    st.session_state.chart_type = None  

if "chart_color" not in st.session_state:
    st.session_state.chart_color = None
 
@tool  
def get_data_info():  
    """ Get columns, datatypes, first 5 rows of uploadeed csv file """  
    if  _df is None:  
        return "No csv found"  
    return f"""  
        Shape:{_df.shape},  
        Columns & Datatype: {_df.dtypes.to_string()},  
        First five rows:{_df.head()}  
"""  
 
@tool   
def filter_tool(condition:str):  
    """ Filter rows using query condition   
    Example: age>30 and Department="Engineering"  
    """  
    if  _df is None:  
        return "No csv found"  
    try:  
        result=_df.query(condition)  
        return f"Found {len(result)} rows:{result.to_string()}"  
    except Exception as e:  
        return f"Error:{e}"  
 
@tool  
def analyze_data(expression:str):  
    """ Run pandas expression on the data-frame (referred to as df)   
    Example: df["salary"].mean()  
      
    """  
    if  _df is None:  
        return "No csv found"  
    try:  
        df = _df  
        result=eval(expression)  
        return str(result)  
    except Exception as e:  
        return f"Error:{e}"  
 
@tool  
def create_chart(expression: str, chart_type: str,color: str = ""):  
    """Create a visualization from the uploaded CSV data.  
  
    Use this tool whenever the user asks for a chart, graph,  
    plot, visualization, trend, comparison, distribution,  
    or relationship between columns.  
  
    The expression must be a valid pandas expression using df.  
  
    Supported chart types:  
    - bar  
    - line  
    - scatter  
    - pie  

    color:
    - Optional color requested by the user.
    """  
      
    if _df is None:  
        return "No csv found"  
  
    try:  
        global _chart_data, _chart_type, _chart_color
 
        df = _df  
  
        # Execute the pandas expression generated by the LLM  
        result = eval(expression)  
  
        if not isinstance(result, (pd.Series, pd.DataFrame)):  
            return "Chart expression must return a pandas Series or DataFrame."  
  
        if chart_type not in ["bar", "line", "scatter", "pie"]:  
            return "Unsupported chart type. Use bar, line, scatter, or pie."  
  
        # Convert Series into DataFrame  
        if isinstance(result, pd.Series):  
            result = result.reset_index()  
         
        _chart_data = result                          
        _chart_type = chart_type   
        _chart_color = color
  
        return f"{chart_type} chart created successfully."  
  
    except Exception as e:  
        return f"Error creating chart: {e}"  
  
all_tools=[get_data_info,filter_tool,analyze_data,create_chart]  
llm=ChatGroq(model="openai/gpt-oss-120b")  
 
system_prompt = """    
You are a data analyst assistant. You help the user explore and analyze CSV data.  
  
Use the available tools to answer the user's questions.  
  
Tools:  
  
get_data_info:  
- Get the dataset shape, columns, datatypes, and first 5 rows.  
  
filter_tool:  
- Filter rows using a pandas query condition.  
  
analyze_data:  
- Run a pandas expression on the dataframe for calculations,  
  aggregations, sorting, and retrieving data.  
- The dataframe is available as `df`.  
  
create_chart:  
- Create a visualization from the uploaded CSV data.  
- Use this tool whenever the user asks for a chart, graph, plot,  
  visualization, trend, comparison, distribution, or relationship.  
- The expression must use the dataframe `df`.  
- Supported chart types are:  
  bar, line, scatter, pie.  
- If the user requests specific chart colors, you MUST pass those colors to create_chart.
- Example: if the user says "green and orange", call create_chart with color="green, orange".
- If the user does not request a color, pass color="".
  
Chart selection:  
- Use bar for categorical comparisons.  
- Use line for trends or time-series data.  
- Use scatter for relationships between two numerical variables.  
- Use pie for part-to-whole distributions.  
  
When the user explicitly asks for a visualization, ALWAYS use  
create_chart instead of only returning the calculated numbers.  
"""  
 
agent=create_agent(model=llm,tools=all_tools,checkpointer=InMemorySaver(),system_prompt=system_prompt)  
  
def run_agent(query:str):  
    res=agent.invoke(  
        {'messages':[{'role':'user','content':query}]},  
        {'configurable':{'thread_id':'1'}}  
    )  
    answer=res["messages"][-1].content  
    return answer  


# ---------------------------------------------------------------------------
# UI (presentation only)
# ---------------------------------------------------------------------------
AVATARS = {"user": "🧑‍💻", "ai": "✨"}

def style_fig(fig):
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Manrope, sans-serif", color="#e9ecf8"),
        title_font=dict(family="Space Grotesk, sans-serif", size=20),
        margin=dict(l=20, r=20, t=60, b=20),
    )
    fig.update_xaxes(gridcolor="#28324f", zerolinecolor="#28324f")
    fig.update_yaxes(gridcolor="#28324f", zerolinecolor="#28324f")
    return fig

def go(target):
    st.session_state.nav = target

if "nav" not in st.session_state:
    st.session_state.nav = "Home"
# keep the uploaded dataset available when switching pages
if st.session_state.get("df") is not None:
    set_df(st.session_state.df)

nav_l, nav_r = st.columns([1, 1])
with nav_l:
    st.markdown('<div class="brand"><div class="logo">◆</div>InsightIQ</div>', unsafe_allow_html=True)
with nav_r:
    page = st.radio("Navigate", ["Home", "Analyze", "About"], key="nav", horizontal=True, label_visibility="collapsed")
st.markdown('<div class="navline"></div>', unsafe_allow_html=True)

# ------------------------------- HOME --------------------------------------
if page == "Home":
    left, right = st.columns([1.1, 1], gap="large")
    with left:
        st.markdown("""
<span class="badge"><span class="dot"></span>Powered by LangChain agents and gpt-oss-120b</span>
<div class="h1">Ask your data <span class="grad">anything.</span></div>
<div class="lead">Upload a CSV and talk to it in plain English. InsightIQ writes the pandas, runs it, and draws the chart, so you get answers in seconds instead of hours.</div>
""", unsafe_allow_html=True)
        b1, b2, _ = st.columns([1, 1, 1])
        b1.button("Start analyzing", type="primary", on_click=go, args=("Analyze",), use_container_width=True)
        b2.button("How it works", on_click=go, args=("About",), use_container_width=True)
    with right:
        st.markdown("""
<div class="mock"><div class="bar3"><i></i><i></i><i></i></div>
<div class="q">Show average salary by department</div>
<div class="a">Engineering leads at the highest average. Here is the comparison:
<div class="bars"><b style="height:92%"></b><b style="height:68%"></b><b style="height:55%"></b><b style="height:78%"></b><b style="height:40%"></b></div></div></div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="stats"><div><strong>4</strong><span>chart types</span></div><div><strong>Plain English</strong><span>no code needed</span></div><div><strong>Any CSV</strong><span>drop in and go</span></div><div><strong>Seconds</strong><span>to first answer</span></div></div>
<div class="h2">Everything an analyst does, on demand</div>
<div class="sub">Four purpose-built tools give the agent what it needs to explore, filter, calculate and visualize.</div>
<div class="grid3">
<div class="card"><div class="ico">💬</div><h4>Conversational analysis</h4><p>Ask follow-up questions and the agent remembers the thread of the conversation.</p></div>
<div class="card"><div class="ico">📈</div><h4>Instant charts</h4><p>Bar, line, scatter and pie charts, picked to fit your question and colored the way you ask.</p></div>
<div class="card"><div class="ico">🔎</div><h4>Smart filtering</h4><p>Slice rows by any condition, like age over 30 in Engineering, without writing a query.</p></div>
<div class="card"><div class="ico">🧮</div><h4>Real calculations</h4><p>Averages, sums, rankings and group-bys are computed by pandas, not guessed by the model.</p></div>
<div class="card"><div class="ico">🗂️</div><h4>Auto data profiling</h4><p>Shape, column types and a preview of your rows the moment a file is loaded.</p></div>
<div class="card"><div class="ico">⚡</div><h4>Fast inference</h4><p>Runs on Groq, so responses feel immediate even for multi-step questions.</p></div>
</div>
<div class="h2">From file to insight in three steps</div>
<div class="grid3" style="margin-top:18px">
<div class="card"><div class="step">1</div><h4>Upload your CSV</h4><p>Drag in any comma-separated file. Nothing to configure.</p></div>
<div class="card"><div class="step">2</div><h4>Ask a question</h4><p>Type it the way you would say it to a colleague.</p></div>
<div class="card"><div class="step">3</div><h4>Get answers and charts</h4><p>Read the explanation and see the visualization right below it.</p></div>
</div>
<div class="cta"><h3>Ready to explore your data?</h3><div class="sub" style="margin:0 auto">Upload a file and ask your first question.</div></div>
""", unsafe_allow_html=True)
    _, c, _ = st.columns([1.2, 1, 1.2])
    c.button("Open the analyzer", type="primary", on_click=go, args=("Analyze",), use_container_width=True, key="cta_btn")

# ------------------------------- ABOUT -------------------------------------
elif page == "About":
    st.markdown("""
<span class="badge"><span class="dot"></span>About InsightIQ</span>
<div class="h1" style="font-size:3rem">An analyst that never <span class="grad">sleeps.</span></div>
<div class="lead">InsightIQ turns a CSV into a conversation. Under the hood, an AI agent decides which tool to use, runs real pandas code on your data, and explains the result.</div>
<div class="h2" style="margin-top:30px">The agent's toolkit</div>
<div class="grid3" style="margin-top:14px">
<div class="card"><div class="ico">🗂️</div><h4>get_data_info</h4><p>Reads the shape, column types and first rows so the agent understands your file.</p></div>
<div class="card"><div class="ico">🔎</div><h4>filter_tool</h4><p>Filters rows using a pandas query condition.</p></div>
<div class="card"><div class="ico">🧮</div><h4>analyze_data</h4><p>Runs calculations, aggregations and sorting on the dataframe.</p></div>
<div class="card"><div class="ico">📈</div><h4>create_chart</h4><p>Builds a bar, line, scatter or pie chart with optional colors.</p></div>
<div class="card"><div class="ico">🧠</div><h4>Memory</h4><p>LangGraph keeps the conversation context so follow-ups just work.</p></div>
<div class="card"><div class="ico">🎨</div><h4>Plotly and Streamlit</h4><p>Interactive charts in a clean web interface.</p></div>
</div>
<div class="h2">Questions</div>
""", unsafe_allow_html=True)
    with st.expander("What data can I upload?"):
        st.write("Any CSV file. Column types are detected automatically when the file loads.")
    with st.expander("Is my data sent anywhere?"):
        st.write("Your file is processed in your session. To write answers, the model receives tool outputs such as sample rows and query results, and these are sent to the Groq API.")
    with st.expander("Can it make mistakes?"):
        st.write("Calculations are done by pandas, but the model chooses which expression to run. Check important numbers against your source data.")
    st.button("Try it now", type="primary", on_click=go, args=("Analyze",), key="about_btn")

# ------------------------------- ANALYZE -----------------------------------
else:
    st.markdown('<div class="h1" style="font-size:2.6rem;margin-top:0">Analyze your <span class="grad">data</span></div>', unsafe_allow_html=True)
    file=st.file_uploader("Select your CSV file",type="csv")  
    if file:  
        df=pd.read_csv(file)  
        set_df(df)  
        st.session_state.df = df
        st.dataframe(df.head())  
        st.success(f"Loaded {df.shape[0]} rows.")  
    elif st.session_state.get("df") is not None:
        st.caption("Using the dataset you uploaded earlier.")

    if st.session_state.get("df") is not None:
        d = st.session_state.df
        m1, m2, m3 = st.columns(3)
        m1.metric("Rows", f"{d.shape[0]:,}")
        m2.metric("Columns", f"{d.shape[1]:,}")
        m3.metric("Missing values", f"{int(d.isna().sum().sum()):,}")
    else:
        st.info("Upload a CSV to get started.")

    st.markdown('<div class="chips"><span class="chip">Which column has missing values?</span><span class="chip">Average salary by department as a bar chart</span><span class="chip">Plot the monthly trend in green</span><span class="chip">Pie chart of the category split</span></div>', unsafe_allow_html=True)

    for msg in st.session_state.messages:  
        role=msg["role"]  
        content=msg["content"]  
        st.chat_message(role, avatar=AVATARS.get(role)).markdown(content)  
 
    query=st.chat_input("Ask anything...")  
 
    if query:  
        st.chat_message("user", avatar=AVATARS["user"]).markdown(query)  
        st.session_state.messages.append({"role":"user","content":query})  
     
        with st.spinner("Analyzing your data..."):
            res=run_agent(query)  
 
        # transfer chart data to Streamlit after agent finishes 
        if _chart_data is not None: 
            st.session_state.chart_data = _chart_data 
            st.session_state.chart_type = _chart_type 
            st.session_state.chart_color = _chart_color
     
        st.chat_message("ai", avatar=AVATARS["ai"]).markdown(res)  
        st.session_state.messages.append({"role":"ai","content":res})  
 
    if st.session_state.chart_data is not None:  
        st.markdown('<div class="h2" style="font-size:1.4rem;margin-top:26px">Latest chart</div>', unsafe_allow_html=True)
        chart_box = st.container(border=True)

        chart_data = st.session_state.chart_data  
        chart_type = st.session_state.chart_type  
        chart_color = st.session_state.chart_color

        # BAR CHART  
        if chart_type == "bar": 
            colors = None
            if chart_color:
                colors = [c.strip() for c in chart_color.split(",")]  

            fig = px.bar(  
                chart_data,  
                x=chart_data.columns[0],  
                y=chart_data.columns[1],  
                color=chart_data.columns[0],
                color_discrete_sequence=colors,  
                title="Data Analysis"  
            )  
            chart_box.plotly_chart(style_fig(fig), use_container_width=True)  

        # LINE CHART  
        elif chart_type == "line":  
            fig = px.line(  
                chart_data,  
                x=chart_data.columns[0],  
                y=chart_data.columns[1],  
                markers=True,  
                title="Data Trend"  
            )  
            if chart_color:
                colors = [c.strip() for c in chart_color.split(",")]
                fig.update_traces(marker_color=colors)
            chart_box.plotly_chart(style_fig(fig), use_container_width=True)  

        # SCATTER CHART  
        elif chart_type == "scatter":  
            fig = px.scatter(  
                chart_data,  
                x=chart_data.columns[0],  
                y=chart_data.columns[1],  
                title="Data Relationship"  
            )  
            if chart_color:
                colors = [c.strip() for c in chart_color.split(",")]
                fig.update_traces(marker_color=colors)
            chart_box.plotly_chart(style_fig(fig), use_container_width=True)  

        # PIE CHART  
        elif chart_type == "pie":  
            fig = px.pie(  
                chart_data,  
                names=chart_data.columns[0],  
                values=chart_data.columns[1],  
                title="Data Distribution"  
            )  
            if chart_color:
                colors = [c.strip() for c in chart_color.split(",")]
                fig.update_traces(marker_colors=colors)
            chart_box.plotly_chart(style_fig(fig), use_container_width=True)

st.markdown('<div class="foot">InsightIQ · Built with LangChain, Groq, pandas, Plotly and Streamlit</div>', unsafe_allow_html=True)