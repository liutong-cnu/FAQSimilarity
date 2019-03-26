# FAQSimilarity
本目录用于智能客服领域中FAQ相似度算法的调研

【如何用 word2vec 计算两个句子之间的相似度？】https://www.zhihu.com/question/29978268/answer/55338644  
【一种基于 CNN 的短文本表达模型】https://cloud.tencent.com/developer/article/1006249  
【Siamese Network】https://blog.csdn.net/thriving_fcl/article/details/73730552  
https://zhuanlan.zhihu.com/p/35040994  
【word2vec + tfidf】https://blog.csdn.net/zhouboke/article/details/80591208  

 
   
2019.3.18-22 
新词发现方法
【方法】词频+信息熵的切词方法  
【参考】http://www.matrix67.com/blog/archives/5044  
https://spaces.ac.cn/archives/4256  
对广西27w扩展问进行jieba分词，对词进行组合和发现，得到本该分到一起而没有分到一起的词，通过设置阈值的方式得到中的新词，即userwords。通过与现有词表中的词做差集，得到userwords中的未登录词。这种新词发现的方法为userwords的添加提供依据，同时可以发现oov的词，也可以作为同义词替换的参考。
