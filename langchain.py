from langchain.llms import OpenAI
from langchain import ConversationChain
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

# langchain.py

def process_cases(cases):
    # Initialize LLM and ConversationChain
    llm = OpenAI(temperature=0)
    conversation = ConversationChain(llm=llm, verbose=True)

    # Load cases into documents
    documents = [TextLoader.from_text(case['title'] + " " + case['snippet']) for case in cases]

    # Split text into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # Index documents for similarity search
    db = FAISS.from_documents(docs)

    # Find relevant cases based on similarity to the query
    query = conversation.latest_input
    docs = db.similarity_search(query)

    # Extract relevant cases and their relevance scores
    relevant_cases = []
    for doc in docs:
        index = doc['index']
        relevant_cases.append({
            'title': cases[index]['title'],
            'snippet': cases[index]['snippet'],
            'relevance_score': doc['similarity']
        })

    relevant_cases.sort(key=lambda x: x['relevance_score'], reverse=True)
    return relevant_cases
