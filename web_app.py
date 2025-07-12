import streamlit as st
import asyncio
from llm_clients import MultiLLMQueryEngine

# --- Page Config ---
st.set_page_config(
    page_title="🤖 Multi-LLM Query Tool",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Helper function to run async code ---
def run_async(coro):
    """Run an async coroutine in a sync context."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

# --- App State ---
if 'query_result' not in st.session_state:
    st.session_state.query_result = None
if 'last_prompt' not in st.session_state:
    st.session_state.last_prompt = ""

# --- UI ---
st.title("🤖 Multi-LLM Query Tool")
st.markdown("Query multiple top-tier LLMs simultaneously, get their responses, and see a final merged answer evaluated by a judge LLM (GPT-4).")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Options")
    show_individual = st.toggle("Show Individual LLM Responses", value=True)
    st.markdown("---")
    st.info("This app uses various LLM APIs. An OpenAI API key is required for the 'judge' model.")

# --- Main Content ---
with st.form("query_form"):
    prompt = st.text_area("Enter your query:", height=150, key="prompt_input", placeholder="e.g., Explain quantum computing in simple terms")
    submitted = st.form_submit_button("🚀 Query Models")

if submitted and prompt:
    st.session_state.last_prompt = prompt
    with st.status("🧠 Processing query...", expanded=True) as status:
        try:
            st.write("Initializing query engine...")
            engine = MultiLLMQueryEngine()
            
            st.write(f"Querying {len(engine.enabled_llms)} LLMs...")
            result = run_async(engine.process_query(prompt))
            st.session_state.query_result = result
            
            status.update(label="✅ Query complete!", state="complete", expanded=False)
        except Exception as e:
            st.session_state.query_result = None
            status.update(label=f"❌ Error: {e}", state="error")


if st.session_state.query_result:
    result = st.session_state.query_result
    
    st.divider()
    
    # --- Display Results ---
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🎯 Final Merged Response")
        st.markdown(result["final_response"])

    with col2:
        st.subheader("📊 Query Summary")
        st.info(f"**Judge LLM:** `{result['judge_llm']}`")
        
        llms_used = ", ".join(f"`{name}`" for name in result['llms_used'])
        st.markdown(f"**LLMs Queried:** {llms_used}")
        
        successful_responses = sum(1 for _, (resp, err) in result["individual_responses"].items() if not err)
        st.success(f"**Successful Responses:** {successful_responses}/{len(result['individual_responses'])}")

    if show_individual:
        st.divider()
        st.subheader("📋 Individual LLM Responses")
        
        sorted_responses = sorted(result["individual_responses"].items())
        
        for name, (response, error) in sorted_responses:
            with st.expander(f"🤖 {name}", expanded=False):
                if error:
                    st.error(f"**Error:** {error}")
                else:
                    st.markdown(response)

# Add an example
st.divider()
if st.button("Try an Example Query"):
    example_prompt = "What are the main differences between Python and JavaScript for web development?"
    st.session_state.last_prompt = example_prompt
    
    with st.status("🧠 Processing example query...", expanded=True) as status:
        try:
            st.write("Initializing query engine...")
            engine = MultiLLMQueryEngine()
            
            st.write(f"Querying {len(engine.enabled_llms)} LLMs...")
            result = run_async(engine.process_query(example_prompt))
            st.session_state.query_result = result
            
            status.update(label="✅ Query complete!", state="complete", expanded=False)
        except Exception as e:
            st.session_state.query_result = None
            status.update(label=f"❌ Error: {e}", state="error")
    # Trigger a rerun to display the results
    st.rerun() 