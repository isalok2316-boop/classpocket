import streamlit as st

st.set_page_config(page_title="ClassPocket", page_icon="🎒", layout="wide")

# Estilo visual moderno para a aplicação
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #fff3fa, #f2faff);}
.block-container {max-width: 1100px; padding-top: 2rem;}
h1, h2, h3 {color: #8952a8;}
div[data-testid="stMetric"] {background: #fff; padding: 14px; border-radius: 18px; border: 1px solid #f0e6f6;}
.stButton>button {border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

# Função simulada de carregamento de dados caso não exista
if "items" not in st.session_state:
    st.session_state.items = []

items = st.session_state.items

st.title("🎒 ClassPocket")
st.caption("Your classes, homework, tests and worksheets – all in one cozy place.")

# Tratamento seguro para evitar erros se os itens estiverem vazios ou mal formatados
CATEGORIES = ["Homework", "Test", "Worksheet", "Project"]
class_names = sorted(set([x.get("class_name", "") for x in items if isinstance(x, dict) and x.get("class_name")]))
classes_filter = ["All classes"] + class_names

chosen_class = st.sidebar.selectbox("Filter by class", classes_filter)
chosen_category = st.sidebar.selectbox("Filter by type", ["All"] + CATEGORIES)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick overview")
st.sidebar.metric("Total tasks", len(items))
st.sidebar.metric("Not completed", sum(1 for x in items if isinstance(x, dict) and not x.get("done", False)))

with st.expander("➕ Add a class task"):
    with st.form("add item", clear_on_submit=True):
        col1, col2 = st.columns(2)
        class_name = col1.text_input("Class / Subject", placeholder="e.g. Biology")
        title = col2.text_input("Title", placeholder="e.g. Chapter 4 worksheet")
        
        col3, col4 = st.columns(2)
        category = col3.selectbox("Type", CATEGORIES)
        due_date = col4.date_input("Due date")
        
        submitted = st.form_submit_button("Add Task")
        if submitted and class_name and title:
            st.session_state.items.append({
                "class_name": class_name,
                "title": title,
                "category": category,
                "due_date": str(due_date),
                "done": False
            })
            st.success("Task added successfully!")
            st.rerun()