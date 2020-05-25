from markov import create_chain, create_sentences, set_var

def generate(parts, N):
    chain = create_chain(parts)
    new_sentences = create_sentences(chain, N)
    return new_sentences

def create_abstract(keywords):
    title, abstract = set_var(keywords)
    new_title = generate(title, 4)
    new_body = generate(abstract, 150)
    return new_title, new_body
