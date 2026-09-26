# InsightIQ --- AI Data Analyst

An **agentic AI-powered data analysis application** that allows users to interact with CSV datasets using natural language.

Instead of manually writing Pandas operations or SQL queries, users can ask questions such as:

* `What are the columns in this dataset?`
* `Show me the average salary.`
* `Filter employees whose salary is greater than 50000.`
* `Show the distribution of gender.`
* `Create a bar chart of employees by department.`
* `Show me the relationship between age and salary.`

The application uses an LLM as an **agentic reasoning layer** that selects appropriate analytical tools, while the actual data processing is performed using **Pandas** and visualizations are generated using **Plotly**.

---

## 🚀 Key Features

* 📂 Upload CSV datasets through a Streamlit interface
* 💬 Analyze datasets using natural-language queries
* 🤖 LLM-powered tool selection and orchestration
* 🐼 Pandas-based data processing and analysis
* 🔎 Data filtering using natural-language instructions
* 📊 Interactive Plotly visualizations
* 🎨 Natural-language chart color customization
* 🧠 Conversational interaction using agent memory
* ⚡ Groq-powered LLM inference
* 🖥️ Simple browser-based interface using Streamlit

---

## 🏗️ Application Architecture

The application follows an **LLM + tools architecture** rather than simply sending the user's question to an LLM and displaying its response.

```text
                    ┌─────────────────────┐
                    │       User          │
                    │ Natural Language    │
                    │       Query         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Streamlit UI    │
                    │      (app.py)       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     LLM Agent       │
                    │      Groq LLM       │
                    └──────────┬──────────┘
                               │
                  Selects appropriate tool
                               │
              ┌────────────────┼─────────────────┐
              │                │                 │
              ▼                ▼                 ▼
       ┌────────────┐   ┌────────────┐   ┌──────────────┐
       │ Data Info  │   │  Filter    │   │ Data Analysis│
       │   Tool     │   │   Tool     │   │     Tool     │
       └────────────┘   └────────────┘   └──────────────┘
              │                │                 │
              └────────────────┼─────────────────┘
                               │
                               ▼
                         ┌───────────┐
                         │  Pandas   │
                         │ DataFrame │
                         └─────┬─────┘
                               │
                               ▼
                       ┌────────────────┐
                       │ Chart Tool     │
                       │    Plotly      │
                       └───────┬────────┘
                               │
                               ▼
                       ┌────────────────┐
                       │ Interactive    │
                       │ Visualization  │
                       └────────────────┘
```

---

## 🧠 How It Works

### 1. Dataset Upload

The user uploads a CSV file through the Streamlit interface.

The dataset is loaded into a Pandas `DataFrame` and becomes available to the analytical tools.

```python
df = pd.read_csv(uploaded_file)
```

The application maintains the currently uploaded dataset so that subsequent natural-language queries can operate on it.

---

### 2. Natural-Language Query

The user interacts with the application through a chat interface.

For example:

```text
Show me the average salary by department.
```

The query is passed to the agent rather than directly to the model as a simple question-answer request.

---

### 3. Agentic Tool Selection

The LLM is provided with a set of custom tools.

Depending on the user's request, the agent determines which tool should be used.

For example:

```text
"What columns are present?"
        ↓
get_data_info()

"Show employees with salary > 50000"
        ↓
filter_tool()

"What is the average salary?"
        ↓
analyze_data()

"Create a bar chart of salary by department"
        ↓
create_chart()
```

This allows the LLM to act as an orchestration layer while deterministic Python code performs the actual data operations.

---

## 🛠️ Available Tools

### `get_data_info`

Provides basic information about the currently loaded dataset.

It can return information such as:

* Number of rows
* Number of columns
* Column names
* Data types
* Sample records

---

### `filter_tool`

Filters the Pandas DataFrame based on a generated condition.

Example:

```text
Show employees whose salary is greater than 50000.
```

The agent can translate this into a Pandas query condition and execute the filtering operation.

---

### `analyze_data`

Performs analytical operations on the dataset using Pandas.

Examples include:

```python
df["salary"].mean()
df["age"].max()
df["department"].value_counts()
df.groupby("department")["salary"].mean()
```

The tool returns the analytical result to the agent so that it can formulate a natural-language response.

---

### `create_chart`

Creates visualizations from analytical results.

Supported chart types include:

* Bar charts
* Line charts
* Scatter plots
* Pie charts

The agent determines the appropriate visualization based on the user's request.

For example:

```text
Show the number of employees in each department as a bar chart.
```

The agent can call:

```text
create_chart(...)
```

The resulting data is then rendered using Plotly in the Streamlit interface.

The tool also supports user-requested colors.

Example:

```text
Create a bar chart using green and orange.
```

---

## 📊 Visualization Flow

The visualization pipeline is separated from the LLM response generation.

```text
User Request
     ↓
LLM Agent
     ↓
create_chart()
     ↓
Pandas Analysis
     ↓
Chart Data
     ↓
Plotly
     ↓
Streamlit
```

This means the LLM does not directly draw the chart.

Instead, it determines **what visualization should be created**, while Python and Plotly handle the actual visualization.

---

## 💻 Technology Stack

| Technology     | Purpose                         |
| -------------- | ------------------------------- |
| Python         | Core application logic          |
| Streamlit      | Web interface                   |
| Pandas         | Data loading and analysis       |
| Plotly Express | Interactive visualizations      |
| LangChain      | Agent and tool orchestration    |
| LangGraph      | Agent state/checkpointing       |
| Groq           | LLM inference                   |
| python-dotenv  | Environment variable management |

---

## 📁 Project Structure

```text
AI-Data-Analyst/
│
├── app.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

### `app.py`

The main application file.

It contains:

* Streamlit UI
* CSV upload handling
* Pandas DataFrame management
* Custom analytical tools
* LLM configuration
* Agent configuration
* Conversation handling
* Chart state management
* Plotly visualization rendering

The current implementation keeps the application intentionally compact rather than splitting a relatively small project into unnecessary modules.

---

### `requirements.txt`

Contains the Python dependencies required to run the application.

Example:

```text
langchain
langchain-groq
langgraph
pandas
plotly
python-dotenv
streamlit
```

Installing the dependencies:

```bash
pip install -r requirements.txt
```

---

### `.gitignore`

Prevents unnecessary or sensitive files from being committed to Git.

Typical entries include:

```text
.env
.venv/
env/
__pycache__/
*.pyc
```

The `.env` file is particularly important because it contains environment variables such as API credentials.

---

### `LICENSE`

Defines how the project's source code can be used, modified, and distributed.

This repository uses the license included in the `LICENSE` file.

---

### `README.md`

Project documentation containing:

* Project overview
* Architecture
* Features
* Technology stack
* Application workflow
* Setup instructions
* Project structure
* Usage examples
* Limitations

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/shirshanag/InsightIQ
cd AI-Data-Analyst
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_api_key_here
```

Do **not** commit the `.env` file to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 💬 Example Queries

After uploading a CSV file, try queries such as:

```text
What information is present in this dataset?
```

```text
What is the average value of the salary column?
```

```text
Show me the top 10 records.
```

```text
Filter the data where age is greater than 30.
```

```text
What is the distribution of gender?
```

```text
Create a bar chart showing employees by department.
```

```text
Create a scatter plot showing the relationship between age and salary.
```

```text
Create a line chart showing the monthly sales trend.
```

```text
Create a bar chart using green, orange and white.
```

---

## 🔐 Data & Security Considerations

The application performs structured data processing using Pandas within the application layer, while the LLM is primarily used for natural-language understanding and tool selection.

However, using an external LLM API does **not automatically guarantee data privacy or security**.

When deploying this application with sensitive datasets, additional measures should be considered, including:

* Data minimization
* Input validation
* Authentication and authorization
* Encryption
* Controlled execution of generated expressions
* Secure API-key management
* Model-provider data-retention policies

The current project is intended as an engineering prototype and should not be considered a secure production analytics platform without additional hardening.

---

## ⚠️ Current Limitations

This project intentionally keeps the implementation relatively simple.

Some areas that would require additional work for production deployment include:

* Safer execution instead of unrestricted `eval()`
* Stronger input validation
* Per-user dataset/session isolation
* More robust exception handling
* Automated tests
* Logging and observability
* Authentication and authorization
* Production-grade state management
* Larger dataset optimization

These are natural areas for future development rather than requirements for the current prototype.

---

## 🔮 Possible Future Improvements

Potential future additions include:

* Support for Excel files
* More advanced statistical analysis
* Missing-value analysis
* Correlation analysis
* Automated data profiling
* Database connectivity
* Authentication
* Persistent conversation history
* Safer analytical expression execution
* MLOps/observability integration

The current implementation deliberately focuses on the core **agent → tools → Pandas → visualization** workflow.

---

## 🎯 Project Objective

The goal of this project is not to build a general-purpose replacement for ChatGPT or Claude.

Instead, it demonstrates how an LLM can be integrated into a **specialized AI application** where the model acts as an orchestration layer over controlled analytical tools.

The core idea is:

```text
Natural Language
       ↓
     LLM
       ↓
 Tool Selection
       ↓
Python / Pandas
       ↓
Analysis / Visualization
       ↓
    Result
```

This architecture demonstrates practical concepts in:

* Agentic AI
* Tool calling
* LLM application development
* Structured data analysis
* State management
* Data visualization
* AI application architecture

---

## 📌 Disclaimer

This project is intended for educational, experimental, and portfolio purposes.

Do not upload confidential, sensitive, or personally identifiable datasets unless the application has been appropriately secured and the applicable model-provider data policies have been reviewed.

---

## 📄 License

This project is distributed under the license included in the `LICENSE` file.
