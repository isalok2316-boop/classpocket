import json
from pathlib import Path
from datetime import date
import streamlit as st

DATA_FILE = Path("classpocket_data.json")
CATEGORIES = ["Homework", "Test", "Worksheet", "Assignment"]

def load_data():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def save_data(items):
    DATA_FILE.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

st.set_page_config(page_title="ClassPocket ♡", page_icon="🎀", layout="wide")
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#fff3fa,#f2faff);}
.block-container {max-width: 1100px; padding-top: 2rem;}
h1,h2,h3 {color:#8952a8;}
div[data-testid="stMetric"] {background:#fff; padding:14px; border-radius:18px; border:1px solid #d9c7f3;}
div.stButton>button {border-radius:16px;}
</style>
""", unsafe_allow_html=True)

if "items" not in st.session_state:
    st.session_state.items = load_data()

items = st.session_state.items
st.title("🎀 ClassPocket")
st.caption("Your classes, homework, tests and worksheets — all in one cozy place.")

classes = sorted(set([x.get("class_name", "") for x in items if x.get("class_name")]))
classes = ["All classes"] + classes
chosen_class = st.sidebar.selectbox("📚 Filter by class", classes)
chosen_category = st.sidebar.selectbox("🗂️ Filter by type", ["All"] + CATEGORIES)
st.sidebar.markdown("---")
st.sidebar.markdown("### ✨ Quick overview")
st.sidebar.metric("Total tasks", len(items))
st.sidebar.metric("Not completed", sum(not x.get("done", False) for x in items))

with st.expander("➕ Add a class task", expanded=True):
    with st.form("add_item", clear_on_submit=True):
        col1, col2 = st.columns(2)
        class_name = col1.text_input("Class / subject", placeholder="e.g. Biology")
        title = col2.text_input("Title", placeholder="e.g. Chapter 4 worksheet")
        col3, col4 = st.columns(2)
        category = col3.selectbox("Type", CATEGORIES)
        due_date = col4.date_input("Due date", value=date.today())
        details = st.text_area("Notes / details", placeholder="What do you need to do?")
        submitted = st.form_submit_button("♡ Save to ClassPocket")
        if submitted:
            if class_name.strip() and title.strip():
                new_item = {
                    "id": str(len(items)) + "_" + str(date.today()),
                    "class_name": class_name.strip(),
                    "title": title.strip(),
                    "category": category,
                    "due": due_date.isoformat(),
                    "details": details.strip(),
                    "done": False,
                }
                items.append(new_item)
                save_data(items)
                st.success("Saved! ✨")
                st.rerun()
            else:
                st.warning("Please enter both a class name and a title.")

filtered = [
    x for x in items
    if (chosen_class == "All classes" or x.get("class_name") == chosen_class)
    and (chosen_category == "All" or x.get("category") == chosen_category)
]
filtered.sort(key=lambda x: x.get("due", "9999-12-31"))

st.markdown("## 🌷 Your planner")
if not filtered:
    st.info("Nothing here yet. Add a class task above to get started! ♡")
else:
    for item in filtered:
        with st.container(border=True):
            left, mid, right = st.columns([0.12, 0.68, 0.20])
            is_done = left.checkbox("Done", value=item.get("done", False), key=f"done_{item['id']}")
            if is_done != item.get("done", False):
                item["done"] = is_done
                save_data(items)
                st.rerun()
            mid.markdown(f"**{item.get('title','Untitled')}**  ·  {item.get('class_name','Class')}")
            mid.caption(f"{item.get('category','Task')}  |  Due: {item.get('due','No date')}")
            if item.get("details"):
                mid.write(item["details"])
            if item.get("done"):
                right.success("Completed ♡")
            else:
                right.warning("To do ✧")
            if right.button("🗑️ Delete", key=f"delete_{item['id']}"):
                st.session_state.items = [x for x in items if x["id"] != item["id"]]
                save_data(st.session_state.items)
                st.rerun()

st.markdown("---")
st.caption("ClassPocket prototype · Python + Streamlit · Data is saved locally in classpocket_data.json")
