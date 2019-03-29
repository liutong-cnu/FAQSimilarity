#_*_coding=utf-8_*_
import jieba
import math
import gensim
class BM25(object):
    def __init__(self):
        self.idf = {} # 存储每个词的idf值
        self.df = {} # 存储每个词及出现了该词的文档数量
        self.k1 = 2
        self.k2 = 0.75
        self.b = 0.75
        self.posts = []
        self.avgdl = 0
        self.stop_words = ["！", "？","，","（","）","。",".",":","/","“","”"]
        self.init()
    
    def init(self):
        N = 270164
        with open("findNewWords_query.txt") as fr:
            for line in fr.readlines():
                words = list(jieba.cut(line.strip()))
                words = self.filter_stop(words)
                self.avgdl += len(words)
                self.posts.append(words)
                setwords = set(words)
                for word in setwords:
                    self.df[word] = self.df.get(word, 0) + 1

        self.avgdl = self.avgdl / N
        for k, v in self.df.items():   
            self.idf[k] = math.log((N- v + 0.5)/(v + 0.5))
    
    def filter_stop(self, words):
        fw = []
        for word in words:
            if word not in self.stop_words:
                fw.append(word)
        return fw
    
    def BMscore(self, query):
        posts = self.posts
        words = list(jieba.cut(query)) # query及分词
        words = self.filter_stop(words)
        print("#".join(words))
        scores = []
        for post in posts:
            sc = 0
            for word in words:
                sc += self.idf.get(word, 0) *  post.count(word) * (self.k1 + 1) / ((post.count(word) + self.k1 *(1-self.b+self.b*len(post)/self.avgdl))) * words.count(word) * (self.k2 + 1) /  (words.count(word) + self.k2)
            scores.append(sc)
        # for s in scores:print (s)
        max_score = max(scores)
        # print("ms:", max_score)
        reply = posts[scores.index(max_score)]
        return reply, max_score
    
    def pqscore(self, query):
        all_words = []
        with open('Trio_embedding.txt') as f:
            for line in f.readlines():
                all_words.append(line.strip().split()[0])
        # print(all_words)
        model = gensim.models.KeyedVectors.load_word2vec_format('Trio_embedding.txt', binary=False) 
        # print(model.similarity("取消", "开通"))
        posts = self.posts
        words = list(jieba.cut(query)) # query及分词
        words = self.filter_stop(words)
        qs_ = []
        ps_ = []
        for post in posts:
            # p2q
            for q in words:
                qs = 0
                qscore = []
                for p in post:
                    s = 0
                    if p in all_words and q in all_words:
                        s = model.similarity(q, p)
                    qscore.append(s)
                    # print ("s:", s)
                qs += max(qscore)
                # print("qs:", qs)
            qs = qs / len(words)
            qs_.append(qs)

            #q2p
            for p in post:
                ps = 0
                pscore = []
                for q in words:
                    s = model.similarity(q, p) if (p in all_words and q in all_words) else 0
                    pscore.append(s)
                ps += max(pscore)
            ps = ps / len(post)
            ps_.append(ps)
        
        print(len(ps_), len(qs_))
        final_score = []
        for i in range(len(ps_)):
            avg = (ps_[i] + qs_[i])/2
            delta = math.fabs(qs_[i] / len(words) - avg)
            fs = avg * (1- delta)
            final_score.append(fs)
        max_score = max(final_score)
        reply = posts[final_score.index(max_score)]
        print("".join(reply), max_score)
        return reply, max_score

if __name__ == "__main__":
    s = BM25()
    # with open("gx_wechat.txt") as frr:
    #     for line in frr.readlines():
    #         line = line.strip()
    #         res, ms = s.BMscore(line)
    #         print(line + "\t" + "".join(res) + "\t" + str(ms))

    res, ms = s.BMscore("2元1G流量月包")
    print("".join(res), ms)

    # with open("gx_wechat.txt") as frr:
    #     for line in frr.readlines():
    #         line = line.strip()
    #         res, ms = s.pqscore(line)
    #         print(line + "\t" + "".join(res) + "\t" + str(ms))

    # s.pqscore("充值未到账处理方法")

            
                    

                    
                    


