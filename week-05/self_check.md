# Why a given query did or didn't return the right chunk
## Embeddings
Both the query and the corpus must use the same embedding model. It should be a model with training / knowledge related to the specific domain of the corpus, if not simple general knowledge.

## Chunking strategy
A chunk should represent roughly what a person would refer to as a "fact" or an "idea". It should be relatively atomic, so as not to add unrelated context to the model context window. 


## Top N
There is a balance to be struck here between making sure the relevant chunks are in context (high N, to counterbalance a lack of retrieval precision) and context management (too high, and expose the model to noise). The more atomic, the knowledge base, and the more precise the retrieval function, the lower N you can likely use.
