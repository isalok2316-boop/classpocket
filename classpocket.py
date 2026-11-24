import streamlit as st

st.set_page_config(page_title="ClassPocket", page_icon="🎒", layout="centered")

st.title("🎒 ClassPocket")
st.write("A tua aplicação para gerir aulas, testes e trabalhos de forma muito fácil.")

# Carregamento seguro dos dados de tarefas/aulas
# (Garante que se os itens estiverem vazios ou mal formatados, não dá erro)
try:
    if "items" not in st.session_state:
        st.session_state["items"] = []
    items = st.session_state["items"]
except Exception:
    items = []

# Tratamento seguro para extrair as categorias e nomes das aulas
CATEGORIES = ["Homework", "Test", "Worksheet", "Project"]

# Extração segura de class_names convertendo sempre para string
class_names = sorted(set(str(x.get("class_name", "")) for x in items if isinstance(x, dict) and x.get("class_name")))
classes_filter = ["All classes"] + class_names

chosen_class = st.sidebar.selectbox("Filter by class", classes_filter)
chosen_category = st.sidebar.selectbox("Filter by Type", ["All"] + CATEGORIES)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ Quick overview")
st.sidebar.metric("Total tasks", len(items))

# Contagem segura de tarefas completadas
completed_count = sum(1 for x in items if isinstance(x, dict) and x.get("done", False))
st.sidebar.metric("Not completed", len(items) - completed_count)

with st.expander("➕ Add a class / task"):
    with st.form("class_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            class_name = st.text_input("Class / Subject", placeholder="e.g. Biology")
        with col2:
            title = st.text_input("Title", placeholder="e.g. Chapter 4 worksheet")
            
        col3, col4 = st.columns(2)
        with col3:
            category = st.selectbox("Type", CATEGORIES)
        with col4:
            due_date = st.date_input("Due date")
            
        submitted = st.form_submit_button("Add Task")
        if submitted and class_name and title:
            items.append({
                "class_name": class_name,
                "title": title,
                "category": category,
                "due_date": str(due_date),
                "done": False
            })
            st.success("Task added successfully!")