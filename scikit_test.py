# encoding=utf-8
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import csv, math
import time


def test():
    transformer = TfidfTransformer()
    vectorizer = CountVectorizer()
    corpus = [

        # '75 759 59 759城 59城 9城 759城市 59城市 9城市 城市 759城市公 59城市公 9城市公 城市公 市公 759城市公寓 59城市公寓 9城市公寓 城市公寓 市公寓 公寓',
        # '75 759 59 759城 59城 9城 759城市 59城市 9城市 城市 759城市公 59城市公 9城市公 城市公 市公 759城市公寓 59城市公寓 9城市公寓 城市公寓 市公寓 公寓 旺棠 旺棠工 棠工 旺棠工业 棠工业 工业 旺棠工业园 棠工业园 工业园 业园 旺棠工业园7 棠工业园7 工业园7 业园7 园7 旺棠工业园75 棠工业园75 工业园75 业园75 园75 75 旺棠工业园759 棠工业园759 工业园759 业园759 园759 759 59 旺棠工业园759公 棠工业园759公 工业园759公 业园759公 园759公 759公 59公 9公 旺棠工业园759公寓 棠工业园759公寓 工业园759公寓 业园759公寓 园759公寓 759公寓 59公寓 9公寓 公寓',
        # '75 759 59 759城 59城 9城 759城市 59城市 9城市 城市 759城市公 59城市公 9城市公 城市公 市公 759城市公寓 59城市公寓 9城市公寓 城市公寓 市公寓 公寓 旺棠 旺棠工 棠工 旺棠工业 棠工业 工业 旺棠工业园 棠工业园 工业园 业园 旺棠工业园7 棠工业园7 工业园7 业园7 园7 旺棠工业园75 棠工业园75 工业园75 业园75 园75 75 旺棠工业园759 棠工业园759 工业园759 业园759 园759 759 59 旺棠工业园759公 棠工业园759公 工业园759公 业园759公 园759公 759公 59公 9公 旺棠工业园759公寓 棠工业园759公寓 工业园759公寓 业园759公寓 园759公寓 759公寓 59公寓 9公寓 公寓 07 075 75 0759 759 59 0759城 759城 59城 9城 0759城市 759城市 59城市 9城市 城市 0759城市公 759城市公 59城市公 9城市公 城市公 市公 0759城市公寓 759城市公寓 59城市公寓 9城市公寓 城市公寓 市公寓 公寓',
        # '75 759 59 759城 59城 9城 759城市 59城市 9城市 城市 759城市公 59城市公 9城市公 城市公 市公 759城市公寓 59城市公寓 9城市公寓 城市公寓 市公寓 公寓 旺棠 旺棠工 棠工 旺棠工业 棠工业 工业 旺棠工业园 棠工业园 工业园 业园 旺棠工业园7 棠工业园7 工业园7 业园7 园7 旺棠工业园75 棠工业园75 工业园75 业园75 园75 75 旺棠工业园759 棠工业园759 工业园759 业园759 园759 759 59 旺棠工业园759公 棠工业园759公 工业园759公 业园759公 园759公 759公 59公 9公 旺棠工业园759公寓 棠工业园759公寓 工业园759公寓 业园759公寓 园759公寓 759公寓 59公寓 9公寓 公寓 07 075 75 0759 759 59 0759城 759城 59城 9城 0759城市 759城市 59城市 9城市 城市 0759城市公 759城市公 59城市公 9城市公 城市公 市公 0759城市公寓 759城市公寓 59城市公寓 9城市公寓 城市公寓 市公寓 公寓 75 759 59 759公 59公 9公 759公寓 59公寓 9公寓 公寓'

        # 'AB AB文化 AB文化广场 文化广场 广场',
        # 'AB AB广场 广场'
        '李松朗129工业区 李松朗129工业 松朗129工业区 李松朗129工 松朗129工业 朗129工业区 李松朗129 松朗129工 朗129工业 129工业区 李松朗12 松朗129 朗129工 129工业 29工业区 李松朗1 松朗12 朗129 129工 29工业 9工业区 李松朗 松朗1 朗12 129 29工 9工业 工业区 李松 松朗 朗1 12 29 9工 工业 业区',
        '129工业园 129工业 29工业园 129工 29工业 9工业园 129 29工 9工业 工业园 12 29 9工 工业 业园',
        '李松蓢129工业区 李松蓢129工业 松蓢129工业区 李松蓢129工 松蓢129工业 蓢129工业区 李松蓢129 松蓢129工 蓢129工业 129工业区 李松蓢12 松蓢129 蓢129工 129工业 29工业区 李松蓢1 松蓢12 蓢129 129工 29工业 9工业区 李松蓢 松蓢1 蓢12 129 29工 9工业 工业区 李松 松蓢 蓢1 12 29 9工 工业 业区',
        '第一129工业园 第一129工业 一129工业园 第一129工 一129工业 129工业园 第一129 一129工 129工业 29工业园 第一12 一129 129工 29工业 9工业园 第一1 一12 129 29工 9工业 工业园 第一 一1 12 29 9工 工业 业园',
        '第一工业129工业园 第一工业129工业 一工业129工业园 第一工业129工 一工业129工业 工业129工业园 第一工业129 一工业129工 工业129工业 业129工业园 第一工业12 一工业129 工业129工 业129工业 129工业园 第一工业1 一工业12 工业129 业129工 129工业 29工业园 第一工业 一工业1 工业12 业129 129工 29工业 9工业园 第一工 一工业 工业1 业12 129 29工 9工业 工业园 第一 一工 工业 业1 12 29 9工 工业 业园'

    ]
    # corpus = [
    #     '锦绣江南|4期',
    #     '勤诚达22世纪',
    #     '碧海富通城6期',
    #     '观澜第3工业区',
    # ]
    X = vectorizer.fit_transform(corpus)
    print X.toarray()
    words = vectorizer.get_feature_names()
    tfidf = transformer.fit_transform(X.toarray())
    # print tfidf.toarray()
    print ','.join(words)
    for line in tfidf.toarray():
        print ','.join([str(round(n, 3)) for n in line])


def getAllParts(root_aoi=u''):
    words = []
    for i in range(len(root_aoi)):
        for j in range(i):
            words.append(root_aoi[j:i + 1])
    words.sort(key=lambda o: -len(o))
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
            root_aoi = e['aoi'].decode('utf-8').replace('|', '')
            all_words.add(root_aoi)

        csvfile.close()
    for root_aoi in all_words:
        words = aoi_ary = getAllParts(root_aoi)
        words_line = ' '.join(aoi_ary).encode('utf-8') + '\n'
        # print words_line.strip()
        f.write(words_line)
    f.close()


def prepare_alias_input():
    otfile = ur'alias_input_test.csv'
    f = open(otfile, 'wb')
    words = ur'李松朗129工业区#一二九工业园#129工业园#李松蓢129工业区#第一129工业园#第一工业129工业园'.split('#')
    for s in words:
        aoi_ary = getAllParts(s)
        words_line = ' '.join(aoi_ary).encode('utf-8') + '\n'
        # print words_line.strip()
        print words_line.strip()
        f.write(words_line)
    f.close()


def compute_tfidf():
    transformer = TfidfTransformer()
    vectorizer = CountVectorizer()
    infile = ur'alias_input_test.csv'
    otfile = ur'alias_output_test.csv'
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
            w = round(line_data[j], 3)
            if math.fabs(w) > 1e-6:
                result += words[j] + ':' + str(w) + '   '
        of.write(result.encode('utf-8').strip(' ') + '\n')
    of.close()


if __name__ == '__main__':
    # prepare_input()
    compute_tfidf()
    # prepare_alias_input()
    # test()
