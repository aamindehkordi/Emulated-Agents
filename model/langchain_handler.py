


def generate_response(query, agent_history, agent_prompt):
    # Add the code here, using the input parameters instead of hard-coded values
    loader = TextLoader('model/prompts/super_prompt.txt')
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    # Read the API key and environment from file lines 1 and 2
    """with open('./key_pinecone.txt') as f:
        api_key = f.readline().strip()
        environment = f.readline().strip()"""
    api_key = "3ad35bc4-f126-413d-8e1c-7b9c6344fab4"
    environment = "us-west4-gcp"
    # initialize pinecone
    pinecone.init(
        api_key=api_key,  # find at app.pinecone.io
        environment=environment  # next to api key in console
    )

    index_name = "ai-langchain"

    docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)
    docs = docsearch.similarity_search(query)

    relevant_doc = docs[0].page_content

    msg = [{'role':'system', 'content': f'{agent_prompt}'}, 
           *agent_history, 
           { "role": "user", "content": 
            f"""As Nathan, you are currently in a conversation with Kyle. 
            Maintain your persona and respond appropriately to his query [{query}]. 
            To assist you in the conversation, you may be provided with some information. 
            However, you should only use the information that is relevant to the current conversation and keep your response concise. 
            Do not use multiple lines of information from the document.
            Please see the following document for information:\n\n{relevant_doc}""" }]
    response = OpenAI.ChatCompletion.create(messages=msg, model="gpt-3.5-turbo", temperature=0.91, top_p=1, n=1, stream=False, stop= "null", max_tokens=350, presence_penalty=0, frequency_penalty=0)
    answer = response["choices"][0]["message"]["content"]
    return answer
