from xml.etree.ElementTree import parse
import nltk
import os
import math
from nltk.corpus import wordnet
from nltk.tag.stanford import POSTagger
java_path ="C:\\Program Files\\Java\\jdk1.8.0_11\\bin\\java.exe"
st=POSTagger('C:\\Users\\SeongWooLim\\Desktop\\RTE\\stanford-postagger\\models\\english-bidirectional-distsim.tagger','C:\\Users\\SeongWooLim\\Desktop\\RTE\\stanford-postagger\\stanford-postagger.jar',encoding='UTF-8')
os.environ['JAVAHOME'] = java_path

data=open('C:\\Users\\SeongWooLim\\Desktop\\RTE\\Treshold3.txt','r')
Tres=float(data.read())
data.close()
Pre=0
Fail=0
n_t=0
n_f=0
s_t=0
s_f=0
while(True):
    print("Type Hypothesis:")
    h=input()
    print("Type Text:")
    t=input()
    h_t=nltk.word_tokenize(h)
    #t_h_t=nltk.pos_tag(h_t)
    t_h_t=st.tag(h_t)[0]
    t_t=nltk.word_tokenize(t)
    #t_t_t=nltk.pos_tag(t_t)
    t_t_t=st.tag(t_t)[0]
    Sim=1
    flag=True
    for i in range(len(h_t)):
        ss=None
        ss2=None
        Match=False
        if (h_t[i]=="not")|(h_t[i]=="no")|(h_t[i]=="n't")|(h_t[i]=="never"):
            if flag==True:
                flag=False
            else:
                flag=True
        elif(t_h_t[i][1]=="NN")|(t_h_t[i][1]=="NNS")|(t_h_t[i][1]=="NNP")|(t_h_t[i][1]=="NNPS"):
            #print("nnnnnnnnnn")
            if h_t[i] not in t_t:
                ss=wordnet.synsets(h_t[i],pos=wordnet.NOUN)
                for j in range(len(t_t)):
                    if(t_t_t[j][1]=="NN")|(t_t_t[j][1]=="NNS")|(t_t_t[j][1]=="NNP")|(t_t_t[j][1]=="NNPS"):
                        if Match==True:
                            break
                        for k in range(len(ss)):
                            if Match==True:
                                break
                            if t_t[j] in [str(lemma.name()) for lemma in ss[k].lemmas()]:
                                Match=True
                                break
                            else:
                                for n in range(len(ss[k].hyponyms())):
                                    if t_t[j] in [str(lemma.name()) for lemma in ss[k].hyponyms()[n].lemmas()]:
                                        Match=True
                                        break
                if Match==False:
                    for j in range(len(t_t)):
                        if(t_t_t[j][1]=="NN")|(t_t_t[j][1]=="NNS")|(t_t_t[j][1]=="NNP")|(t_t_t[j][1]=="NNPS"):
                            for k in range(len(ss)):
                                if Match==True:
                                    break
                                for n in range(len(ss[k].lemmas())):
                                    if t_t[j] in [str(lemma.name()) for lemma in ss[k].lemmas()[n].antonyms()]:
                                        Match=True
                                        if flag==True:
                                            flag=False
                                        else:
                                            flag=True
                                        break
                    if Match==False:
                        buf=0
                        for j in range(len(t_t)):
                            if(t_t_t[j][1]!="CC")&(t_t_t[j][1]!="DT")&(t_t_t[j][1]!="TO")&(t_t_t[j][1]!=".")&(t_t_t[j][1]!=",")&(t_t_t[j][1]!=":")&(t_t_t[j][1]!="IN"):
                                ss2=wordnet.synsets(t_t[j],pos=wordnet.NOUN)
                                for k in range(len(ss)):
                                    for n in range(len(ss2)):
                                        if ss[k].wup_similarity(ss2[n])!=None:
                                            if buf<ss[k].wup_similarity(ss2[n]):
                                                buf=ss[k].wup_similarity(ss2[n])
                        Sim=Sim*buf
        elif(t_h_t[i][1]=="VB")|(t_h_t[i][1]=="VBD")|(t_h_t[i][1]=="VBG")|(t_h_t[i][1]=="VBN")|(t_h_t[i][1]=="VBP")|(t_h_t[i][1]=="VBZ"):
            #print("vvvvvvvvvv")
            if h_t[i] not in t_t:
                ss=wordnet.synsets(h_t[i],pos=wordnet.VERB)
                for j in range(len(t_t)):
                    if Match==True:
                        break
                    if(t_t_t[j][1]=="VB")|(t_t_t[j][1]=="VBD")|(t_t_t[j][1]=="VBG")|(t_t_t[j][1]=="VBN")|(t_t_t[j][1]=="VBP")|(t_t_t[j][1]=="VBZ"):
                        for k in range(len(ss)):
                            if t_t[j] in [str(lemma.name()) for lemma in ss[k].lemmas()]:
                                Match=True
                                if ((t_h_t[i][1]=="VBN")&(t_t_t[j][1]!="VBN")|(t_h_t[i][1]!="VBN")&(t_t_t[j][1]=="VBN")):
                                    if flag==True:
                                        flag=False
                                    else:
                                        flag=True
                                break
                            else:
                                for n in range(len(ss[k].hyponyms())):
                                    if t_t[j] in [str(lemma.name()) for lemma in ss[k].hyponyms()[n].lemmas()]:
                                        Match=True
                if Match==False:
                    for j in range(len(t_t)):
                        if Match==True:
                            break
                        if(t_t_t[j][1]=="VB")|(t_t_t[j][1]=="VBD")|(t_t_t[j][1]=="VBG")|(t_t_t[j][1]=="VBN")|(t_t_t[j][1]=="VBP")|(t_t_t[j][1]=="VBZ"):
                            for k in range(len(ss)):
                                for n in range(len(ss[k].lemmas())):
                                    if t_t[j] in [str(lemma.name()) for lemma in ss[k].lemmas()[n].antonyms()]:
                                        Match=True
                                        if ((t_h_t[i][1]=="VBN")&(t_t_t[j][1]=="VBN"))|((t_h_t[i][1]!="VBN")&(t_t_t[j][1]!="VBN")):
                                            if flag==True:
                                                flag=False
                                            else:
                                                flag=True
                                        break
                    if Match==False:
                        buf=0
                        for j in range(len(t_t)):
                            if(t_t_t[j][1]!="CC")&(t_t_t[j][1]!="DT")&(t_t_t[j][1]!="TO")&(t_t_t[j][1]!=".")&(t_t_t[j][1]!=",")&(t_t_t[j][1]!=":")&(t_t_t[j][1]!="IN"):
                                ss2=wordnet.synsets(t_t[j],pos=wordnet.VERB)
                                for k in range(len(ss)):
                                        for n in range(len(ss2)):
                                            if ss[k].wup_similarity(ss2[n])!=None:
                                                if buf<ss[k].wup_similarity(ss2[n]):
                                                    buf=ss[k].wup_similarity(ss2[n])
                        Sim=Sim*buf
        elif(t_h_t[i][1]!="CC")&(t_h_t[i][1]!="TO")&(t_h_t[i][1]!="IN")&(t_h_t[i][1]!="DT")&(t_h_t[i][1]!=".")&(t_h_t[i][1]!=",")&(t_h_t[i][1]!=":"):
            #print("ooooooooo")
            if h_t[i] not in t_t:
                buf=0
                ss=wordnet.synsets(h_t[i],pos=wordnet.ADJ)
                if wordnet.synsets(h_t[i],pos=wordnet.ADV)!=[]:
                    ss=ss+wordnet.synsets(h_t[i],pos=wordnet.ADV)
                for j in range(len(t_t)):
                    if Match==True:
                        break
                    if(t_t_t[j][1]!="CC")&(t_t_t[j][1]!="DT")&(t_t_t[j][1]!="TO")&(t_t_t[j][1]!=".")&(t_t_t[j][1]!=",")&(t_t_t[j][1]!=":")&(t_t_t[j][1]!="IN")&(t_t_t[j][1]!="NN")&(t_t_t[j][1]!="NNS")&(t_t_t[j][1]!="NNP")&(t_t_t[j][1]!="NNPS")&(t_t_t[j][1]!="VB")&(t_t_t[j][1]!="VBD")&(t_t_t[j][1]!="VBG")&(t_t_t[j][1]!="VBN")&(t_t_t[j][1]!="VBP")&(t_t_t[j][1]!="VBZ"):
                        for k in range(len(ss)):
                            if Match==True:
                                break
                            if t_t[j] in [str(lemma.name()) for lemma in ss[k].lemmas()]:
                                Match=True
                                break
                            else:
                                for n in range(len(ss[k].hyponyms())):
                                    if t_t[j] in [str(lemma.name()) for lemma in ss[k].hyponyms()[n].lemmas()]:
                                        Match=True
                                        break
                if Match==False:
                    for j in range(len(t_t)):
                        if(t_t_t[j][1]!="CC")&(t_t_t[j][1]!="DT")&(t_t_t[j][1]!="TO")&(t_t_t[j][1]!=".")&(t_t_t[j][1]!=",")&(t_t_t[j][1]!=":")&(t_t_t[j][1]!="IN"):#&(t_t_t[j][1]!="NN")&(t_t_t[j][1]!="NNS")&(t_t_t[j][1]!="NNP")&(t_t_t[j][1]!="NNPS")&(t_t_t[j][1]!="VB")&(t_t_t[j][1]!="VBD")&(t_t_t[j][1]!="VBG")&(t_t_t[j][1]!="VBN")&(t_t_t[j][1]!="VBP")&(t_t_t[j][1]!="VBZ"):
                            for k in range(len(ss)):
                                if Match==True:
                                    break
                                for n in range(len(ss[k].lemmas())):
                                    if t_t[j] in [str(lemma.name()) for lemma in ss[k].lemmas()[n].antonyms()]:
                                        Match=True
                                        if flag==True:
                                            flag=False
                                        else:
                                            flag=True
                                        break
                    if Match==False:
                        for j in range(len(t_t)):
                            if(t_t_t[j][1]!="CC")&(t_t_t[j][1]!="DT")&(t_t_t[j][1]!="TO")&(t_t_t[j][1]!=".")&(t_t_t[j][1]!=",")&(t_t_t[j][1]!=":")&(t_t_t[j][1]!="IN")&(t_t_t[j][1]!="NN")&(t_t_t[j][1]!="NNS")&(t_t_t[j][1]!="NNP")&(t_t_t[j][1]!="NNPS")&(t_t_t[j][1]!="VB")&(t_t_t[j][1]!="VBD")&(t_t_t[j][1]!="VBG")&(t_t_t[j][1]!="VBN")&(t_t_t[j][1]!="VBP")&(t_t_t[j][1]!="VBZ"):
                                ss2=wordnet.synsets(t_t[j],pos=wordnet.ADJ)
                                if wordnet.synsets(t_t[j],pos=wordnet.ADV)!=[]:
                                    ss2=ss2+wordnet.synsets(t_t[j],pos=wordnet.ADV)
                                for k in range(len(ss)):
                                    for n in range(len(ss2)):
                                        if ss[k].wup_similarity(ss2[n])!=None:
                                            if buf<ss[k].wup_similarity(ss2[n]):
                                                buf=ss[k].wup_similarity(ss2[n])
                    Sim=Sim*buf
    if flag==False:
        Sim=0
    print(Sim)

    if(Sim>=Tres):
        print("Entailment!")
    else:
        print("Not Entailment!")
