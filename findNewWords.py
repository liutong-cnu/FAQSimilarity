#import pymongo

#db = pymongo.MongoClient().baike.items
def texts():
    #for a in db.find(no_cursor_timeout=True).limit(1000000):
        #yield a['content']
	with open("findNewWords_query.txt") as f:
		for line in f.readlines():
			a = line.strip()
			yield a

from collections import defaultdict #defaultdict是经过封装的dict，它能够让我们设定默认值
from tqdm import tqdm #tqdm是一个非常易用的用来显示进度的库
from math import log
import re

class Find_Words:
    def __init__(self, min_count=10, min_pmi=0):
        self.min_count = min_count
        self.min_pmi = min_pmi
        self.chars, self.pairs, self.three, self.four, self.five, self.six = defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int) #如果键不存在，那么就用int函数
                                                                  #初始化一个值，int()的默认结果为0
        self.total = 0.
    def text_filter(self, texts): #预切断句子，以免得到太多无意义（不是中文、英文、数字）的字符串
        for a in tqdm(texts):
            for t in re.split(u'[^\u4e00-\u9fa50-9a-zA-Z]+', a): #这个正则表达式匹配的是任意非中文、
                                                              #非英文、非数字，因此它的意思就是用任
                                                              #意非中文、非英文、非数字的字符断开句子
                if t:
                    yield t
    def count(self, texts): #计数函数，计算单字出现频数、相邻两字出现的频数
        for text in self.text_filter(texts):
            self.chars[text[0]] += 1
            for i in range(len(text)-6):
                self.chars[text[i+1]] += 1
                self.pairs[text[i:i+2]] += 1
                self.total += 1
        self.chars = {i:j for i,j in self.chars.items() if j >= self.min_count} #最少频数过滤
        self.pairs = {i:j for i,j in self.pairs.items() if j >= self.min_count} #最少频数过滤
		self.three = {i:j for i,j in self.three.items() if j >= self.min_count} #最少频数过滤
		self.four = {i:j for i,j in self.four.items() if j >= self.min_count} #最少频数过滤
		self.five = {i:j for i,j in self.five.items() if j >= self.min_count} #最少频数过滤
		self.six = {i:j for i,j in self.six.items() if j >= self.min_count} #最少频数过滤
        self.strong_segments = set()
        for i,j in self.pairs.items(): #根据互信息找出比较“密切”的邻字
            _ = log(self.total*j/(self.chars[i[0]]*self.chars[i[1]]))
            if _ >= self.min_pmi:
                self.strong_segments.add(i)
		for i,j in self.three.items(): #根据互信息找出比较“密切”的邻字
            _ = log(self.total*j/(self.chars[i[0]]*self.chars[i[1]]*self.chars[i[2]]))
            if _ >= self.min_pmi:
                self.strong_segments.add(i)
		for i,j in self.four.items(): #根据互信息找出比较“密切”的邻字
            _ = log(self.total*j/(self.chars[i[0]]*self.chars[i[1]]*self.chars[i[2]]*self.chars[i[3]]))
            if _ >= self.min_pmi:
                self.strong_segments.add(i)
		for i,j in self.five.items(): #根据互信息找出比较“密切”的邻字
            _ = log(self.total*j/(self.chars[i[0]]*self.chars[i[1]]*self.chars[i[2]]*self.chars[i[3]]*self.chars[i[4]]))
            if _ >= self.min_pmi:
                self.strong_segments.add(i)
		for i,j in self.six.items(): #根据互信息找出比较“密切”的邻字
            _ = log(self.total*j/(self.chars[i[0]]*self.chars[i[1]]*self.chars[i[2]]*self.chars[i[3]]*self.chars[i[4]]*self.chars[i[5]]))
            if _ >= self.min_pmi:
                self.strong_segments.add(i)
    def find_words(self, texts): #根据前述结果来找词语
        self.words = defaultdict(int)
        for text in self.text_filter(texts):
            s = text[0]
            for i in range(len(text)-1):
                if text[i:i+2] in self.strong_segments: #如果比较“密切”则不断开
                    s += text[i+1]
                else:
                    self.words[s] += 1 #否则断开，前述片段作为一个词来统计
                    s = text[i+1]
			for i in range(len(text)-2):
                if text[i:i+3] in self.strong_segments: #如果比较“密切”则不断开
                    s += text[i+2]
                else:
                    self.words[s] += 1 #否则断开，前述片段作为一个词来统计
                    s = text[i+2]
			for i in range(len(text)-3):
                if text[i:i+4] in self.strong_segments: #如果比较“密切”则不断开
                    s += text[i+3]
                else:
                    self.words[s] += 1 #否则断开，前述片段作为一个词来统计
                    s = text[i+3]
			for i in range(len(text)-4):
                if text[i:i+5] in self.strong_segments: #如果比较“密切”则不断开
                    s += text[i+4]
                else:
                    self.words[s] += 1 #否则断开，前述片段作为一个词来统计
                    s = text[i+4]
			for i in range(len(text)-5):
                if text[i:i+6] in self.strong_segments: #如果比较“密切”则不断开
                    s += text[i+5]
                else:
                    self.words[s] += 1 #否则断开，前述片段作为一个词来统计
                    s = text[i+5]
        self.words = {i:j for i,j in self.words.items() if j >= self.min_count} #最后再次根据频数过滤

fw = Find_Words(10, 1)
fw.count(texts())
fw.find_words(texts())

#import pandas as pd
#words = pd.Series(fw.words).sort_values(ascending=False)