import streamlit as st
import asyncio
from llm_clients import MultiLLMQueryEngine

st.title("Multi-LLM Query Tool Web")

prompt = st.text_area("Enter your query:")
show_individual = st.checkbox("Show individual responses")

if st.button("Query LLMs"):
    if prompt:
        with st.spinner("Processing..."):
            engine = MultiLLMQueryEngine()
            result = asyncio.run(engine.process_query(prompt))
            
            if show_individual:
                st.subheader("Individual Responses")
                for name, (resp, err) in result["individual_responses"].items():
                    if err:
                        st.error(f"{name}: {err}")
                    else:
                        st.success(f"{name}: {resp}")
            
            st.subheader("Final Merged Response")
            st.write(result["final_response"])
    else:
        st.warning("Please enter a query.") 