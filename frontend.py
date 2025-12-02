import streamlit as st
import requests

Backend_URL = "http://localhost:1234"


def main():
    st.title("Personal AI Journalist")

    #session state
    if 'topics' not in st.session_state:
        st.session_state.topics=[]



    #Sidebar
    with st.sidebar:
        st.header("Settings")
        source_type = st.selectbox("Data Sources", options = ["both", "news", "reddit"],
        format_func = lambda x: f"{x.capitalize()}" if x == "news" else f"{x.capitalize()}")

    #Topic management
    st.markdown("Topic Management")
    col1, col2 = st.columns([4,1])    
    with col1:
        new_topic = st.text_input("Enter a topic to analyze", 
        placeholder = "e.g. Artificial Intelligence")

    with col2:
        add_disabled = len(st.session_state.topics) >= 1 or not new_topic.strip()
        if st.button("Add", disabled=add_disabled):
            st.session_state.topics.append(new_topic.strip())
            st.rerun()   

    if st.session_state.topics:
        st.subheader("Selected Topic")
        for i, topic in enumerate(st.session_state.topics[:3]):
            cols = st.columns([4,1])
            cols[0].write(f"{i+1}.{topic}")
            if cols[1].button("Remove", key = f"remove_{i}"):
                del st.session_state.topics[i]
                st.rerun()  

    st.markdown("---")   
    st.subheader("Audio Generation")  
    
    if st.button("Generate Summary", disabled= len(st.session_state.topics) == 0):
        if not st.session_state.topics:
            st.error("Please add at least one topic")
        else:
            with st.spinner("Analyzing topic and generating audio..."):
                try:
                    response = requests.post(f"{Backend_URL}/generate-news-audio",
                    json={
                        "topics":st.session_state.topics,
                        "source_type": source_type
                    })
                    if response.static_code == 200:
                        st.audio(response.content, format= "audio/mpeg")
                        st.download_button(
                            "Download Audio summary",
                            data = response.content,
                            file_name = "news-summary.mp3",
                            type="primary"
                        )
                    else: 
                        handle_api_error(response)
                except requests.exceptions.ConnectionError:
                    st.error("Connection Error: Could not reach the backend server")  
                except Exception as e:
                    st.error(f"Unexpected error: {str(e)}")           
                


def handle_api_error(response):
    """ Handle api error responses"""
    try: 
        error_detail = response.json().get("detail", "Unknown error")
        st.error(f"API error({response.status_code}):{error_detail}")
    except ValueError:
        st.error(f"Unexpected API response: {response.text}")    
if __name__=='__main__':
    main()    