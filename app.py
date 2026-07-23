import streamlit as st
import time

from pipeline import run_repo_analyzer


st.set_page_config(
    page_title="GitHub AI Repository Analyzer",
    page_icon="🤖",
    layout="wide",
)


st.markdown(
    """
<style>

body {
    background-color: #0b0f19;
}


.stApp {
    background:
    radial-gradient(circle at top left,#1f2937,#020617);
    color:white;
}


.main-title {
    font-size:45px;
    font-weight:900;
    background: linear-gradient(
        90deg,
        #00f5ff,
        #8b5cf6,
        #ec4899
    );
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}


.subtitle {
    font-size:18px;
    color:#cbd5e1;
}


.card {

    background:
    rgba(255,255,255,0.05);

    border-radius:20px;

    padding:25px;

    border:
    1px solid rgba(255,255,255,0.1);

    backdrop-filter:
    blur(15px);

    margin-bottom:20px;

}


.stButton button {

    width:100%;

    border-radius:15px;

    height:50px;

    font-size:18px;

    font-weight:700;

    background:
    linear-gradient(
        90deg,
        #06b6d4,
        #8b5cf6
    );

    color:white;

    border:none;

}


.stTextInput input {

    background:#111827;

    color:white;

    border-radius:12px;

}


</style>

""",
    unsafe_allow_html=True,
)



st.markdown(
    """
<div class="main-title">
🤖 GitHub AI Repository Analyzer
</div>

<div class="subtitle">
Agentic AI + RAG + LangChain powered repository intelligence system.
</div>

<br>
""",
    unsafe_allow_html=True,
)



with st.container():

    st.markdown(
        """
        <div class="card">
        🚀 Enter any public GitHub repository URL.
        The AI will:
        
        <br><br>

        • Clone repository  
        • Build RAG knowledge base  
        • Search documentation  
        • Analyze architecture  
        • Review with critic agent  
        • Generate markdown report  

        </div>
        """,
        unsafe_allow_html=True,
    )



repo_url = st.text_input(
    "🔗 GitHub Repository URL",
    placeholder="https://github.com/user/project",
)



query = st.text_input(
    "💬 What do you want to analyze?",
    placeholder="Explain architecture, technologies and improvements",
)



analyze = st.button(
    "🚀 Analyze Repository"
)



if analyze:

    if not repo_url:

        st.error(
            "Please provide GitHub repository URL"
        )

    else:

        if not query:
            query = "Analyze this repository completely"



        progress = st.progress(0)

        status = st.empty()


        steps = [
            "🔎 Searching repository...",
            "📦 Loading repository files...",
            "🧠 Building RAG memory...",
            "🤖 Running AI agents...",
            "📝 Generating explanation...",
            "🧐 Running critic review...",
            "💾 Saving report..."
        ]


        for i,step in enumerate(steps):

            status.info(step)

            progress.progress(
                (i+1)/len(steps)
            )

            time.sleep(0.3)



        try:

            result = run_repo_analyzer(
                query=repo_url + "\n" + query,
                repo_path=repo_url,
            )


            status.success(
                "Analysis Completed Successfully 🎉"
            )


            st.divider()



            st.markdown(
                """
                ## 🧠 AI Final Analysis
                """
            )


            st.markdown(
                result.get(
                    "feedback",
                    "No result generated"
                )
            )



            with st.expander(
                "🔍 Search Agent Output"
            ):

                st.write(
                    result.get(
                        "search",
                        "No search output"
                    )
                )


            with st.expander(
                "📂 Repository Agent Output"
            ):

                st.write(
                    result.get(
                        "repository",
                        "No repository output"
                    )
                )



            with st.expander(
                "📄 Generated Report"
            ):

                st.write(
                    result.get(
                        "report",
                        "No report"
                    )
                )


        except Exception as e:

            st.error(
                f"""
                ❌ Error occurred:

                {e}
                """
            )



st.divider()


st.markdown(
    """
<div style="
text-align:center;
color:#94a3b8;
">

Built with ❤️ using:

LangChain • RAG • Agents • Mistral • Streamlit

</div>
""",
    unsafe_allow_html=True,
)







# analize it with provides the names of all .jsx file which are include in it