# encoding=utf-8
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from common_util import *
import csv, math
import time


def test():
    transformer = TfidfTransformer()
    vectorizer = CountVectorizer()
    corpus = [

        'A1 BD C1 D1 A1 E1 F1 C1 F1 A1 C1 one G1 H1 E1 F1'
        ,

        'A1  GB C1 D1 A1 E1 F1 C1 F1 A1 C1 two G1 H1 E1 F1'
        ,

        'A1  B1 C1 D1 A1 E1 F1 C1 FC1 A1 C1 three two G1 H1 DE F1'

    ]
    # corpus = [
    #     '锦绣江南|4期',
    #     '勤诚达22世纪',
    #     '碧海富通城6期',
    #     '观澜第3工业区',
    # ]
    X = vectorizer.fit_transform(corpus)
    print X.toarray()

    print ','.join(vectorizer.get_feature_names())
    tfidf = transformer.fit_transform(X.toarray())
    # print tfidf.toarray()
    for line in tfidf.toarray():
        print ','.join([str(round(n, 3)) for n in line])


def getAllParts(root_aoi=u'', words=[]):
    for i in range(len(root_aoi)):
        w = root_aoi[i]
        words.append(w)
        for j in range(i):
            words.append(root_aoi[j:i + 1])
    return words


def prepare_input():
    infile = ur'E:\work\AOI平台\work2\755\gj\todo.csv'
    otfile = ur'E:\work\AOI平台\work2\755\gj\tfidf_input.csv'
    count = 0
    f = open(otfile, 'wb')
    all_words = set()
    with open(infile, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for e in reader:
            count += 1
            if count % 10000 == 0:
                print count
            root_aoi = standardize(e['aoi'].decode('utf-8').replace('|', ''))
            all_words.add(root_aoi)

        csvfile.close()
    for root_aoi in all_words:
        words = []
        aoi_ary = getAllParts(root_aoi, words)
        words_line = ' '.join(aoi_ary).encode('utf-8') + '\n'
        # print words_line.strip()
        f.write(words_line)
    f.close()


def compute_tfidf():
    transformer = TfidfTransformer()
    vectorizer = CountVectorizer()
    infile = ur'E:\work\AOI平台\work2\755\gj\tfidf_input.csv'
    otfile = ur'E:\work\AOI平台\work2\755\gj\tfidf_output.csv'
    of = open(otfile, 'wb')

    corpus = []
    f = open(infile, 'rb')
    for line in f:
        corpus.append(line.strip().decode('utf-8'))
    print  'begin to convert vector and computer tfidf'
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    words = vectorizer.get_feature_names()

    print 'begin to output'
    count = 0
    for line in tfidf:
        # print ','.join([str(round(n, 3)) for n in line])
        # line = tfidf_ary[i]
        count += 1
        if count % 100 == 0:
            break
        line_data = line.toarray()[0]
        result = ''
        for j in range(len(line_data)):
            w = round(line_data[j], 6)
            if math.fabs(w) > 1e-6:
                result += words[j] + ':' + str(w) + '   '
        of.write(result.encode('utf-8').strip(' ') + '\n')
    of.close()


if __name__ == '__main__':
    # prepare_input()
    compute_tfidf()
