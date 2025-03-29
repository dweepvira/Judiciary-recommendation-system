# standard packages
import pandas as pd
import numpy as np

# nlp packages
import string
import nltk
from nltk.corpus import stopwords
import gensim
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load("en_core_web_lg")
# EDA packages

from sklearn.metrics.pairwise import cosine_similarity

import nltk
from nltk.tokenize import word_tokenize
import csv
from gensim.models import word2vec
import pickle



def ipc_suggest(text):
    # Open the file in binary mode
    with open('file.pkl', 'rb') as file:
        # Call load method to deserialze
        w2v = pickle.load(file)
    w2v_vocab = set(w2v.key_to_index)
    print(w2v_vocab)
    data = []
    filename = "ipc.csv"
    with open(filename, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    a = []
    for i in range(len(data)):
        a.append(data[i][1])
    # use n_similarity to compute a cosine similarity (should be reasonably robust)
    sentences_similarity = np.zeros(len(a))
    target_sentence = text
    target_sentence_words = [w for w in target_sentence.split() if w in w2v_vocab]
    for idx, sentence in enumerate(a):
        sentence_words = [w for w in sentence.split() if w in w2v_vocab]
        # print(sentence_words)
        if len(sentence_words) != 0:
            sim = w2v.n_similarity(target_sentence_words, sentence_words)
        # print(sim)
        sentences_similarity[idx] = sim
        # print(sentences_similarity)
    result = list(zip(sentences_similarity, a))
    result.sort(key=lambda item: item[0], reverse=True)
    s = [x[1] for x in result[:10]]
    z = []
    for i in s:
        for j in range(len(data)):
            if i == data[j][1]:
                z.append([data[j][0], data[j][1]])
    return z


def case_reccomender(test_case_date, test_input):
    def sent_to_words(sentences):
        for sentence in sentences:
            yield (gensim.utils.simple_preprocess(str(sentence), deacc=True))

    clean_data_df = pd.read_csv("supreme_court.csv")
    clean_data_df.head()
    list_of_token_text = list(sent_to_words(clean_data_df["issue.text"]))
    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(list_of_token_text)]
    model = Doc2Vec(
        documents,
        vector_size=300,
        window=1,
        min_count=1,
        workers=4,
        dm=1,
        sample=0.01,
        dm_concat=1,
        negative=5,
        dbow_words=1,
    )
    test_case_date = int(test_case_date)

    def clean_test_input(test_text):
        # test_input = test_text.text.lower().translate(str.maketrans('  ', '  ', string.punctuation)).replace('\n', ' ').replace('•', ' ').replace('“', ' ').replace('”', ' ')
        # test_input = nlp.tokenizer(test_input)
        # # s=word_tokenize(test_input)
        # # test_input = ''.join([str(elem) for elem in s])
        # test_input=stop_word_remove(test_input)

        test_input = word_tokenize(str(test_text))
        test_vector = model.infer_vector(test_input)

        input_vector = pd.DataFrame(test_vector).T
        return input_vector

    input_vector = clean_test_input(test_input)

    def docvec_df(model_docvecs):
        _list = []

        for i in range(len(model_docvecs)):
            test = pd.DataFrame({clean_data_df["id.case"][i]: list(model_docvecs[i])}).T
            _list.append(test)

        vec_features = pd.concat(_list, sort=False)
        return vec_features

    vec_features = docvec_df(model.docvecs)

    def date_df(clean_df):
        feature_df = clean_df
        feature_df = feature_df.drop(
            columns=[
                "3_judge_dc",
                "docket",
                "name",
                "citation.led",
                "citation.lexis",
                "citation.sct",
                "citation.us",
                "decision.authority",
                "decision.direction",
                "decision.dissent agrees",
                "decision.jurisdiction",
                "decision.precedent altered?",
                "decision.term",
                "decision.type",
                "decision.unconstitutional",
                "decision.winning party",
                "id.case issues",
                "id.docket",
                "id.vote",
                "issue.area",
                "issue.id",
                "laws.id",
                "laws.type",
                "lower court.direction",
                "lower court.disagreement?",
                "lower court.disposition",
                "lower court.reasons",
                "natural court.chief",
                "natural court.period",
                "origin.id",
                "source.id",
                "source.name",
                "voting.majority",
                "voting.minority",
                "voting.split on second",
                "voting.unclear",
                "arguments.petitioner.entity",
                "arguments.petitioner.id",
                "arguments.respondent.entity",
                "arguments.respondent.id",
                "decision.admin action.agency",
                "decision.admin action.id",
                "decision.case.disposition",
                "decision.case.unusual",
                "decision.date.day",
                "decision.date.full",
                "decision.date.month",
                "voting.majority assigner.id",
                "voting.majority assigner.name",
                "voting.majority writer.id",
                "voting.majority writer.name",
            ]
        )

        return feature_df

    feature_df = date_df(clean_data_df)

    def combine_df(df1, df2):
        combined_df = feature_df.merge(
            vec_features, left_on="id.case", right_index=True, copy=False
        )
        combined_df.drop(
            ["id.case", "issue.text", "natural court.id", "origin.name"],
            axis=1,
            inplace=True,
        )
        return combined_df

    combined_df = combine_df(feature_df, vec_features)

    def cosine_text_similarity(text_vector, case_date, combined_df, clean_data_df):
        alpha = -0.07  # weight of date and type of court

        text_similarity = cosine_similarity(combined_df.iloc[:, 1:], text_vector)
        rec_df = pd.DataFrame(
            {
                "_id": clean_data_df["id.case"],
                "date": combined_df["decision.date.year"],
                "similarity": list(text_similarity),
            }
        )
        rec_df["similarity"] = rec_df["similarity"].apply(lambda x: x[0])
        rec_df["date_similarity"] = rec_df["date"].apply(
            lambda x: abs(x - case_date) / 100
        )
        rec_df["tot_similarity"] = rec_df["similarity"] + (
            alpha * rec_df["date_similarity"]
        )
        rec_df = (
            rec_df.sort_values(by="tot_similarity", ascending=False)
            .reset_index()
            .loc[0:15]
        )
        rec_df.drop(["index"], axis=1, inplace=True)

        _ids = []
        for i in rec_df["_id"]:
            _ids.append(i)

        # print(_ids)
        _index_values = []
        for i in _ids:
            temp = str(clean_data_df.loc[clean_data_df["id.case"] == f"{i}"]["name"])
            temp2 = temp.split()[0]
            _index_values.append(int(temp2))

        case_list = []
        for j, i in enumerate(_index_values):
            # case_list.append(f"{j+1} -- {clean_data_df['name'][i]}")
            # case_list.append(f"{clean_data_df['decision.winning party'][i]}")
            # case_list.append(f"{clean_data_df['arguments.petitioner.entity'][i]}")

            # case_list.append(f"{clean_data_df['issue.text'][i]}")
            case_list.append(
                [
                    clean_data_df["name"][i],
                    clean_data_df["decision.winning party"][i],
                    clean_data_df["arguments.petitioner.entity"][i],
                    clean_data_df["issue.text"][i],
                ]
            )

        return case_list

    text = cosine_text_similarity(
        input_vector, test_case_date, combined_df, clean_data_df
    )
    return text
