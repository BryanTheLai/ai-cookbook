import streamlit as st
import pandas as pd
import time
import os # Needed for potential file path joining later

# --- Configuration ---
PAGE_TITLE = "10K Insights Assistant"
PAGE_ICON = "📊"

# --- Placeholder Backend Functions ---
# (Replace these with your actual logic)

def load_available_context_options():
    """Loads available tickers and filing periods from the knowledge base."""
    # In reality: Query your metadata store (DB, file index, etc.)
    print("Backend Call: load_available_context_options()")
    # Dummy data
    tickers = ["AAPL", "GOOGL", "MSFT"]
    filings = ["2023 Q4", "2022 Q4", "2021 Q4"]
    return tickers, filings

def process_pdf_upload(uploaded_file, ticker, year, quarter, progress_callback):
    """Extracts text, converts to Markdown, and prepares for KB insertion."""
    # In reality: Use PyPDF2, PyMuPDF, etc. for text extraction
    #            Convert text to Markdown
    #            Save Markdown temporarily or return it
    print(f"Backend Call: process_pdf_upload({uploaded_file.name}, {ticker}, {year}, {quarter})")
    markdown_content = f"# {ticker} - {year} Q{quarter} (Simulated Extraction)\n\n"
    markdown_content += f"This is simulated Markdown content extracted from '{uploaded_file.name}'.\n\n"
    markdown_content += "## Section 1: Business Overview\nLorem ipsum dolor sit amet...\n\n"
    markdown_content += "## Section 2: Risk Factors\nConsectetur adipiscing elit...\n\n"

    # Simulate processing time and progress
    total_steps = 5
    for i in range(total_steps):
        time.sleep(0.5) # Simulate work
        progress = (i + 1) / total_steps
        progress_callback(progress) # Update the progress bar in UI

    # Simulate success/failure
    success = True # Change to False to test error handling
    if success:
        # In reality: you might save the markdown to a specific path here
        # For now, we just return the content
        return True, markdown_content, "extracted_markdown.md" # success_flag, content, saved_filename (optional)
    else:
        return False, None, None

def add_markdown_to_knowledge_base(markdown_content, ticker, year, quarter, filename):
    """Chunks, embeds, and stores the document in the vector DB and metadata store."""
    # In reality: Chunk the markdown, generate embeddings, store in vector DB
    #            Update your metadata store (DB, file index)
    print(f"Backend Call: add_markdown_to_knowledge_base({ticker}, {year}, {quarter}, {filename})")
    time.sleep(1) # Simulate work
    return True # Indicate success/failure

def get_rag_response(query, selected_tickers, selected_filings, chat_history):
    """Performs RAG: retrieves context and generates response using LLM."""
    # In reality: Embed query, search vector DB based on filters, build prompt, call LLM
    print(f"Backend Call: get_rag_response(query='{query}', tickers={selected_tickers}, filings={selected_filings})")
    time.sleep(1.5) # Simulate LLM call
    # Dummy response
    response_text = f"Based on the selected filings for {', '.join(selected_tickers)}, here's an analysis regarding '{query}':\n\n"
    response_text += "- Insight 1 derived from context.\n- Insight 2 comparing data points.\n- Overall sentiment appears neutral to positive."
    sources = [
        {"source": f"{ticker}-{filing.replace(' ', '')}.md", "content": "Relevant chunk 1 snippet..."}
        for ticker in selected_tickers[:1] for filing in selected_filings[:1]
    ]
    sources.append({"source": "AnotherDoc-2022Q4.md", "content": "Relevant chunk 2 snippet..."})
    return response_text, sources # response, list_of_source_chunks

def load_knowledge_base_data():
    """Loads metadata of documents currently in the knowledge base."""
    # In reality: Query your metadata store
    print("Backend Call: load_knowledge_base_data()")
    # Dummy data
    data = [
        {"id": 1, "Ticker": "AAPL", "Year": 2023, "Quarter": "Q4", "Filename": "aapl_2023q4_10k.pdf", "Import Date": "2024-01-15"},
        {"id": 2, "Ticker": "GOOGL", "Year": 2023, "Quarter": "Q4", "Filename": "googl_2023q4_10k.pdf", "Import Date": "2024-01-18"},
        {"id": 3, "Ticker": "MSFT", "Year": 2023, "Quarter": "Q4", "Filename": "msft_2023q4_10k.pdf", "Import Date": "2024-01-20"},
    ]
    return pd.DataFrame(data)

def get_document_details(doc_id):
    """Retrieves the Markdown content and original PDF path for a specific document."""
    # In reality: Query metadata store for paths, read Markdown file
    print(f"Backend Call: get_document_details(doc_id={doc_id})")
    # Dummy data - replace with actual file loading
    kb_entry = st.session_state.knowledge_base_data[st.session_state.knowledge_base_data['id'] == doc_id].iloc[0]
    ticker = kb_entry['Ticker']
    year = kb_entry['Year']
    quarter = kb_entry['Quarter']
    filename = kb_entry['Filename'] # In reality, this might be a PDF path

    # Assume markdown is stored with a consistent naming convention or path is in metadata
    markdown_filename = f"{ticker}_{year}{quarter}_extracted.md" # Example name
    dummy_markdown = f"# {ticker} {year} {quarter} (Stored Markdown)\n\nThis is the full stored markdown content for document ID {doc_id} ({filename}).\n\n*More detailed content would be here.*"

    # Store or retrieve the PDF path - for the skeleton, we might just use the filename
    pdf_path = filename # In a real app, this would be the actual path to the stored PDF

    return dummy_markdown, pdf_path

def delete_document_from_kb(doc_id):
    """Deletes document chunks from vector DB and removes metadata."""
    # In reality: Delete from vector DB, delete from metadata store, maybe delete files
    print(f"Backend Call: delete_document_from_kb(doc_id={doc_id})")
    time.sleep(1) # Simulate work
    return True # Indicate success/failure

# --- Streamlit App Structure ---

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")
st.title(f"{PAGE_ICON} {PAGE_TITLE}")

# --- Initialize Session State ---
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'available_tickers' not in st.session_state:
    st.session_state.available_tickers = []
if 'available_filings' not in st.session_state:
    st.session_state.available_filings = []
if 'selected_chat_tickers' not in st.session_state:
    st.session_state.selected_chat_tickers = []
if 'selected_chat_filings' not in st.session_state:
    st.session_state.selected_chat_filings = []
if 'knowledge_base_data' not in st.session_state:
    st.session_state.knowledge_base_data = pd.DataFrame() # Initialize as empty DataFrame
if 'import_file_processed' not in st.session_state:
    st.session_state.import_file_processed = False
if 'extracted_markdown' not in st.session_state:
    st.session_state.extracted_markdown = None
if 'extracted_filename' not in st.session_state: # Store the original uploaded filename
    st.session_state.extracted_filename = None
if 'import_metadata' not in st.session_state:
    st.session_state.import_metadata = {}
if 'selected_doc_id_manage' not in st.session_state:
    st.session_state.selected_doc_id_manage = None
if 'view_markdown' not in st.session_state:
    st.session_state.view_markdown = None
if 'view_pdf_path' not in st.session_state:
    st.session_state.view_pdf_path = None

# --- Load initial data ---
# Using a flag to load only once per session or when needed
if not st.session_state.available_tickers or not st.session_state.available_filings:
    st.session_state.available_tickers, st.session_state.available_filings = load_available_context_options()

if st.session_state.knowledge_base_data.empty:
     st.session_state.knowledge_base_data = load_knowledge_base_data()

# --- Define Tabs ---
tab_chat, tab_import, tab_manage = st.tabs(["💬 10K Chat", "📥 Import Filings", "📚 Manage Knowledge Base"])

# --- Tab 1: 10K Chat ---
with tab_chat:
    st.header("Ask Analytical Questions")

    col1, col2 = st.columns([1, 3]) # Sidebar-like layout within the tab

    with col1:
        st.subheader("Context Selection")
        st.session_state.selected_chat_tickers = st.multiselect(
            "Select Tickers to Query:",
            options=st.session_state.available_tickers,
            default=st.session_state.selected_chat_tickers # Maintain selection across reruns
        )
        st.session_state.selected_chat_filings = st.multiselect(
            "Select Filing Periods:",
            options=st.session_state.available_filings,
            default=st.session_state.selected_chat_filings # Maintain selection
        )
        st.button("Update Chat Context", key="update_context") # Button might trigger specific backend logic if needed
        st.caption(f"Context: {len(st.session_state.selected_chat_tickers)} tickers, {len(st.session_state.selected_chat_filings)} periods selected.")

        with st.expander("Quick Analysis Options:", expanded=False):
            if st.button("Summarize MD&A Section", key="quick_mdna"):
                st.session_state.predefined_query = "Summarize the Management Discussion and Analysis section."
            if st.button("Identify Top Risk Factors", key="quick_risks"):
                 st.session_state.predefined_query = "Identify and list the top 3 risk factors mentioned."
            if st.button("Compare Key Metrics Y-o-Y", key="quick_compare"):
                 st.session_state.predefined_query = "Compare key financial metrics year-over-year based on the latest two filings."
            # Add more buttons as needed

    with col2:
        st.subheader("Chat Interface")

        # Display chat messages from history
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "sources" in message and message["sources"]:
                    with st.expander("Show Sources Used"):
                        for source in message["sources"]:
                            st.caption(f"Source: {source.get('source', 'Unknown')}")
                            st.markdown(f"```\n{source.get('content', 'N/A')}\n```")

        # Handle predefined query clicks
        query_to_run = None
        if 'predefined_query' in st.session_state and st.session_state.predefined_query:
            query_to_run = st.session_state.predefined_query
            st.session_state.predefined_query = None # Clear after use

        # Get user input (prioritize predefined query if set)
        if prompt := query_to_run or st.chat_input("Ask about revenue trends, risks, comparisons..."):
            if not st.session_state.selected_chat_tickers or not st.session_state.selected_chat_filings:
                 st.warning("Please select at least one ticker and filing period for context.")
            else:
                # Add user message to chat history
                st.session_state.chat_messages.append({"role": "user", "content": prompt})
                # Display user message
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Display assistant response with spinner
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response_text = ""
                    sources = []
                    with st.spinner("Thinking..."):
                        # Call RAG backend
                        full_response_text, sources = get_rag_response(
                            prompt,
                            st.session_state.selected_chat_tickers,
                            st.session_state.selected_chat_filings,
                            st.session_state.chat_messages # Pass history if needed by backend
                        )
                        message_placeholder.markdown(full_response_text + "▌") # Simulate typing
                    message_placeholder.markdown(full_response_text) # Final response

                    # Display sources if available
                    if sources:
                        with st.expander("Show Sources Used"):
                             for source in sources:
                                st.caption(f"Source: {source.get('source', 'Unknown')}")
                                st.markdown(f"```\n{source.get('content', 'N/A')}\n```")

                # Add assistant response to chat history
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": full_response_text,
                    "sources": sources
                })

# --- Tab 2: Import Filings ---
with tab_import:
    st.header("Import New 10-K Filing")

    uploaded_file = st.file_uploader("1. Upload 10-K Filing (PDF):", type="pdf", key="file_uploader")

    col_meta1, col_meta2, col_meta3 = st.columns(3)
    with col_meta1:
        ticker_input = st.text_input("2. Ticker Symbol:", key="import_ticker").upper()
    with col_meta2:
        year_input = st.number_input("3. Filing Year:", min_value=2000, max_value=2030, step=1, key="import_year")
    with col_meta3:
        # 10-Ks are typically annual (Q4 represents the full year)
        quarter_input = st.selectbox("4. Filing Quarter (Nominal):", ["Q4"], index=0, key="import_quarter", help="10-Ks cover the full fiscal year, typically represented as Q4.")

    if st.button("Start Import & Extraction", key="import_start"):
        if uploaded_file is not None and ticker_input and year_input and quarter_input:
            st.session_state.import_file_processed = False # Reset flag
            st.session_state.extracted_markdown = None
            st.session_state.extracted_filename = None
            st.session_state.import_metadata = {
                "ticker": ticker_input,
                "year": year_input,
                "quarter": quarter_input,
                "original_filename": uploaded_file.name
            }

            status_placeholder = st.empty()
            progress_bar = st.progress(0, text="Starting extraction...")

            def progress_callback(progress_value):
                progress_bar.progress(progress_value, text=f"Extracting... {int(progress_value*100)}%")

            with st.spinner("Processing PDF... Please wait."):
                 success, md_content, saved_md_filename = process_pdf_upload(
                     uploaded_file, ticker_input, year_input, quarter_input, progress_callback
                 )

            if success:
                status_placeholder.success(f"✅ Extraction Successful for {uploaded_file.name}!")
                st.session_state.extracted_markdown = md_content
                st.session_state.extracted_filename = saved_md_filename # Store the name if backend saved it
                st.session_state.import_file_processed = True
            else:
                status_placeholder.error(f"❌ Extraction Failed for {uploaded_file.name}. Please check the file or logs.")
                st.session_state.import_file_processed = False
                st.session_state.extracted_markdown = None # Clear any potential partial data

        else:
            st.warning("Please upload a PDF and fill in all metadata fields.")

    if st.session_state.import_file_processed and st.session_state.extracted_markdown:
        st.subheader("Extracted Markdown Preview:")
        st.markdown("---") # Visual separator
        st.text_area("Preview:", value=st.session_state.extracted_markdown, height=400, key="markdown_preview_area", disabled=True)
        st.markdown("---") # Visual separator

        if st.button("Confirm & Add to Knowledge Base ✅", key="confirm_add_kb"):
            with st.spinner("Adding to Knowledge Base..."):
                add_success = add_markdown_to_knowledge_base(
                    st.session_state.extracted_markdown,
                    st.session_state.import_metadata['ticker'],
                    st.session_state.import_metadata['year'],
                    st.session_state.import_metadata['quarter'],
                    st.session_state.import_metadata['original_filename'] # Pass original PDF name or the saved MD name
                )
            if add_success:
                st.success("Document successfully added to Knowledge Base!")
                # Clear state related to the import
                st.session_state.import_file_processed = False
                st.session_state.extracted_markdown = None
                st.session_state.extracted_filename = None
                st.session_state.import_metadata = {}
                # Reload KB data for the management tab
                st.session_state.knowledge_base_data = load_knowledge_base_data()
                # Optionally clear the file uploader state (more complex, might need experimental_rerun)
                # st.experimental_rerun() # Force rerun to clear widgets if needed
            else:
                st.error("Failed to add document to Knowledge Base. Please check logs.")


# --- Tab 3: Manage Knowledge Base ---
with tab_manage:
    st.header("Manage Ingested Filings")

    if st.button("Refresh List 🔄", key="refresh_kb"):
        st.session_state.knowledge_base_data = load_knowledge_base_data()
        st.session_state.selected_doc_id_manage = None # Reset selection
        st.session_state.view_markdown = None
        st.session_state.view_pdf_path = None
        st.success("Knowledge Base list refreshed.")

    st.subheader("Current Documents")
    if not st.session_state.knowledge_base_data.empty:
        # Display the dataframe - consider using data_editor for potential future inline editing
        st.dataframe(
            st.session_state.knowledge_base_data,
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("View / Delete Document")
        # Create identifier strings for selection
        doc_options = {
            f"{row['Ticker']} - {row['Year']} {row['Quarter']} (ID: {row['id']})": row['id']
            for index, row in st.session_state.knowledge_base_data.iterrows()
        }
        selected_doc_str = st.selectbox(
            "Select Document:",
            options=doc_options.keys(),
            index=None, # Default to no selection
            placeholder="Choose a document...",
            key="manage_doc_select"
        )

        if selected_doc_str:
            st.session_state.selected_doc_id_manage = doc_options[selected_doc_str]

            col_view, col_delete = st.columns(2)
            with col_view:
                 if st.button("View Document Details 🔎", key="view_doc_details"):
                    st.session_state.view_markdown = None # Clear previous view
                    st.session_state.view_pdf_path = None
                    with st.spinner(f"Loading details for Document ID {st.session_state.selected_doc_id_manage}..."):
                        markdown_content, pdf_path = get_document_details(st.session_state.selected_doc_id_manage)
                        st.session_state.view_markdown = markdown_content
                        st.session_state.view_pdf_path = pdf_path # Store the path

            with col_delete:
                st.button("Delete Document 🗑️", key="delete_doc_prompt", type="primary")


            # Conditional display for Delete Confirmation
            # Using a separate session state flag triggered by the delete button
            if st.session_state.get("delete_doc_prompt"):
                 st.warning(f"**Confirm Deletion:** Are you sure you want to delete Document ID {st.session_state.selected_doc_id_manage} ({selected_doc_str})? This action cannot be undone.")
                 confirm_col1, confirm_col2 = st.columns(2)
                 with confirm_col1:
                    if st.button("Yes, Delete Permanently", key="delete_doc_confirm", type="primary"):
                         with st.spinner(f"Deleting Document ID {st.session_state.selected_doc_id_manage}..."):
                            delete_success = delete_document_from_kb(st.session_state.selected_doc_id_manage)
                         if delete_success:
                            st.success(f"Document ID {st.session_state.selected_doc_id_manage} deleted successfully.")
                            # Reset state and reload data
                            st.session_state.knowledge_base_data = load_knowledge_base_data()
                            st.session_state.selected_doc_id_manage = None
                            st.session_state.view_markdown = None
                            st.session_state.view_pdf_path = None
                            st.session_state.delete_doc_prompt = False # Reset confirmation flag
                            st.rerun() # Rerun to reflect changes immediately
                         else:
                            st.error("Failed to delete document. Please check logs.")
                 with confirm_col2:
                    if st.button("Cancel", key="delete_doc_cancel"):
                        st.session_state.delete_doc_prompt = False # Reset confirmation flag
                        st.rerun() # Rerun to hide confirmation


            # Conditional display for Document Viewer
            if st.session_state.view_markdown:
                st.markdown("---")
                st.subheader(f"Viewing: {selected_doc_str}")
                view_tab_md, view_tab_pdf = st.tabs(["📄 Extracted Markdown", "📊 Original PDF (Placeholder)"])

                with view_tab_md:
                    st.markdown(st.session_state.view_markdown)

                with view_tab_pdf:
                    st.info("PDF Viewer Placeholder")
                    st.write(f"Path to original PDF: `{st.session_state.view_pdf_path}`")
                    st.write("*(Requires integrating a PDF viewing component like `streamlit-pdf-viewer` or embedding)*")
                    # Example (requires installation and handling potential errors):
                    # try:
                    #     # Assuming view_pdf_path is a valid path to the PDF
                    #     if st.session_state.view_pdf_path and os.path.exists(st.session_state.view_pdf_path):
                    #          with open(st.session_state.view_pdf_path,"rb") as f:
                    #              base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    #          pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
                    #          st.markdown(pdf_display, unsafe_allow_html=True)
                    #     else:
                    #          st.warning("PDF file not found at the specified path.")
                    # except Exception as e:
                    #     st.error(f"Error displaying PDF: {e}")


        else:
            # Clear viewer if no document is selected
            st.session_state.view_markdown = None
            st.session_state.view_pdf_path = None
            st.session_state.delete_doc_prompt = False # Ensure confirmation is hidden

    else:
        st.info("Knowledge Base is currently empty. Import documents using the 'Import Filings' tab.")

# --- Footer or Sidebar Info ---
st.sidebar.markdown("---")
st.sidebar.info("Built with Streamlit for FYP.")