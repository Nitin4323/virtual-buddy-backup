from utility import RAG

def execute_prompt(prompt, retries=3):
    """
    Main method to send prompt to AI engine 
    """
    response  = RAG.get_llm_response(user_query=prompt)
    if response['is_sql']:
        return  response['doc_ans']  
    else :
        return response['normal_response']
    
def get_vector_store(filename):
    """
    Method to create the chunks from meta data file
    """
