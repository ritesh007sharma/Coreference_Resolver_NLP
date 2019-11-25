"""
@author Ritesh Sharma
Date: Nov 25, 2019
Coreference Resolver.
"""

import spacy
import re
import sys
import copy
from pathlib import Path


enSpacy = spacy.load("en_core_web_md")
pronouns = ["i","you","they", "him", "mine", "your","yours", "hers", "who", "whom", "whose","myself", "yourself", "himself", "herself","itself", "me", "my", "he", "she", "his", "her", "it", "its", "their", "this", "that"]
regex = re.compile('[@_!#$%^&*()<>?/|}{~:]')

"""
The main function takes in the system argument and assigns it to first and second
args respectively and then passes those first and second args to the coreference method.
"""
def main():
    if sys.argv[1] is not None and sys.argv[2] is not None:
        firstArgs = sys.argv[1]
        secondArgs = sys.argv[2]
    else:
        print("please provide required txt files.")
    
    #Calling the coreference function.
    coreference(firstArgs, secondArgs)

"""
The coreference function takes in first and second args respectively and 
runs the coreference resolution by doing some matching before printing the values to 
the response files.
"""
def coreference(firstArgs, secondArgs):
    rList = []
    #openning the input files and appending it to rList.
    with open(firstArgs, 'r') as f:
        for line in f:
            rList.append(Path(line.strip()))
    
    outputDic = {}
    for path in rList:
        #dict of dict is created to store all sentences, corefs and noun phrases.
        parsedValues = {}
        parsedValues["s"] = {}
        parsedValues["c"] = {}
        parsedValues["np"] = {}
        #checking if the input match the given regex. 
        with open(str(path)) as f:
            for line in f:
                sRe = re.match("<S ID=\"([0-9]+)\">(.*)</S>", line)
                sId, sent = sRe.group(1, 2)

                corefR = re.findall("<COREF ID=\"(X[0-9]+)\">(.*?)</COREF>", sent)
                for i, j in corefR:
                    parsedValues['c'][i] = (j,sId)
            
                sent = re.sub("<[^<]+?>", '', sent)
                parsedValues['s'][sId] = sent
                nounPhrases = []
                #using spacy to get the noun chunks.
                noun_chunks = enSpacy(sent).noun_chunks
                #gets the head of the nounphrase and appends it to nounPhrase list.
                for np in noun_chunks:
                    nounPhrases.append({"np": np, "head": np.root.text})
                
                parsedValues['np'][sId] = nounPhrases
        s = parsedValues['s']
        c = parsedValues['c']
        nounPhrases = parsedValues['np']

        heads = []
        #appends the root to heads.
        for k, v in nounPhrases.items():
            if v == []:
                continue
            else:
                for dic in v:
                    heads.append((dic['head'], k))

        matchDic = {}

        for cID, currCoref in c.items():
            matchDic[cID] = []
            coText, coSentNum = currCoref
            #makes all the coref texts to lower to make computation easier.
            if coText.lower() in pronouns:
                matchDic[cID].append((coSentNum, coText))
                continue
            #calling the scanner function.
            scanner(matchDic[cID], s, coText, coSentNum)
            coRoots = []
            document = enSpacy(coText)
            for c in document.noun_chunks:
                coRoots.append(c.root.text)
            for head in heads:
                if int(head[1]) <= int(coSentNum):
                    continue
                #continue of root is a pronoun else append it to matchDic.
                if head[0].lower() in pronouns:
                    continue
                for iR in set(coRoots):
                    if head[0].lower() == iR.lower():
                        cR = copy.deepcopy(head[0])
                        if (head[1], cR) not in matchDic[cID]:
                            matchDic[cID].append((head[1], cR))
                        #if we encounter head in list of heads then remove if from the list.
                        if head in heads:
                            heads.remove(head)

        #All the code below is for printing or outputting into response file.
        outputDic[path.stem] = matchDic
        path = Path(secondArgs) / (path.stem + '.response')
        with open(str(path), 'w') as file:
            for k, v in outputDic[path.stem].items():
                file.write(str("<COREF ID=\"" + str(k) + "\">" +  str(v[0][1]) +  "</COREF>") + "\n")
                for i in range(1, len(v)):
                    g = str("{" + str(v[i][0] + "}" + " " + "{" + str(v[i][1] + "}")))
                    file.write(g + "\n")
                file.write("\n")
                file.close
     
"""
The scanner function scans the senctence using regex, if the match is found it
appends the match to numCoref.
"""
def scanner(numCoref, s, coText, coSentNum):
    for i, j in s.items():
        if int(i) < int(coSentNum):
            continue
        ##if regex search cannot find coref text then we append it into numCoref.
        if regex.search(coText) != None:
            numCoref.append((i, coText))
            break
        matched = re.findall('\w*' + coText + '\w*', j, re.I)
        #if it is a match then we append it into numCoref.
        for m in matched:
            numCoref.append((i, m))

#running the main.
if __name__ == '__main__':
    main()