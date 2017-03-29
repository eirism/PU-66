from gensim import corpora, models, similarities
from collections import defaultdict


def similarity(inputTexts, inputText, threshold):
    """

        The comparison algorithm for questions.

        Creates a Vector Space Model of questions.
        Calculates the cosine similarity between different questions in this space.
        Returns a list of similar questions satisfying.

        """
    documents = inputTexts

    # Remove common words and tokenize
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in documents]

    # Remove words that appear only once
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]

    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
    doc = str(inputText)
    vec_bow = dictionary.doc2bow(doc.lower().split())
    # convert the query to LSI space
    vec_lsi = lsi[vec_bow]
    index = similarities.MatrixSimilarity(lsi[corpus])
    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print(sims)

    similar_questions = list()
    for sim in sims:
        if sim[1] > threshold:
            similar_questions.append(inputTexts[sim[0]])
    return similar_questions

