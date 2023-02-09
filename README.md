<h1 align="center"> 📖 InsideGPT 📖</h1>

Get quick and accurate answers for your documents with instant citations. This project uses Streamlit for its frontend, OpenAI for its language model, and other libraries for various other functionalities.

🔧 Features
-----------

-   Ask questions about your documents 📁 and receive answers with references.
-   The answers come with citations 📚 and relevant text excerpts.

💻 Running Locally
------------------

1.  Clone the repository 📂


- ` git clone  https://github.com/RemiPelloux/InsideGPT.git`
- `cd InsideGPT`

2.  Install dependencies using [Poetry](https://python-poetry.org/) and activate the virtual environment 🔨 


-  `poetry install`
-  `poetry shell`

3.  Install required packages using pip



- `pip install streamlit`
- `pip install openai`
- `pip install tenacity`
- `pip install pydantic`
- `pip install langchain`
- `pip install faiss-cpu`
- `pip install embeddings`
- `pip install docx2txt`
- `pip install pypdf2`

4.  Launch the Streamlit server 🚀


- `cd InsideGPT`
- `streamlit run main.py`