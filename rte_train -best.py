from xml.etree.ElementTree import parse
import os
import nltk
import math
from nltk.corpus import wordnet
from nltk.tag.stanford import POSTagger

#############
#Change path#
#############
java_path ="C:\\Program Files\\Java\\jdk1.8.0_11\\bin\\java.exe"
st=POSTagger('C:\\Users\\SeongWooLim\\Desktop\\RTE\\stanford-postagger\\models\\english-bidirectional-distsim.tagger','C:\\Users\\SeongWooLim\\Desktop\\RTE\\stanford-postagger\\stanford-postagger.jar',encoding='UTF-8')
os.environ['JAVAHOME'] = java_path
print("Please Input RTE Set Number:")
key=input()
#############
#Change path#
#############
if key=="1":
    tree = parse("C:\\Users\\SeongWooLim\\Desktop\\RTE\\dev\\dev.xml")
elif key=="2":
    tree = parse("C:\\Users\\SeongWooLim\\Desktop\\RTE\\dev2\\dev.xml")
elif key=="3":
    tree = parse("C:\\Users\\SeongWooLim\\Desktop\\RTE\\dev3\\dev.xml")
root = tree.getroot()
true_similarity=[]
number_true=0
false_similarity=[]
number_false=0

for m in root.findall("pair"):
    hypothesis=m.findtext("h").casefold()
    tokenized_hypothesis=nltk.word_tokenize(hypothesis)
    #tagged_tokenized_hypothesis=nltk.pos_tag(tokenized_hypothesis)    #nltk tagger
    tagged_tokenized_hypothesis=st.tag(tokenized_hypothesis)[0]    #stanfordnlp tagger
    text=m.findtext("t").casefold()
    tokenized_text=nltk.word_tokenize(text)
    #tagged_tokenized_text=nltk.pos_tag(tokenized_text)    #nltk tagger
    tagged_tokenized_text=st.tag(tokenized_text)[0]    #stanfordnlp tagger
    Similarity=1
    text_flag=True
    hypothesis_flag=True
    flag=True
#########################
#Negative word processig#
#########################
    for i in range(len(tokenized_text)):
        tagged_tokenized_text[i]=list(tagged_tokenized_text[i])
        tagged_tokenized_text[i].append("")
    for i in range(len(tokenized_text)):
        if (tokenized_text[i]=="never"): 
            if text_flag==True:
                text_flag=False
            else:
                text_flag=True
        elif (tokenized_text[i]=="n't")|(tokenized_text[i]=="not"):
            for j in range(len(tokenized_text)-i-1):
                if(tagged_tokenized_text[i+j][1] in ["VB","VBD","VBG","VBN","VBP","VBZ"]):
                    tagged_tokenized_text[i+j][2]="~"
        elif(tokenized_text[i]=="no"):
            for j in range(len(tokenized_text)-i-1):
                if(tagged_tokenized_text[i+j][1] in ["NN","NNS","NNP","NNPS"]):
                    tagged_tokenized_text[i+j][2]="~"

###############################################################################

    for i in range(len(tokenized_hypothesis)):
        tagged_tokenized_hypothesis[i]=list(tagged_tokenized_hypothesis[i])
        tagged_tokenized_hypothesis[i].append("")
    for i in range(len(tokenized_hypothesis)):
        synonymSet_hypothesis=None
        synonymSet_text=None
        Match=False
        if (tokenized_hypothesis[i]=="never"): 
            if hypothesis_flag==True:
                hypothesis_flag=False
            else:
                hypothesis_flag=True
        if (tokenized_hypothesis[i]=="n't")|(tokenized_hypothesis[i]=="not"):
            for j in range(len(tokenized_hypothesis)-i-1):
                if(tagged_tokenized_hypothesis[i+j][1] in ["VB","VBD","VBG","VBN","VBP","VBZ"]):
                    tagged_tokenized_hypothesis[i+1][2]="~"
        elif(tokenized_hypothesis[i]=="no"):
            for j in range(len(tokenized_hypothesis)-i-1):
                if(tagged_tokenized_hypothesis[i+j][1] in ["NN","NNS","NNP","NNPS"]):
                    tagged_tokenized_hypothesis[i+j][2]="~"
######################
#End of Preprocessing#
######################
        #Noun case
        elif(tagged_tokenized_hypothesis[i][1]=="NN")|(tagged_tokenized_hypothesis[i][1]=="NNS")|(tagged_tokenized_hypothesis[i][1]=="NNP")|(tagged_tokenized_hypothesis[i][1]=="NNPS"):
            #there is not same word.
            if tokenized_hypothesis[i] not in tokenized_text: 
                synonymSet_hypothesis=wordnet.synsets(tokenized_hypothesis[i],pos=wordnet.NOUN)
                for j in range(len(tokenized_text)):
                    if(tagged_tokenized_text[j][1]=="NN")|(tagged_tokenized_text[j][1]=="NNS")|(tagged_tokenized_text[j][1]=="NNP")|(tagged_tokenized_text[j][1]=="NNPS"):
                        if Match==True:
                            break
                        for k in range(len(synonymSet_hypothesis)):
                            if Match==True:
                                break
                            if(tagged_tokenized_hypothesis[i][2]==tagged_tokenized_text[j][2]):
                                for lemma in synonymSet_hypothesis[k].lemmas():     #synonym
                                    if (len(wordnet.synsets(tokenized_text[j]))!=0):
                                        if(len(set(wordnet.synsets(tokenized_text[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                            Match=True
                                            break
                                for n in range(len(synonymSet_hypothesis[k].hyponyms())):       #hyponym
                                    for lemma in synonymSet_hypothesis[k].hyponyms()[n].lemmas():
                                        if (len(wordnet.synsets(tokenized_text[j]))!=0):
                                            if(len(set(wordnet.synsets(tokenized_text[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                Match=True
                                                break
                            else:   #negative
                                for lemma in synonymSet_hypothesis[k].lemmas():
                                    if (len(wordnet.synsets(tokenized_text[j]))!=0):
                                        if(len(set(wordnet.synsets(tokenized_text[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                            Match=True
                                            if flag==True:
                                                flag=False
                                            else:
                                                flag=True
                                            break
                                else:
                                    for n in range(len(synonymSet_hypothesis[k].hyponyms())):
                                        for lemma in synonymSet_hypothesis[k].hyponyms()[n].lemmas():
                                            if (len(wordnet.synsets(tokenized_text[j]))!=0):
                                                if(len(set(wordnet.synsets(tokenized_text[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                    Match=True
                                                    if flag==True:
                                                        flag=False
                                                    else:
                                                        flag=True
                                                    break
                if Match==False:
                    for j in range(len(tokenized_text)):
                        if(tagged_tokenized_text[j][1]=="NN")|(tagged_tokenized_text[j][1]=="NNS")|(tagged_tokenized_text[j][1]=="NNP")|(tagged_tokenized_text[j][1]=="NNPS"):
                            for k in range(len(synonymSet_hypothesis)):
                                if Match==True:
                                    break
                                for n in range(len(synonymSet_hypothesis[k].lemmas())):
                                    for lemma in synonymSet_hypothesis[k].lemmas()[n].antonyms():   #antonym
                                        if (len(wordnet.synsets(tokenized_text[j]))!=0):
                                            if(len(set(wordnet.synsets(tokenized_text[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                Match=True
                                                if(tagged_tokenized_hypothesis[i][2]==tagged_tokenized_text[j][2]):
                                                    if flag==True:
                                                        flag=False
                                                    else:
                                                        flag=True
                                                    break
                if Match==False:        #not matched
                    buf=0
                    for j in range(len(tokenized_text)):
                        if(tagged_tokenized_text[j][1]!="DT")&(tagged_tokenized_text[j][1]!="TO")&(tagged_tokenized_text[j][1]!=".")&(tagged_tokenized_text[j][1]!=",")&(tagged_tokenized_text[j][1]!=":")&(tagged_tokenized_text[j][1]!="POS")&(tagged_tokenized_text[j][1]!="IN"):
                            synonymSet_text=wordnet.synsets(tokenized_text[j],pos=wordnet.NOUN)
                            for k in range(len(synonymSet_hypothesis)):
                                for n in range(len(synonymSet_text)):
                                    if synonymSet_hypothesis[k].wup_similarity(synonymSet_text[n])!=None:
                                        if buf<synonymSet_hypothesis[k].wup_similarity(synonymSet_text[n]):
                                            buf=synonymSet_hypothesis[k].wup_similarity(synonymSet_text[n])
                    Similarity=Similarity*buf
        #verb case
        elif(tagged_tokenized_hypothesis[i][1]=="VB")|(tagged_tokenized_hypothesis[i][1]=="VBD")|(tagged_tokenized_hypothesis[i][1]=="VBG")|(tagged_tokenized_hypothesis[i][1]=="VBN")|(tagged_tokenized_hypothesis[i][1]=="VBP")|(tagged_tokenized_hypothesis[i][1]=="VBZ"):
            if tokenized_hypothesis[i] not in tokenized_text:
                synonymSet_hypothesis=wordnet.synsets(tokenized_hypothesis[i],pos=wordnet.VERB)
                for j in range(len(tokenized_text)):
                    if Match==True:
                        break
                    if(tagged_tokenized_text[j][1]=="VB")|(tagged_tokenized_text[j][1]=="VBD")|(tagged_tokenized_text[j][1]=="VBG")|(tagged_tokenized_text[j][1]=="VBN")|(tagged_tokenized_text[j][1]=="VBP")|(tagged_tokenized_text[j][1]=="VBZ"):
                        for k in range(len(synonymSet_hypothesis)):
                            if Match==True:
                                break
                            if(tagged_tokenized_hypothesis[i][2]==tagged_tokenized_text[j][2]):
                                for lemma in synonymSet_hypothesis[k].lemmas():
                                    if (len(wordnet.synsets(tokenized_text[j]))!=0):
                                        if(len(set(wordnet.synsets(tokenized_text[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                            Match=True
                                            if (((tagged_tokenized_hypothesis[i][1]=="VBN")&(tagged_tokenized_text[j][1]!="VBN"))|((tagged_tokenized_hypothesis[i][1]!="VBN")&(tagged_tokenized_text[j][1]=="VBN"))):  #This statement means case, "T : I give a book to giyoung, H : I was given book from giyoung"
                                                if flag==True:
                                                    flag=False
                                                else:
                                                    flag=True
                                            break
                                for n in range(len(synonymSet_hypothesis[k].hyponyms())):
                                    for lemma in synonymSet_hypothesis[k].hyponyms()[n].lemmas():
                                        if (len(wordnet.synsets(tokenized_text[j]))!=0):
                                            if(len(set(wordnet.synsets(tokenized_text[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                Match=True
                                                if (((tagged_tokenized_hypothesis[i][1]=="VBN")&(tagged_tokenized_text[j][1]!="VBN"))|((tagged_tokenized_hypothesis[i][1]!="VBN")&(tagged_tokenized_text[j][1]=="VBN"))):
                                                    if flag==True:
                                                        flag=False
                                                    else:
                                                        flag=True
                                                break
                            else:
                                for lemma in synonymSet_hypothesis[k].lemmas():
                                    if (len(wordnet.synsets(tokenized_text[j]))!=0):
                                        if(len(set(wordnet.synsets(tokenized_text[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                            Match=True
                                            if (not(((tagged_tokenized_hypothesis[i][1]=="VBN")&(tagged_tokenized_text[j][1]!="VBN"))|((tagged_tokenized_hypothesis[i][1]!="VBN")&(tagged_tokenized_text[j][1]=="VBN")))):
                                                if flag==True:
                                                    flag=False
                                                else:
                                                    flag=True
                                            break
                                for n in range(len(synonymSet_hypothesis[k].hyponyms())):
                                    for n in range(len(synonymSet_hypothesis[k].hyponyms())):
                                        for lemma in synonymSet_hypothesis[k].hyponyms()[n].lemmas():
                                            Match=True
                                            if (not(((tagged_tokenized_hypothesis[i][1]=="VBN")&(tagged_tokenized_text[j][1]!="VBN"))|((tagged_tokenized_hypothesis[i][1]!="VBN")&(tagged_tokenized_text[j][1]=="VBN")))):
                                                if flag==True:
                                                    flag=False
                                                else:
                                                    flag=True
                                            break
                if Match==False:
                    for j in range(len(tokenized_text)):
                        if Match==True:
                            break
                        if(tagged_tokenized_text[j][1]=="VB")|(tagged_tokenized_text[j][1]=="VBD")|(tagged_tokenized_text[j][1]=="VBG")|(tagged_tokenized_text[j][1]=="VBN")|(tagged_tokenized_text[j][1]=="VBP")|(tagged_tokenized_text[j][1]=="VBZ"):
                            for k in range(len(synonymSet_hypothesis)):
                                if Match==True:
                                    break
                                if(tagged_tokenized_hypothesis[i][2]==tagged_tokenized_text[j][2]):
                                    for n in range(len(synonymSet_hypothesis[k].lemmas())):
                                        for lemma in synonymSet_hypothesis[k].lemmas()[n].antonyms():
                                            if (len(wordnet.synsets(tokenized_text[j]))!=0):
                                                if(len(set(wordnet.synsets(tokenized_text[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                    Match=True
                                                    if (not(((tagged_tokenized_hypothesis[i][1]=="VBN")&(tagged_tokenized_text[j][1]!="VBN"))|((tagged_tokenized_hypothesis[i][1]!="VBN")&(tagged_tokenized_text[j][1]=="VBN")))):
                                                        if flag==True:
                                                            flag=False
                                                        else:
                                                            flag=True
                                                    break
                                else:
                                    for n in range(len(synonymSet_hypothesis[k].lemmas())):
                                        for lemma in synonymSet_hypothesis[k].lemmas()[n].antonyms():
                                            if (len(wordnet.synsets(tokenized_text[j]))!=0):
                                                if(len(set(wordnet.synsets(tokenized_text[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                    Match=True
                                                    if (((tagged_tokenized_hypothesis[i][1]=="VBN")&(tagged_tokenized_text[j][1]!="VBN"))|((tagged_tokenized_hypothesis[i][1]!="VBN")&(tagged_tokenized_text[j][1]=="VBN"))):
                                                        if flag==True:
                                                            flag=False
                                                        else:
                                                            flag=True
                                                    break
                if Match==False:
                    #print(h_t[i])
                    buf=0
                    for j in range(len(tokenized_text)):
                        if(tagged_tokenized_text[j][1]!="CC")&(tagged_tokenized_text[j][1]!="DT")&(tagged_tokenized_text[j][1]!="TO")&(tagged_tokenized_text[j][1]!=".")&(tagged_tokenized_text[j][1]!=",")&(tagged_tokenized_text[j][1]!=":")&(tagged_tokenized_text[j][1]!="POS")&(tagged_tokenized_text[j][1]!="IN"):
                            #print(t_t_t[j])
                            synonymSet_text=wordnet.synsets(tokenized_text[j],pos=wordnet.VERB)
                            for k in range(len(synonymSet_hypothesis)):
                                    for n in range(len(synonymSet_text)):
                                        #print(h_t[i])
                                        #print(t_t[j])
                                        #print(ss[k].wup_similarity(ss2[n]))
                                        if synonymSet_hypothesis[k].wup_similarity(synonymSet_text[n])!=None:
                                            if buf<synonymSet_hypothesis[k].wup_similarity(synonymSet_text[n]):
                                                buf=synonymSet_hypothesis[k].wup_similarity(synonymSet_text[n])
                                                #print(h_t[i])
                                                #print(t_t[j])
                                                #print(buf)
                    Similarity=Similarity*buf
        elif(tagged_tokenized_hypothesis[i][1]!="CC")&(tagged_tokenized_hypothesis[i][1]!="TO")&(tagged_tokenized_hypothesis[i][1]!="IN")&(tagged_tokenized_hypothesis[i][1]!="DT")&(tagged_tokenized_hypothesis[i][1]!=".")&(tagged_tokenized_hypothesis[i][1]!=",")&(tagged_tokenized_hypothesis[i][1]!=":")&(tagged_tokenized_hypothesis[i][1]!="POS"):
            #print("ooooooooo")
            if tokenized_hypothesis[i] not in tokenized_text:
                buf=0
                synonymSet_hypothesis=wordnet.synsets(tokenized_hypothesis[i],pos=wordnet.ADJ)
                if wordnet.synsets(tokenized_hypothesis[i],pos=wordnet.ADV)!=[]:
                    synonymSet_hypothesis=synonymSet_hypothesis+wordnet.synsets(tokenized_hypothesis[i],pos=wordnet.ADV)
                for j in range(len(tokenized_text)):
                    if Match==True:
                        break
                    if(tagged_tokenized_text[j][1]!="CC")&(tagged_tokenized_text[j][1]!="DT")&(tagged_tokenized_text[j][1]!="TO")&(tagged_tokenized_text[j][1]!=".")&(tagged_tokenized_text[j][1]!=",")&(tagged_tokenized_text[j][1]!=":")&(tagged_tokenized_text[j][1]!="POS")&(tagged_tokenized_text[j][1]!="IN")&(tagged_tokenized_text[j][1]!="NN")&(tagged_tokenized_text[j][1]!="NNS")&(tagged_tokenized_text[j][1]!="NNP")&(tagged_tokenized_text[j][1]!="NNPS")&(tagged_tokenized_text[j][1]!="VB")&(tagged_tokenized_text[j][1]!="VBD")&(tagged_tokenized_text[j][1]!="VBG")&(tagged_tokenized_text[j][1]!="VBN")&(tagged_tokenized_text[j][1]!="VBP")&(tagged_tokenized_text[j][1]!="VBZ"):
                        for k in range(len(synonymSet_hypothesis)):
                            if Match==True:
                                break
                            if(tagged_tokenized_hypothesis[i][2]==tagged_tokenized_text[j][2]):
                                for lemma in synonymSet_hypothesis[k].lemmas():
                                    if (len(wordnet.synsets(tokenized_text[j]))!=0):
                                        if(len(set(wordnet.synsets(tokenized_text[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                            Match=True
                                            break
                                for n in range(len(synonymSet_hypothesis[k].hyponyms())):
                                    for lemma in synonymSet_hypothesis[k].hyponyms()[n].lemmas():
                                        if (len(wordnet.synsets(tokenized_text[j]))!=0):
                                            if(len(set(wordnet.synsets(tokenized_text[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                Match=True
                                                break
                            else:
                                for lemma in synonymSet_hypothesis[k].lemmas():
                                    if (len(wordnet.synsets(tokenized_text[j]))!=0):
                                        if(len(set(wordnet.synsets(tokenized_text[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                            Match=True
                                            if flag==True:
                                                flag=False
                                            else:
                                                flag=True
                                            break
                                for n in range(len(synonymSet_hypothesis[k].hyponyms())):
                                    for lemma in synonymSet_hypothesis[k].hyponyms()[n].lemmas():
                                        if (len(wordnet.synsets(tokenized_text[j]))!=0):
                                            if(len(set(wordnet.synsets(tokenized_text[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                Match=True
                                                if flag==True:
                                                    flag=False
                                                else:
                                                    flag=True
                                                break
                if Match==False:
                    for j in range(len(tokenized_text)):
                        if(tagged_tokenized_text[j][1]!="CC")&(tagged_tokenized_text[j][1]!="DT")&(tagged_tokenized_text[j][1]!="TO")&(tagged_tokenized_text[j][1]!=".")&(tagged_tokenized_text[j][1]!=",")&(tagged_tokenized_text[j][1]!=":")&(tagged_tokenized_text[j][1]!="POS")&(tagged_tokenized_text[j][1]!="IN")&(tagged_tokenized_text[j][1]!="NN")&(tagged_tokenized_text[j][1]!="NNS")&(tagged_tokenized_text[j][1]!="NNP")&(tagged_tokenized_text[j][1]!="NNPS")&(tagged_tokenized_text[j][1]!="VB")&(tagged_tokenized_text[j][1]!="VBD")&(tagged_tokenized_text[j][1]!="VBG")&(tagged_tokenized_text[j][1]!="VBN")&(tagged_tokenized_text[j][1]!="VBP")&(tagged_tokenized_text[j][1]!="VBZ"):
                            for k in range(len(synonymSet_hypothesis)):
                                if Match==True:
                                    break
                                for n in range(len(synonymSet_hypothesis[k].lemmas())):
                                    for lemma in synonymSet_hypothesis[k].lemmas()[n].antonyms():
                                            if (len(wordnet.synsets(tokenized_text[j]))!=0):
                                                if(len(set(wordnet.synsets(tokenized_text[j])[0].lemma_names()).intersection(lemma.name()))>0):
                                                    Match=True
                                                    if(tagged_tokenized_hypothesis[i][2]==tagged_tokenized_text[j][2]):
                                                        if flag==True:
                                                            flag=False
                                                        else:
                                                            flag=True
                                                    break
                if Match==False:
                    for j in range(len(tokenized_text)):
                        if(tagged_tokenized_text[j][1]!="CC")&(tagged_tokenized_text[j][1]!="DT")&(tagged_tokenized_text[j][1]!="TO")&(tagged_tokenized_text[j][1]!=".")&(tagged_tokenized_text[j][1]!=",")&(tagged_tokenized_text[j][1]!=":")&(tagged_tokenized_text[j][1]!="POS")&(tagged_tokenized_text[j][1]!="IN"):#&(t_t_t[j][1]!="NN")&(t_t_t[j][1]!="NNS")&(t_t_t[j][1]!="NNP")&(t_t_t[j][1]!="NNPS")&(t_t_t[j][1]!="VB")&(t_t_t[j][1]!="VBD")&(t_t_t[j][1]!="VBG")&(t_t_t[j][1]!="VBN")&(t_t_t[j][1]!="VBP")&(t_t_t[j][1]!="VBZ"):
                            synonymSet_text=wordnet.synsets(tokenized_text[j],pos=wordnet.ADJ)
                            if wordnet.synsets(tokenized_text[j],pos=wordnet.ADV)!=[]:
                                synonymSet_text=synonymSet_text+wordnet.synsets(tokenized_text[j],pos=wordnet.ADV)
                            for k in range(len(synonymSet_hypothesis)):
                                for n in range(len(synonymSet_text)):
                                    if synonymSet_hypothesis[k].wup_similarity(synonymSet_text[n])!=None:
                                        if buf<synonymSet_hypothesis[k].wup_similarity(synonymSet_text[n]):
                                            buf=synonymSet_hypothesis[k].wup_similarity(synonymSet_text[n])
                Similarity=Similarity*buf
    if ((text_flag==hypothesis_flag)&(flag==False))|((text_flag!=hypothesis_flag)&(flag==True)):
        Similarity=0
    #print(t)
    #print(h)
    if key=="1":
        print(m.get("value"))
    elif (key=="2")|(key=="3"):
        print(m.get("entailment"))
    print(Similarity)
    #test
    #print("stop:5")
    #if input()=="5":
    #    break
    if key=="1":
        if(m.get("value")=="TRUE"):
            true_similarity.append(Similarity)
            number_true=number_true+1
        else:
            false_similarity.append(Similarity)
            number_false=number_false+1
    elif (key=="2")|(key=="3"):
        if(m.get("entailment")=="YES"):
            true_similarity.append(Similarity)
            number_true=number_true+1
        else:
            false_similarity.append(Similarity)
            number_false=number_false+1
print("RTE"+key+" set")
print("Result:")
################################
#Normalization and set treshold#
################################
print(" Average of True:")
sum_true=0
sum_false=0
for i in true_similarity:
    sum_true=sum_true+i
average_true=sum_true/number_true
print(average_true)
print(" Average of False:")
for i in false_similarity:
    sum_false=sum_false+i
average_false=sum_false/number_false
print(average_false)
squre_sum_ture=0
squre_sum_false=0
print(" Distribution of True:")
for i in true_similarity:
    squre_sum_ture=squre_sum_ture+(i*i)
distribution_true=(squre_sum_ture/number_true)-(average_true*average_true)
print(distribution_true)
print(" Distribution of False:")
for i in false_similarity:
    squre_sum_false=squre_sum_false+(i*i)
distribution_false=(squre_sum_false/number_false)-(average_false*average_false)
print(distribution_false)
print(" Treshold:")
Tres=((math.sqrt(distribution_true)*average_false)+(math.sqrt(distribution_false)*average_true))/(math.sqrt(distribution_false)+math.sqrt(distribution_true))
print(Tres)
if key=="1":
    data=open('C:\\Users\\SeongWooLim\\Desktop\\RTE\\Treshold.txt','w')
elif key=="2":
    data=open('C:\\Users\\SeongWooLim\\Desktop\\RTE\\Treshold2.txt','w')
elif key=="3":
    data=open('C:\\Users\\SeongWooLim\\Desktop\\RTE\\Treshold3.txt','w')
data.write("%lf" %Tres)
data.close()
