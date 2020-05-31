from markov import create_chain, create_sentences, set_var
from main_nn import generate_title, generate_abstract

def generate(parts, N):
    chain = create_chain(parts)
    new_sentences = create_sentences(chain, N)
    return new_sentences

def create_abstract(keywords, method, dataframe, title_model, abstract_model):
    title, abstract = set_var(keywords, dataframe)
    if method == 'markov':
        new_title = generate(title, 4)
        new_body = generate(abstract, 150)
    else:
        new_title = generate_title(generate(title, 1), title_model)
        new_body = generate_abstract(generate(abstract, 1), abstract_model)
    return new_title, new_body
