'''
实现了 n-Gram 算法，并对 markov 生成的句子进行打分；
'''

n = 4
trainfilePath = 'rawdata/indomain.en'
generalDomainPath_En = 'rawdata/generaldomain.en'
generalDomainPath_Zh = 'rawdata/generaldomain.zh'
punctationList = [".",",",'"'] # 标点符号集合
# percentage = [0.1,0.2,0.3,0.4,0.5]
percentage = [0.1]
class ScoreInfo:
    score = 0
    content = ''
    lineId = -1
 
class NGram:
    # 词频
    __dicWordFrequency = dict()
    
    # 词段频
    # ld = locals()
    # for i in range(2,n+1):
    #     ld['__dicPhraseFrequency'+str(i)] = dict()
    __dicPhraseFrequency2 = dict()
    __dicPhraseFrequency3 = dict()
    __dicPhraseFrequency4 = dict()
    totalWords = 0
    
    # 词段概率
    # __dicPhraseProbability = dict() 

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
    def getTotalWords(self):
        if self.totalWords != 0:
            return self.totalWords
        count = 0
        for num in self.__dicWordFrequency.values():
            count += num
        self.totalWords = count
        return count

    def append(self,content):
        '''
        训练 ngram  模型
        :param content: 训练内容
        :return: 
        '''
        # 预处理
        content = content.rstrip()              # 删除末尾空白符

        for punctation in punctationList:
            content = content.replace(punctation,' '+punctation+' ')    # 标点符号前后加空格
        sp = content.split()                                            # 分割成单词
        ie = self.getIterator(sp)                                       # n-Gram 模型
        
        # 加入前n-1个单词
        for i in range(n-1):
            # self.__vocabularySize.add(sp[i])
            if i < len(sp):
                if sp[i] not in self.__dicWordFrequency.keys():
                    self.__dicWordFrequency[sp[i]] = 1
                else:
                    self.__dicWordFrequency[sp[i]] += 1
                
        if(len(sp) >= 2):
            key2_1 = '%s_%s'%(sp[0],sp[1])
            if key2_1 not in self.__dicPhraseFrequency2.keys():
                self.__dicPhraseFrequency2[key2_1] = 0
            self.__dicPhraseFrequency2[key2_1] += 1
        
        if len(sp) >= 3:
            key2_2 = '%s_%s'%(sp[1],sp[2])
            if key2_2 not in self.__dicPhraseFrequency2.keys():
                self.__dicPhraseFrequency2[key2_2] = 0
            self.__dicPhraseFrequency2[key2_2] += 1
        
        if len(sp) >= 4:
            key3_1 = '%s_%s_%s'%(sp[0],sp[1],sp[2])
            if key3_1 not in self.__dicPhraseFrequency3.keys():
                self.__dicPhraseFrequency3[key3_1] = 0
            self.__dicPhraseFrequency3[key3_1] += 1
        
        # ld = locals()
        # for i in range(2,n+1):
        #     ld['keys'+str(i)] = []


        for w in ie:
            # 词频 
            # 0 1 ... n-1 already exist
            k = w[n-1]
            if k not in self.__dicWordFrequency.keys():
                self.__dicWordFrequency[k] = 0
            self.__dicWordFrequency[k] += 1
            
            # 词段频 2
            key2 = '%s_%s'%(w[2],w[3])
            if key2 not in self.__dicPhraseFrequency2.keys():
                self.__dicPhraseFrequency2[key2] = 0
            self.__dicPhraseFrequency2[key2] += 1
            
            # 词段频 3
            key3 = '%s_%s_%s'%(w[1],w[2],w[3])
            if key3 not in self.__dicPhraseFrequency3.keys():
                self.__dicPhraseFrequency3[key3] = 0
            self.__dicPhraseFrequency3[key3] += 1
            
            # 词段频 4
            key4 = '%s_%s_%s_%s'%(w[0],w[1],w[2],w[3])
            if key4 not in self.__dicPhraseFrequency4.keys():
                self.__dicPhraseFrequency4[key4] = 0
            self.__dicPhraseFrequency4[key4] += 1
 
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
        :return: 返回迭代器,item 为 tuple,每项 2 个值
        '''
        ct = len(txt)
        if ct<n:
            return txt
        # ld = locals
        for i in range(ct-(n-1)):
            # for j in range(n):
            #     ld['w'+str(i)] = txt[i+j]
            w1 = txt[i]
            w2 = txt[i+1]
            w3 = txt[i+2]
            w4 = txt[i+3]
            # ------------------------------------ #
            yield (w1,w2,w3,w4) # 这里我暂时没有替代为n
            # ------------------------------------ #
 
    def getScore(self,txt):
        '''
        使用 ugram 模型计算 str 得分
        :param txt: 
        :return: 
        '''
        lenTxt = len(txt.split())
        if lenTxt > 4 and lenTxt <20:
            return score * lenTxt
        else:
            return 0
        ie = self.getIterator(txt.split())
        score = 1
        v = len(self.__dicWordFrequency)
        total = self.getTotalWords()
        for w in ie:
            key4 = '%s_%s_%s_%s'%(w[0],w[1],w[2],w[3])
            key3 = '%s_%s_%s'%(w[0],w[1],w[2])
            key2 = '%s_%s'%(w[0],w[1])
            key1 = w[0]
            if key4 in self.__dicPhraseFrequency4.keys():
                    prob = ((self.__dicWordFrequency[key1]+1) / (total+v)) * \
                           ((self.__dicPhraseFrequency2[key2]+1)/(self.__dicWordFrequency[key1]+v)) * \
                           ((self.__dicPhraseFrequency3[key3]+1)/(self.__dicPhraseFrequency2[key2]+v)) * \
                           ((self.__dicPhraseFrequency4[key4]+1)/(self.__dicPhraseFrequency3[key3]+v))
            elif key3 in self.__dicPhraseFrequency3.keys():
                    prob = ((self.__dicWordFrequency[key1]+1) / (total+v)) * \
                           ((self.__dicPhraseFrequency2[key2]+1)/(self.__dicWordFrequency[key1]+v)) * \
                           ((self.__dicPhraseFrequency3[key3]+1)/(self.__dicPhraseFrequency2[key2]+v)) * \
                           (1/(self.__dicPhraseFrequency3[key3]+v))
            elif key2 in self.__dicPhraseFrequency2.keys():
                    prob = ((self.__dicWordFrequency[key1]+1) / (total+v)) * \
                           ((self.__dicPhraseFrequency2[key2]+1)/(self.__dicWordFrequency[key1]+v)) * \
                           (1/(self.__dicPhraseFrequency2[key2]+v)) * \
                           (1/v)
            elif key1 in self.__dicWordFrequency.keys():
                    prob = ((self.__dicWordFrequency[key1]+1) / (total+v)) * \
                            (1/(self.__dicWordFrequency[key1]+v)) * \
                            (1/v) * \
                            (1/v)
            else:
                    prob = (1/v)*(1/v)*(1/v)*(1/(total+v))
                # if w[0] in self.__dicWordFrequency.keys():
                #     prob = 1/(self.__dicWordFrequency[w[0]]+v)
                # else:
                #     prob = 1/v
            #fs.append(freq)
            score = prob * score
        #print(fs)
        #return str(round(score,2))
        # info = ScoreInfo()
        # info.score = score
        # info.content = txt
        
        return score * lenTxt
 
    def sort(self,infos):
        '''
        对结果排序
        :param infos: 
        :return: 
        '''
        return sorted(infos,key=lambda x:x.score,reverse=True)
 
 
def fileReader():
    with open(trainfilePath,'r',encoding='utf-8') as f:

        rows = 0
        # 按行统计
        while True:
            rows += 1
            line = f.readline()
            #line = re.sub('\n','',line)
            
            if not line:
                #print('read end %s'%path)
                return
            line = line.rstrip()
            #print('content rows=%s len=%s type=%s'%(rows,len(line),type(line)))
            #print(line)
            yield line

    
    
 
def getData():
    #使用相同语料随机生成的句子
    with open(generalDomainPath_En,'r',encoding='utf-8') as f:
        arr = []
        for line in f:
            line = line.rstrip()         
            arr.append(line)
       
    return arr
 
def trainNgram(): 
    ng = NGram()
    reader = fileReader()
    #将语料追加到 bigram 模型中
    for row in reader:
        ng.append(row)

    return ng

def ratingGeneralDomainData(ng):
    #测试生成的句子，是否合理
    arr = getData()
    infos= []
    for i in range(len(arr)):
        #对生成的句子打分
        info = ScoreInfo()
        info.score = ng.getScore(arr[i])
        info.lineId = i
        info.content = arr[i]
        infos.append(info)
    #排序
    return ng.sort(infos)

def dataSelection(infoArr):
    length = len(infoArr)
    zh_File = []
    with open(generalDomainPath_Zh,'r',encoding='utf-8') as inputFile:
        for line in inputFile:
            zh_File.append(line.rstrip())
    
    for topK in percentage:
        with open("dataSelect_en_top"+str(topK),'w',encoding='utf-8') as En_outPutfile:
            with open("dataSelect_zh_top"+str(topK),'w',encoding='utf-8') as Zh_outPutfile:
                for i in range(int(topK*length)):
                    En_outPutfile.write(infoArr[i].content+"\n")
                    Zh_outPutfile.write(zh_File[infoArr[i].lineId] + "\n")


    
def main():
    ng = trainNgram()
    infoArr = ratingGeneralDomainData(ng)
    dataSelection(infoArr)
    
                    
    # for info in infoArr:
    #     print('%s\t(score:  %s)'%(info.content,info.score))
    
 
if __name__ == '__main__':
    main()
    
