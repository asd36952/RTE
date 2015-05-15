from xml.etree.ElementTree import parse
import os
import nltk
import math
from nltk.corpus import wordnet
from nltk.tag.stanford import POSTagger
java_path ="C:\\Program Files\\Java\\jdk1.8.0_11\\bin\\java.exe"
st=POSTagger('C:\\Users\\SeongWooLim\\Desktop\\RTE\\stanford-postagger\\models\\english-bidirectional-distsim.tagger','C:\\Users\\SeongWooLim\\Desktop\\RTE\\stanford-postagger\\stanford-postagger.jar',encoding='UTF-8')
os.environ['JAVAHOME'] = java_path
print("Please Input RTE Set Number:")
key=input()
if key=="1":
    tree = parse("C:\\Users\\SeongWooLim\\Desktop\\RTE\\dev\\dev.xml")
elif key=="2":
    tree = parse("C:\\Users\\SeongWooLim\\Desktop\\RTE\\dev2\\dev.xml")
elif key=="3":
    tree = parse("C:\\Users\\SeongWooLim\\Desktop\\RTE\\dev3\\dev.xml")
root = tree.getroot()
v_t=[]
s_t=0
n_t=0
v_f=[]
s_f=0
n_f=0
for m in root.findall("pair"):
    h=m.findtext("h").casefold()
    h_t=nltk.word_tokenize(h)
    #t_h_t=nltk.pos_tag(h_t)
    t_h_t=st.tag(h_t)[0]
    t=m.findtext("t").casefold()
    t_t=nltk.word_tokenize(t)
    #t_t_t=nltk.pos_tag(t_t)
    t_t_t=st.tag(t_t)[0]
    Sim=1
    t_flag=True
    h_flag=True
    flag=True
#########################
#Negative word processig#
#########################
    for i in range(len(t_t)):
        t_t_t[i]=list(t_t_t[i])
        t_t_t[i].append("")
    for i in range(len(t_t)):
        if (t_t[i]=="never"): 
            if t_flag==True:
                t_flag=False
            else:
                t_flag=True
        elif (t_t[i]=="n't")|(t_t[i]=="not"):
            for j in range(len(t_t)-i-1):
                if(t_t_t[i+j][1] in ["VB","VBD","VBG","VBN","VBP","VBZ"]):
                    t_t_t[i+j][2]="~"
        elif(t_t[i]=="no"):
            for j in range(len(t_t)-i-1):
                if(t_t_t[i+j][1] in ["NN","NNS","NNP","NNPS"]):
                    t_t_t[i+j][2]="~"
    for i in range(len(h_t)):
        t_h_t[i]=list(t_h_t[i])
        t_h_t[i].append("")
    for i in range(len(h_t)):
        ss=None
        ss2=None
        Match=False
        if (h_t[i]=="never"): 
            if h_flag==True:
                h_flag=False
            else:
                h_flag=True
        if (h_t[i]=="n't")|(h_t[i]=="not"):
            for j in range(len(h_t)-i-1):
                if(t_h_t[i+j][1] in ["VB","VBD","VBG","VBN","VBP","VBZ"]):
                    t_h_t[i+1][2]="~"
        elif(h_t[i]=="no"):
            for j in range(len(h_t)-i-1):
                if(t_h_t[i+j][1] in ["NN","NNS","NNP","NNPS"]):
                    t_h_t[i+j][2]="~"
######################
#End of Preprocessing#
######################

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
                            if(t_h_t[i][2]==t_t_t[j][2]):
                                for lemma in ss[k].lemmas():
                                    if (len(wordnet.synsets(t_t[j]))!=0):
                                        if(len(set(wordnet.synsets(t_t[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                            Match=True
                                            break
                                for n in range(len(ss[k].hyponyms())):
                                    for lemma in ss[k].hyponyms()[n].lemmas():
                                        if (len(wordnet.synsets(t_t[j]))!=0):
                                            if(len(set(wordnet.synsets(t_t[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                Match=True
                                                break
                            else:
                                for lemma in ss[k].lemmas():
                                    if (len(wordnet.synsets(t_t[j]))!=0):
                                        if(len(set(wordnet.synsets(t_t[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                            Match=True
                                            if flag==True:
                                                flag=False
                                            else:
                                                flag=True
                                            break
                                else:
                                    for n in range(len(ss[k].hyponyms())):
                                        for lemma in ss[k].hyponyms()[n].lemmas():
                                            if (len(wordnet.synsets(t_t[j]))!=0):
                                                if(len(set(wordnet.synsets(t_t[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                    Match=True
                                                    if flag==True:
                                                        flag=False
                                                    else:
                                                        flag=True
                                                    break
                if Match==False:
                    #print(h_t[i])
                    for j in range(len(t_t)):
                        if(t_t_t[j][1]=="NN")|(t_t_t[j][1]=="NNS")|(t_t_t[j][1]=="NNP")|(t_t_t[j][1]=="NNPS"):
                            for k in range(len(ss)):
                                if Match==True:
                                    break
                                for n in range(len(ss[k].lemmas())):
                                    for lemma in ss[k].lemmas()[n].antonyms():
                                        if (len(wordnet.synsets(t_t[j]))!=0):
                                            if(len(set(wordnet.synsets(t_t[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                Match=True
                                                if(t_h_t[i][2]==t_t_t[j][2]):
                                                    if flag==True:
                                                        flag=False
                                                    else:
                                                        flag=True
                                                    break
                if Match==False:
                    buf=0
                    for j in range(len(t_t)):
                        if(t_t_t[j][1]!="DT")&(t_t_t[j][1]!="TO")&(t_t_t[j][1]!=".")&(t_t_t[j][1]!=",")&(t_t_t[j][1]!=":")&(t_t_t[j][1]!="POS")&(t_t_t[j][1]!="IN"):
                            ss2=wordnet.synsets(t_t[j],pos=wordnet.NOUN)
                            for k in range(len(ss)):
                                for n in range(len(ss2)):
                                    if ss[k].wup_similarity(ss2[n])!=None:
                                        if buf<ss[k].wup_similarity(ss2[n]):
                                            buf=ss[k].wup_similarity(ss2[n])
                                            #print(h_t[i])
                                            #print(t_t[j])
                                            #print(buf)
                        #print(buf)
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
                            if Match==True:
                                break
                            if(t_h_t[i][2]==t_t_t[j][2]):
                                for lemma in ss[k].lemmas():
                                    if (len(wordnet.synsets(t_t[j]))!=0):
                                        if(len(set(wordnet.synsets(t_t[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                            Match=True
                                            if (((t_h_t[i][1]=="VBN")&(t_t_t[j][1]!="VBN"))|((t_h_t[i][1]!="VBN")&(t_t_t[j][1]=="VBN"))):  #This statement means case, "T : I give a book to giyoung, H : I was given book from giyoung"
                                                if flag==True:
                                                    flag=False
                                                else:
                                                    flag=True
                                            break
                                for n in range(len(ss[k].hyponyms())):
                                    for lemma in ss[k].hyponyms()[n].lemmas():
                                        if (len(wordnet.synsets(t_t[j]))!=0):
                                            if(len(set(wordnet.synsets(t_t[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                Match=True
                                                if (((t_h_t[i][1]=="VBN")&(t_t_t[j][1]!="VBN"))|((t_h_t[i][1]!="VBN")&(t_t_t[j][1]=="VBN"))):
                                                    if flag==True:
                                                        flag=False
                                                    else:
                                                        flag=True
                                                break
                            else:
                                for lemma in ss[k].lemmas():
                                    if (len(wordnet.synsets(t_t[j]))!=0):
                                        if(len(set(wordnet.synsets(t_t[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                            Match=True
                                            if (not(((t_h_t[i][1]=="VBN")&(t_t_t[j][1]!="VBN"))|((t_h_t[i][1]!="VBN")&(t_t_t[j][1]=="VBN")))):
                                                if flag==True:
                                                    flag=False
                                                else:
                                                    flag=True
                                            break
                                for n in range(len(ss[k].hyponyms())):
                                    for n in range(len(ss[k].hyponyms())):
                                        for lemma in ss[k].hyponyms()[n].lemmas():
                                            Match=True
                                            if (not(((t_h_t[i][1]=="VBN")&(t_t_t[j][1]!="VBN"))|((t_h_t[i][1]!="VBN")&(t_t_t[j][1]=="VBN")))):
                                                if flag==True:
                                                    flag=False
                                                else:
                                                    flag=True
                                            break
                if Match==False:
                    for j in range(len(t_t)):
                        if Match==True:
                            break
                        if(t_t_t[j][1]=="VB")|(t_t_t[j][1]=="VBD")|(t_t_t[j][1]=="VBG")|(t_t_t[j][1]=="VBN")|(t_t_t[j][1]=="VBP")|(t_t_t[j][1]=="VBZ"):
                            for k in range(len(ss)):
                                if Match==True:
                                    break
                                if(t_h_t[i][2]==t_t_t[j][2]):
                                    for n in range(len(ss[k].lemmas())):
                                        for lemma in ss[k].lemmas()[n].antonyms():
                                            if (len(wordnet.synsets(t_t[j]))!=0):
                                                if(len(set(wordnet.synsets(t_t[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                    Match=True
                                                    if (not(((t_h_t[i][1]=="VBN")&(t_t_t[j][1]!="VBN"))|((t_h_t[i][1]!="VBN")&(t_t_t[j][1]=="VBN")))):
                                                        if flag==True:
                                                            flag=False
                                                        else:
                                                            flag=True
                                                    break
                                else:
                                    for n in range(len(ss[k].lemmas())):
                                        for lemma in ss[k].lemmas()[n].antonyms():
                                            if (len(wordnet.synsets(t_t[j]))!=0):
                                                if(len(set(wordnet.synsets(t_t[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                    Match=True
                                                    if (((t_h_t[i][1]=="VBN")&(t_t_t[j][1]!="VBN"))|((t_h_t[i][1]!="VBN")&(t_t_t[j][1]=="VBN"))):
                                                        if flag==True:
                                                            flag=False
                                                        else:
                                                            flag=True
                                                    break
                if Match==False:
                    #print(h_t[i])
                    buf=0
                    for j in range(len(t_t)):
                        if(t_t_t[j][1]!="CC")&(t_t_t[j][1]!="DT")&(t_t_t[j][1]!="TO")&(t_t_t[j][1]!=".")&(t_t_t[j][1]!=",")&(t_t_t[j][1]!=":")&(t_t_t[j][1]!="POS")&(t_t_t[j][1]!="IN"):
                            #print(t_t_t[j])
                            ss2=wordnet.synsets(t_t[j],pos=wordnet.VERB)
                            for k in range(len(ss)):
                                    for n in range(len(ss2)):
                                        #print(h_t[i])
                                        #print(t_t[j])
                                        #print(ss[k].wup_similarity(ss2[n]))
                                        if ss[k].wup_similarity(ss2[n])!=None:
                                            if buf<ss[k].wup_similarity(ss2[n]):
                                                buf=ss[k].wup_similarity(ss2[n])
                                                #print(h_t[i])
                                                #print(t_t[j])
                                                #print(buf)
                    Sim=Sim*buf
        elif(t_h_t[i][1]!="CC")&(t_h_t[i][1]!="TO")&(t_h_t[i][1]!="IN")&(t_h_t[i][1]!="DT")&(t_h_t[i][1]!=".")&(t_h_t[i][1]!=",")&(t_h_t[i][1]!=":")&(t_h_t[i][1]!="POS"):
            #print("ooooooooo")
            if h_t[i] not in t_t:
                buf=0
                ss=wordnet.synsets(h_t[i],pos=wordnet.ADJ)
                if wordnet.synsets(h_t[i],pos=wordnet.ADV)!=[]:
                    ss=ss+wordnet.synsets(h_t[i],pos=wordnet.ADV)
                for j in range(len(t_t)):
                    if Match==True:
                        break
                    if(t_t_t[j][1]!="CC")&(t_t_t[j][1]!="DT")&(t_t_t[j][1]!="TO")&(t_t_t[j][1]!=".")&(t_t_t[j][1]!=",")&(t_t_t[j][1]!=":")&(t_t_t[j][1]!="POS")&(t_t_t[j][1]!="IN")&(t_t_t[j][1]!="NN")&(t_t_t[j][1]!="NNS")&(t_t_t[j][1]!="NNP")&(t_t_t[j][1]!="NNPS")&(t_t_t[j][1]!="VB")&(t_t_t[j][1]!="VBD")&(t_t_t[j][1]!="VBG")&(t_t_t[j][1]!="VBN")&(t_t_t[j][1]!="VBP")&(t_t_t[j][1]!="VBZ"):
                        for k in range(len(ss)):
                            if Match==True:
                                break
                            if(t_h_t[i][2]==t_t_t[j][2]):
                                for lemma in ss[k].lemmas():
                                    if (len(wordnet.synsets(t_t[j]))!=0):
                                        if(len(set(wordnet.synsets(t_t[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                            Match=True
                                            break
                                for n in range(len(ss[k].hyponyms())):
                                    for lemma in ss[k].hyponyms()[n].lemmas():
                                        if (len(wordnet.synsets(t_t[j]))!=0):
                                            if(len(set(wordnet.synsets(t_t[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                Match=True
                                                break
                            else:
                                for lemma in ss[k].lemmas():
                                    if (len(wordnet.synsets(t_t[j]))!=0):
                                        if(len(set(wordnet.synsets(t_t[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                            Match=True
                                            if flag==True:
                                                flag=False
                                            else:
                                                flag=True
                                            break
                                for n in range(len(ss[k].hyponyms())):
                                    for lemma in ss[k].hyponyms()[n].lemmas():
                                        if (len(wordnet.synsets(t_t[j]))!=0):
                                            if(len(set(wordnet.synsets(t_t[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                Match=True
                                                if flag==True:
                                                    flag=False
                                                else:
                                                    flag=True
                                                break
                if Match==False:
                    for j in range(len(t_t)):
                        if(t_t_t[j][1]!="CC")&(t_t_t[j][1]!="DT")&(t_t_t[j][1]!="TO")&(t_t_t[j][1]!=".")&(t_t_t[j][1]!=",")&(t_t_t[j][1]!=":")&(t_t_t[j][1]!="POS")&(t_t_t[j][1]!="IN")&(t_t_t[j][1]!="NN")&(t_t_t[j][1]!="NNS")&(t_t_t[j][1]!="NNP")&(t_t_t[j][1]!="NNPS")&(t_t_t[j][1]!="VB")&(t_t_t[j][1]!="VBD")&(t_t_t[j][1]!="VBG")&(t_t_t[j][1]!="VBN")&(t_t_t[j][1]!="VBP")&(t_t_t[j][1]!="VBZ"):
                            for k in range(len(ss)):
                                if Match==True:
                                    break
                                for n in range(len(ss[k].lemmas())):
                                    for lemma in ss[k].lemmas()[n].antonyms():
                                            if (len(wordnet.synsets(t_t[j]))!=0):
                                                if(len(set(wordnet.synsets(t_t[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                    Match=True
                                                    if(t_h_t[i][2]==t_t_t[j][2]):
                                                        if flag==True:
                                                            flag=False
                                                        else:
                                                            flag=True
                                                    break
                if Match==False:
                    for j in range(len(t_t)):
                        if(t_t_t[j][1]!="CC")&(t_t_t[j][1]!="DT")&(t_t_t[j][1]!="TO")&(t_t_t[j][1]!=".")&(t_t_t[j][1]!=",")&(t_t_t[j][1]!=":")&(t_t_t[j][1]!="POS")&(t_t_t[j][1]!="IN"):#&(t_t_t[j][1]!="NN")&(t_t_t[j][1]!="NNS")&(t_t_t[j][1]!="NNP")&(t_t_t[j][1]!="NNPS")&(t_t_t[j][1]!="VB")&(t_t_t[j][1]!="VBD")&(t_t_t[j][1]!="VBG")&(t_t_t[j][1]!="VBN")&(t_t_t[j][1]!="VBP")&(t_t_t[j][1]!="VBZ"):
                            ss2=wordnet.synsets(t_t[j],pos=wordnet.ADJ)
                            if wordnet.synsets(t_t[j],pos=wordnet.ADV)!=[]:
                                ss2=ss2+wordnet.synsets(t_t[j],pos=wordnet.ADV)
                            for k in range(len(ss)):
                                for n in range(len(ss2)):
                                    if ss[k].wup_similarity(ss2[n])!=None:
                                        if buf<ss[k].wup_similarity(ss2[n]):
                                            buf=ss[k].wup_similarity(ss2[n])
                Sim=Sim*buf
    if ((t_flag==h_flag)&(flag==False))|((t_flag!=h_flag)&(flag==True)):
        Sim=0
    #print(t)
    #print(h)
    if key=="1":
        print(m.get("value"))
    elif (key=="2")|(key=="3"):
        print(m.get("entailment"))
    print(Sim)
    #test
    #print("stop:5")
    #if input()=="5":
    #    break
    if key=="1":
        if(m.get("value")=="TRUE"):
            v_t.append(Sim)
            n_t=n_t+1
        else:
            v_f.append(Sim)
            n_f=n_f+1
    elif (key=="2")|(key=="3"):
        if(m.get("entailment")=="YES"):
            v_t.append(Sim)
            n_t=n_t+1
        else:
            v_f.append(Sim)
            n_f=n_f+1
print("RTE"+key+" set")
print("Result:")
print(" Average of True:")
for i in v_t:
    s_t=s_t+i
a_t=s_t/n_t
print(a_t)
print(" Average of False:")
for i in v_f:
    s_f=s_f+i
a_f=s_f/n_f
print(a_f)
s_t=0
s_f=0
print(" Distribution of True:")
for i in v_t:
    s_t=s_t+(i*i)
d_t=(s_t/n_t)-(a_t*a_t)
print(d_t)
print(" Distribution of False:")
for i in v_f:
    s_f=s_f+(i*i)
d_f=(s_f/n_f)-(a_f*a_f)
print(d_f)
print(" Treshold:")
Tres=((math.sqrt(d_t)*a_f)+(math.sqrt(d_f)*a_t))/(math.sqrt(d_f)+math.sqrt(d_t))
print(Tres)
if key=="1":
    data=open('C:\\Users\\SeongWooLim\\Desktop\\RTE\\Treshold.txt','w')
elif key=="2":
    data=open('C:\\Users\\SeongWooLim\\Desktop\\RTE\\Treshold2.txt','w')
elif key=="3":
    data=open('C:\\Users\\SeongWooLim\\Desktop\\RTE\\Treshold3.txt','w')
data.write("%lf" %Tres)
data.close()
