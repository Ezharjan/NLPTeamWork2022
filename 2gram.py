'''
实现了 4-Gram 算法，并对 markov 生成的句子进行打分；
'''

punctuationfilePath = 'punctuation.txt'
trainfilePath = 'IWSLT14.TED.tst2014.zh-en.en'
testfilePath = 'dsds.txt'

class ScoreInfo:
    score = 0
    content = ''
 
class NGram:
    __dicWordFrequency = dict() #词频
    __dicPhraseFrequency = dict() #词段频
    __dicPhraseProbability = dict() #词段概率
    __vocabularySize = set() #词汇表大小

    # def printNGram(self):
    #     print('词频')
    #     for key in self.__dicWordFrequency.keys():
    #         print('%s\t%s'%(key,self.__dicWordFrequency[key]))
    #     print('词段频')
    #     for key in self.__dicPhraseFrequency.keys():
    #         print('%s\t%s'%(key,self.__dicPhraseFrequency[key]))
    #     print('词段概率')
    #     for key in self.__dicPhraseProbability.keys():
    #         print('%s\t%s'%(key,self.__dicPhraseProbability[key]))
 
    def append(self,content):
        '''
        训练 ngram  模型
        :param content: 训练内容
        :return: 
        '''
        # 预处理
        content = content.rstrip()              # 删除末尾空白符
        punctationList = []                     # 标点符号集合
        with open(punctuationfilePath, 'r', encoding='utf-8') as f:
            for line in f:
                punctationList.append(line.rstrip())
        
        for punctation in punctationList:
            content = content.replace(punctation,' '+punctation+' ')    # 标点符号前后加空格
        sp = content.split()                    # 分割成单词
        
        
        ie = self.getIterator(sp)               #2-Gram 模型
        
        # 加入第一个单词
        self.__vocabularySize.add(sp[0])
        if sp[0] not in self.__dicWordFrequency.keys():
            self.__dicWordFrequency[sp[0]] = 1
        else:
            self.__dicWordFrequency[sp[0]] += 1
        
        keys = []
        for w in ie:
            #词频 0 1 2 already exists
            k = w[1]
            self.__vocabularySize.add(k)
            
            if k not in self.__dicWordFrequency.keys():
                self.__dicWordFrequency[k] = 0

            self.__dicWordFrequency[k] += 1
            
            #词段频
            key = '%s_%s'%(w[0],w[1])
            keys.append(key)
            if key not in self.__dicPhraseFrequency.keys():
                self.__dicPhraseFrequency[key] = 0
            self.__dicPhraseFrequency[key] += 1
 
        #词段概率
        # for w1w2 in keys:
        #     w1 = w1w2.split('_')[0]
        #     w1Freq = self.__dicWordFrequency[w1]
        #     w1w2Freq = self.__dicPhraseFrequency[w1w2]
        #     # P(w2|w1) = w1w2出现的总次数/w1出现的总次数 = 827/2533 ≈0.33 , 即 w2 在 w1 后面的概率
        #     self.__dicPhraseProbability[w1w2] = round(w1w2Freq/w1Freq,2)
        
 
    def getIterator(self,txt):
        '''
        bigram 模型迭代器
        :param txt: 一段话或一个句子
        :return: 返回迭代器，item 为 tuple，每项 2 个值
        '''
        ct = len(txt)
        if ct<2:
            return txt
        for i in range(ct-1):
            w1 = txt[i]
            w2 = txt[i+1]
            yield (w1,w2)
 
    def getScore(self,txt):
        '''
        使用 ugram 模型计算 str 得分
        :param txt: 
        :return: 
        '''
        ie = self.getIterator(txt.split())
        score = 1
        #fs = []
        v = len(self.__vocabularySize)
        
        for w in ie:
            key = '%s_%s'%(w[0],w[1])
            if key in self.__dicPhraseFrequency.keys():
                prob = (self.__dicPhraseFrequency[key]+1)/(self.__dicWordFrequency[w[0]]+v)
            else:
                if w[0] in self.__dicWordFrequency.keys():
                    prob = 1/(self.__dicWordFrequency[w[0]]+v)
                else:
                    prob = 1/v
            #fs.append(freq)
            score = prob * score
        #print(fs)
        #return str(round(score,2))
        info = ScoreInfo()
        info.score = score
        info.content = txt
        return info
 
    def sort(self,infos):
        '''
        对结果排序
        :param infos: 
        :return: 
        '''
        return sorted(infos,key=lambda x:x.score,reverse=True)
 
 
def fileReader():
    path = trainfilePath
    with open(path,'r',encoding='utf-8') as f:

        rows = 0
        # 按行统计
        while True:
            rows += 1
            line = f.readline()
            #line = re.sub('\n','',line)
            
            if not line:
                print('read end %s'%path)
                return
            line = line.rstrip()
            #print('content rows=%s len=%s type=%s'%(rows,len(line),type(line)))
            #print(line)
            yield line

    
    
 
def getData():
    #使用相同语料随机生成的句子
    with open(testfilePath,'r',encoding='utf-8') as f:
        arr = []
        for line in f:
            line = line.rstrip()         
            arr.append(line)
       
    return arr
 
 
 
def main():
    ng = NGram()
    reader = fileReader()
    #将语料追加到 bigram 模型中
    for row in reader:
        
        ng.append(row)
    #ng.printNGram()
    #测试生成的句子，是否合理
    arr = getData()
    infos= []
    for s in arr:
        #对生成的句子打分
        info = ng.getScore(s)
        infos.append(info)
    #排序
    infoArr = ng.sort(infos)
    for info in infoArr:
        print('%s\t(score:  %s)'%(info.content,info.score))
    
 
if __name__ == '__main__':
    main()
    
