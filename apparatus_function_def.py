# apparatus_function_def.py
# required by replacement_TEX_ZML.py
# written between 8 and 17 September 2023 by Böðvar Ólafsson and Katarzyna Anna Kapitan
import re
import numpy as np

def apparatus(myString):
    myre = r'[A-Z]+[0-9]+'
    str_lem = "edtext{"
    str_rdg = "Afootnote{"
    str_obr = "{"
    str_cbr = "}"
    indent = '    '
    index_lem = [i.start() for i in re.finditer(str_lem, myString)]
    index_rdg = [i.start() for i in re.finditer(str_rdg, myString)]
    index_obr = [i.start() for i in re.finditer(str_obr, myString)]
    index_cbr = [i.start() for i in re.finditer(str_cbr, myString)]

    shelfmarks = re.findall(myre, myString)
    shelfmark_index = [i.start() for i in re.finditer(myre, myString)]
    shelfmark_index = np.array(shelfmark_index)

# We start by looking at the lemma
# Look for opening brackets that are associated with lemma
    i_obr_lem = []
    i_cbr_lem = []
    for i in range(len(index_lem)):
        for j in range(len(index_obr)):
            if index_obr[j] > index_lem[i]:
                i_obr_lem.append(index_obr[j])
                break
        for j in range(len(index_cbr)):
            if index_cbr[j] > index_lem[i]:
                i_cbr_lem.append(index_cbr[j])
                break
# Now we are moving to the readings
# Look for opening brackets that are associated with readings
    i_obr = []
    i_cbr = []

    for i in range(len(index_rdg)):
        for j in range(len(index_obr)):
            if index_obr[j] > index_rdg[i]:
                i_obr.append(index_obr[j])
                break
        for j in range(len(index_cbr)):
            if index_cbr[j] > index_rdg[i]:
                i_cbr.append(index_cbr[j])
                break
            
    myFinalString = myString[:index_lem[0]-1]
    for i in range(len(i_obr)):
        i_rdg=[]
        i_rdg = shelfmark_index[shelfmark_index>i_obr[i]]
        i_rdg = i_rdg[i_rdg<i_cbr[i]]
        myNewString = myString[ i_obr[i]+1 : i_cbr[i] ]

        myFinalString = (myFinalString + '\n<app>\n'
                        + indent + '<lem>' + myString[i_obr_lem[i]+1:i_cbr_lem[i]] + '</lem>\n')
        rdg_str = ''
        #print('myFinalString after adding lemma: ',myFinalString)
        #print("myNewString is [readings]: ", myNewString)
        shelfmarks = re.findall(myre, myNewString)
        shelfmark_index = [i.start() for i in re.finditer(myre, myNewString)]
        shelfmark_index = np.array(shelfmark_index)

        if len(shelfmark_index) > 1:
            myRange = range(len(shelfmark_index)-1)
            outputShelf = ''
            ctr = 0
            for j in myRange:
                # Test if there is more than one manuscript with the same reading
                if shelfmark_index[j+1] <= shelfmark_index[j] + len(shelfmarks[j]) + 2:
                    # Test whether we are at the last iteration of the loop
                    if j == len(shelfmark_index)-2:
                        #If we are on the last one
                        outputShelf = str(outputShelf) + '#' + str(shelfmarks[j]) + ' #' + str(shelfmarks[j+1])
                        if j-ctr == 0:
                            variant_text = myNewString[:shelfmark_index[j-ctr]]
                        else:
                            variant_text = myNewString[ shelfmark_index[j-ctr-1]+len(shelfmarks[j-ctr-1])+2 : shelfmark_index[j-ctr]]
                        rdg_str = rdg_str + indent + '<rdg wit="' + str(outputShelf) + '">' + variant_text + '</rdg>\n' 
                    else:    
                        outputShelf = str(outputShelf) + '#' + shelfmarks[j] + ' '
                        ctr += 1
                        # Continue withi this until you hit the last shelfamrk for this reading
                        continue
                # If there is no more shelfmarks, i.e. there is only one shelfmark per reading do this:    
                else: # Test whether we are at the last iteration of the loop
##                    print('my j in else loop', j)
                    if j == len(myRange)-1:
                        #If we are on the last one
                        outputShelf = str(outputShelf) + '#' + str(shelfmarks[j])
                        outputShelf2 = '#' + str(shelfmarks[j+1])
                        if j-ctr == 0:
                            variant_text = myNewString[:shelfmark_index[j-ctr]]
                        else:    
                            variant_text = myNewString[ shelfmark_index[j-ctr-1]+len(shelfmarks[j-ctr-1])+2 : shelfmark_index[j-ctr]]
                        variant_text2 = myNewString[ shelfmark_index[j]+len(shelfmarks[j])+2 : shelfmark_index[j+1]]
                        rdg_str = rdg_str + indent + '<rdg wit="' + str(outputShelf) + '">' + variant_text + '</rdg>\n'
                        rdg_str = rdg_str + indent + '<rdg wit="' + str(outputShelf2) + '">' + variant_text2 + '</rdg>\n'
                    else:
                        outputShelf = str(outputShelf) + '#' + shelfmarks[j]
                        variant_text = ''
                        if j-ctr == 0:
                            variant_text = myNewString[:shelfmark_index[j-ctr]]
                        else:
                            variant_text = myNewString[ shelfmark_index[j-ctr-1]+len(shelfmarks[j-ctr-1])+2 : shelfmark_index[j-ctr] ]
                        rdg_str = rdg_str + indent + '<rdg wit="' + str(outputShelf) + '">' + variant_text + '</rdg>\n'
                        ctr = 0
                        outputShelf = ''
##                print(rdg_str)
        elif len(shelfmark_index) == 1:
            outputShelf = '#' + shelfmarks[0]
            variant_text = myNewString[:shelfmark_index[0]]
            rdg_str = rdg_str + indent + '<rdg wit="' + str(outputShelf) + '">' + variant_text + '</rdg>\n'
        elif len(shelfmark_index) == 0:
            print("Opps, looks like you have an error in your LaTeX encoding, look for the following text:")
            test = i_obr[i]
            print(myString[(test-30):(test+30)])
            
            
# Now we create final string
# It tests whether there is one more lemma afterwards, if so it will copy the text up to there
# If not it will take what is left
        if i < len(index_lem)-1:    
            myFinalString = myFinalString + rdg_str + '</app>\n' + myString[i_cbr[i]+2:index_lem[i+1]-1]
        else:
            myFinalString = myFinalString + rdg_str + '</app>\n' + myString[i_cbr[i]+2:]
    return myFinalString

