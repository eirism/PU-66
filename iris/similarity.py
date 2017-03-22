from gensim import corpora, models, similarities
from collections import defaultdict


def similarity(inputTexts, inputText, threshold):
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
    # Store the dictionary??

    corpus = [dictionary.doc2bow(text) for text in texts]
    # store to disk, for later use??

    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

    # Doc is the input we compare to corpus for similarities
    doc = str(inputText)
    vec_bow = dictionary.doc2bow(doc.lower().split())
    vec_lsi = lsi[vec_bow]  # convert the query to LSI space
    index = similarities.MatrixSimilarity(lsi[corpus])
    sims = index[vec_lsi]
    # print(list(enumerate(sims)))

    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print(sims)

    # Create a list of questions with higher cosine similiarty than threshold
    similiarQuestions = []
    for sim in sims:
        if sim[1] > threshold:
            similiarQuestions.append(inputTexts[sim[0]])
    return similiarQuestions


documents = ["This is not a test question related to the testing",
             "Python is great question",
             "A python student asked a super question this great evening",
             "Great python lecture"]

compare = "This is test question"

a = similarity(documents, compare, 0.8)
print(a)
