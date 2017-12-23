import string


def common_terms(str1, str2):
    """Return the number of words common in str1 and str2"""
    exclude = set(string.punctuation)
    nopunct_str1 = ''.join(ch for ch in str1 if ch not in exclude)
    nopunct_str2 = ''.join(ch for ch in str2 if ch not in exclude)
    nopunct_l_str1=nopunct_str1.lower()
    nopunct_l_str2=nopunct_str2.lower()
    final_str1=nopunct_l_str1.split(" ")
    final_str2=nopunct_l_str2.split(" ")
    toret=0
    for i in final_str1:
        for j in final_str2:
            temp=0
            lim=min(len(i),len(j))
            for u in range(lim-1):
                if i[u]==j[u] and i[u+1]==j[u+1]:
                    temp=temp+1
            temp=temp+1
            if lim<=5 and lim>3:    #if the min. number of characters in the two words is between 3 and 5, if 40% of the initial characters match, we can safely say that both the words refer to the same thing
                if temp>0.4*lim:
                    toret=toret+1
            elif lim>5 and lim<=10:
                if temp>=0.5*lim:
                    toret=toret+1
            elif lim>10:
                if temp>=0.8*lim:
                    toret=toret+1
            else:
                continue
    return toret


class featurevec(object):
    def __init__(self, query, idx, quest, ans, quest_pop, ans_life, upvote, downvote):
        """Returns the final feature vector for the tuple of query, question and answer
        The following features will be returned in the feature vector in the same order as listed below:
        1. Query-Question overlap
        2. Query-Answer overlap
        3. Question-Answer overlap
        4. Query-Question length ratio
        5. Query-Answer length ratio
        6. Question-Answer length ratio
        7. Query length
        8. Question length
        9. Answer length
        10. Answer lifetime in years
        11. Question popularity
        12. Upvotes for the answer
        13. Downvotes for the answer
        """
        self.features=[]
        self.queryindex=idx
        query_quest_com=common_terms(query, quest)
        query_ans_com=common_terms(query, ans)
        quest_ans_com=common_terms(quest, ans)
        self.features=[query_quest_com, query_ans_com, quest_ans_com]
        query_len=len(query.split(" "))
        quest_len=len(quest.split(" "))
        ans_len=len(ans.split(" "))
        self.features.append(float(query_len)/quest_len)
        self.features.append(float(query_len)/ans_len)
        self.features.append(float(quest_len)/ans_len)
        self.features.append(query_len)
        self.features.append(quest_len)
        self.features.append(ans_len)
        self.features.append(ans_life)
        self.features.append(quest_pop)
        self.features.append(upvote)
        self.features.append(downvote)


def decide_preference(featurevec1, featurevec2):
    """This function returns a list of the two features passed as the arguments with the first function referring to the more feature vector with higher preference
    Note : Both the feature vectors passed as arguments should have the same queries
    """
    s=1
    p1=featurevec1.features[11]/(featurevec1.features[11]+featurevec1.features[12]+s)
    p2=featurevec2.features[11]/(featurevec2.features[11]+featurevec2.features[12]+s)
    if p1>p2:
        toret=[featurevec1, featurevec2]
    else:
        toret=[featurevec2, featurevec1]
    return toret


def process_doc(str):
    """This function processes the text document containing the dataset of the queries, questions and answers and returns a list of all the feature vectors
    available in the dataset"""
    dataset=open(str)
    data=dataset.read()
    linelist=data.split("\n")
    linelist=filter(None,linelist)
    wordslist1=[x.split(" ") for x in linelist]
    for v in range(len(wordslist1)):
        wordslist1[v]=filter(None, wordslist1[v])
    wordslist1=filter(None,wordslist1)
    wordslist=[w for w in wordslist1 if len(w)>1]
    #print wordslist[0:50]
    featurelist=[]
    j=0
    #print "Checkpoint 1"
    for i in range(len(wordslist)):
        if wordslist[i][0]=='Query:':
            idx_cur_query=wordslist[i][1]
            currentQuery=wordslist[i][2:len(wordslist[i])]
            currentQuery=' '.join(currentQuery)
            #print currentQuery
            i=i+1
            if wordslist[i][0]=='Question:': 
                currentQuestion=wordslist[i][1:len(wordslist[i])]       #currentQuestion here is a list of individaul words but it should be a string, so join it
                currentQuestion=' '.join(currentQuestion)
                #print currentQuestion
                i=i+1
                if wordslist[i][0]=='Popularity:': 
                    Popularity=int(wordslist[i][1])
                    #print Popularity
                    i=i+1
                    if wordslist[i][0]=='Answer:': 
                        #print "Checkpoint 2"
                        j=i
                        while wordslist[j][0]!="Lifetime:" and wordslist[j][0]!="Query:":
                            j=j+1
                            if j==len(wordslist):
                                break
                        if j<len(wordslist):
                            if wordslist[j][0]=="Lifetime:":
                                currentAnswer='\n'.join([' '.join(wordslist[a]) for a in range(i,j)])                #wordslist[i:j]
                                #print currentAnswer
                                i=j
                                ansLife=wordslist[i][1]
                                #print ansLife
                                if ansLife.isdigit():
                                    ansLife=int(ansLife)
                                else:
                                    continue
                                i=i+1
                                if wordslist[i][0]=='upVotes:':
                                    upvote=int(wordslist[i][1])
                                    #print upvote
                                    i=i+1
                                    if wordslist[i][0]=='downVotes:':
                                        downvote=int(wordslist[i][1])
                                        #print downvote
                                        featurelist.append(featurevec(currentQuery, idx_cur_query, currentQuestion, currentAnswer, Popularity, ansLife, upvote, downvote))
                                        #print featurelist[len(featurelist)-1]
        else:
            continue
    return featurelist


def segregate_features(feature_list):
    """ This function segregates features corresponding to the same query given a list of extracted features from a document.
    The list returned is a list of lists containing features corresponding to the same query
    """
    processed=[]       # This list holds the query indices which have been segregated from the feature_list argument
    segregated_feat=[]    # List to be returned
    count=0            # Count of features segregated

    for feature in feature_list:
        if feature.queryindex not in processed:
            cur_idx=feature.queryindex
            cur_query_list=[]
            for feature in feature_list:
                if feature.queryindex==cur_idx:
                    cur_query_list.append(feature)
            segregated_feat.append(cur_query_list)
            processed.append(cur_idx)
    return segregated_feat


def create_S(segregatedFeatures):
    """This function will create the list S which contains lists of features with the first feature having higher preference than the second feature"""
    S=[]
    for q_list in segregatedFeatures:
        listlen=len(q_list)
        for i in range(listlen):
            for j in range(i+1,listlen):
                S.append(decide_preference(q_list[i],q_list[j]))
    return S



