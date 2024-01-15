# replacement_TEX_XML.py
# to convert a critical edition from tex to tei-xml 
# written between 8 and 17 September 2023 by Böðvar Ólafsson and Katarzyna Anna Kapitan
# It requires that xml-based edition uses shelfmark format A601, B1109 etc
# and that apparatus is encoded following the reledmac guidelines.

import re
import numpy as np
from apparatus_function_def import *

#Put your filename here: 
filename_in = 'app_A601_edition'
extension_in = '.tex'


if __name__ == "__main__":
    f = open(filename_in + extension_in)
    myString = f.read()
    text_file = open('Out_Apparatus_' + filename_in + '.xml','w')
    print("The proccess has started - wait and be patient")

    ## Conditions we are looking for:
    str_exp = "textit{"
    str_lem = "edtext{"
    str_obr = "{"
    str_cbr = "}"
    indent = '    '
    str_quote = "enquote{"
    str_footnote = "commentary{"
    str_pagebreak = "ledouternote{"
    str_subsec = "subsection\*{"
    str_section = "section\*{"

    # Pre-processing: search and replace
    myStringNew = myString.replace(
        '\\newpage', '').replace(
            '\\beginnumbering', '').replace(
                '\\endnumbering', '').replace(
                    '\\pstart', '<p>').replace(
                        '\pend', '</p>').replace(
                            '\\footnote{', '\commentary{').replace(
                                '||', '').replace('  ', ' ')
    
    # Pre-processing: RegExp replacment
    REpattern1 = r'\\vspace{\d+mm\}'
    REString1 = re.sub(REpattern1, '', myStringNew)

    REpattern2 = r'\\-'
    REString2 = re.sub(REpattern2, '', REString1)

    
    ## Overwrite the previous string 
    myString = REString2

    ## __________________________________________________
    ## Section I. ABBREVIATIONS
    ## index_exp - incidicies for all textit{
    ## index_obr - indicies for all opening brackets
    ## index_cbr - indicies for all closing brackets
    index_exp = [i.start() for i in re.finditer(str_exp, myString)]
    index_obr = [i.start() for i in re.finditer(str_obr, myString)]
    index_cbr = [i.start() for i in re.finditer(str_cbr, myString)]
    ## Generete indexing for 'expansion' when the brackets open and close after \textit
    ## i_obr - indicies for  opening brackets that match the criteria of the loop
    ## i_cbr - indicies for  closing brackets that match the criteria of the loop
    ## The first loop goes to the array containing all indicies of "textit" and itterates through it
    ## The second loop goes into the array of all indicies for the opening brackets and checks whether their indicies are greater than indicies of  "textit"
    ## If the index of opening bracket is greater than the index of "textit" it is passed on into i_obr.
    ## The third loop repeats the second for closing brackets.
    i_obr = []
    i_cbr = []
    for i in range(len(index_exp)):
        for j in range(len(index_obr)):
            if index_obr[j] > index_exp[i]:
                i_obr.append(index_obr[j])
                break
        for j in range(len(index_cbr)):
            if index_cbr[j] > index_exp[i]:
                i_cbr.append(index_cbr[j])
                break
    # The result are only the indicies associated with "textit"
    ## Create a new string, which starts by copying everything until the index-1 of the first "textit"
    ## The loop goes through indicies of "textit" and adds <ex>, followed by eveything within the brackets, and followed by </ex>, and
    ## everything until the next occurance of "textit"

    myString_new = myString[:index_exp[0]-1]
    for i in range(len(index_exp)):
        if i < len(index_exp)-1:
            myString_new = myString_new + '<ex>' + myString[i_obr[i]+1:i_cbr[i]] + '</ex>' + myString[i_cbr[i]+1:index_exp[i+1]-1]
        else:
            myString_new = myString_new + '<ex>' + myString[i_obr[i]+1:i_cbr[i]] + '</ex>' + myString[i_cbr[i]+1:]

    ## Overwrite previous string
    myString = myString_new
    print('Section I: Abreviation replacement done')

    ## __________________________________________________
    ## Section II: QUOTES
    ## This section changes "enquotes" into <q>s
    del myString_new

    index_quote = [i.start() for i in re.finditer(str_quote, myString)]
    index_obr = [i.start() for i in re.finditer(str_obr, myString)]
    index_cbr = [i.start() for i in re.finditer(str_cbr, myString)]

    i_obr = []
    i_cbr = []
    for i in range(len(index_quote)):
        for j in range(len(index_obr)):
            if index_obr[j] > index_quote[i]:
                i_obr.append(index_obr[j])
                break
        for j in range(len(index_cbr)):
            if index_cbr[j] > index_quote[i]:
                i_cbr.append(index_cbr[j])
                break
    myString_new = myString[:index_quote[0]-1]
    for i in range(len(index_quote)):
        if i < len(index_quote)-1:
            myString_new = myString_new + '<q>' + myString[i_obr[i]+1:i_cbr[i]] + '</q>' + myString[i_cbr[i]+1:index_quote[i+1]-1]
        else:
            myString_new = myString_new + '<q>' + myString[i_obr[i]+1:i_cbr[i]] + '</q>' + myString[i_cbr[i]+1: ]

    ## Overwrite previous string
    myString = myString_new
    print("Section II: Quotes replacement done")


    ## __________________________________________________
    ## Section III: FOOTNOTES
    ## replace '\commentary{ with <note>'
    del index_obr, index_cbr, i_obr,i_cbr
    index_fn = [i.start() for i in re.finditer(str_footnote, myString)]
    index_obr = [i.start() for i in re.finditer(str_obr, myString)]
    index_cbr = [i.start() for i in re.finditer(str_cbr, myString)]
    i_obr = []
    i_cbr = []
    
    for i in range(len(index_fn)):
        for j in range(len(index_obr)):
            if index_obr[j] > index_fn[i]:
                i_obr.append(index_obr[j])
                break
        for j in range(len(index_cbr)):
            if index_cbr[j] > index_fn[i]:
                i_cbr.append(index_cbr[j])
                break
    myString_new = myString[:index_fn[0]-1]
    for i in range(len(index_fn)):
        if i < len(index_fn)-1:
            myString_new = myString_new + '<note>' + myString[i_obr[i]+1:i_cbr[i]] + '</note>' + myString[i_cbr[i]+1:index_fn[i+1]-1]
        else:
            myString_new = myString_new + '<note>' + myString[i_obr[i]+1:i_cbr[i]] + '</note>' + myString[i_cbr[i]+1: ]
    ## Overwrite previous string
    myString = myString_new
    print("Section III: Footnotes replacement done")
    
    ## ________________________________________________________________________
    #Section IV: Page breaks
    del index_obr, index_cbr, i_obr,i_cbr
    index_pagebreak = [i.start() for i in re.finditer(str_pagebreak, myString)]
    index_obr = [i.start() for i in re.finditer(str_obr, myString)]
    index_cbr = [i.start() for i in re.finditer(str_cbr, myString)]
    i_obr = []
    i_cbr = []
    for i in range(len(index_pagebreak)):
        for j in range(len(index_obr)):
            if index_obr[j] > index_pagebreak[i]:
                i_obr.append(index_obr[j])
                break
        for j in range(len(index_cbr)):
            if index_cbr[j] > index_pagebreak[i]:
                i_cbr.append(index_cbr[j])
                break
    myString_new = myString[:index_pagebreak[0]-1]
    
    for i in range(len(index_pagebreak)):
        if i < len(index_pagebreak)-1:
            myString_new = myString_new + '<pb n="' + myString[i_obr[i]+1:i_cbr[i]] + '"/>' + myString[i_cbr[i]+1:index_pagebreak[i+1]-1]
        else:
            myString_new = myString_new + '<pb n="' + myString[i_obr[i]+1:i_cbr[i]] + '"/>' + myString[i_cbr[i]+1: ]
    ## Overwrite previous string
    myString = myString_new
    print("Section IV: Pagebreaks done")

    ## __________________________________________________
    # Section V: Subsections
    del index_obr, index_cbr, i_obr,i_cbr
    index_subsec = [i.start() for i in re.finditer(str_subsec, myString)]
    index_obr = [i.start() for i in re.finditer(str_obr, myString)]
    index_cbr = [i.start() for i in re.finditer(str_cbr, myString)]
    i_obr = []
    i_cbr = []
    
    for i in range(len(index_subsec)):
        for j in range(len(index_obr)):
            if index_obr[j] > index_subsec[i]:
                i_obr.append(index_obr[j])
                break
        for j in range(len(index_cbr)):
            if index_cbr[j] > index_subsec[i]:
                i_cbr.append(index_cbr[j])
                break

    myString_new = myString[:index_subsec[0]-1]

    for i in range(len(index_subsec)):
        if i < len(index_subsec)-1:
            myString_new = myString_new + '<hi rend="rubric">' + myString[i_obr[i]+1:i_cbr[i]] + '</hi>' + myString[i_cbr[i]+1:index_subsec[i+1]-1]
        else:
            myString_new = myString_new + '<hi rend="rubric">' + myString[i_obr[i]+1:i_cbr[i]] + '</hi>' + myString[i_cbr[i]+1: ]

    ## Overwrite previous string
    myString = myString_new
    print("Section V: Subsections done")


        ## __________________________________________________
    # Section VI: Sections
    del index_obr, index_cbr, i_obr,i_cbr
    index_section = [i.start() for i in re.finditer(str_section, myString)]
    index_obr = [i.start() for i in re.finditer(str_obr, myString)]
    index_cbr = [i.start() for i in re.finditer(str_cbr, myString)]
    i_obr = []
    i_cbr = []
    
    for i in range(len(index_section)):
        for j in range(len(index_obr)):
            if index_obr[j] > index_section[i]:
                i_obr.append(index_obr[j])
                break
        for j in range(len(index_cbr)):
            if index_cbr[j] > index_section[i]:
                i_cbr.append(index_cbr[j])
                break

    myString_new = myString[:index_section[0]-1]

    for i in range(len(index_section)):
        if i < len(index_section)-1:
            myString_new = myString_new + '<hi rend="rubric">' + myString[i_obr[i]+1:i_cbr[i]] + '</hi>' + myString[i_cbr[i]+1:index_section[i+1]-1]
        else:
            myString_new = myString_new + '<hi rend="rubric">' + myString[i_obr[i]+1:i_cbr[i]] + '</hi>'  + myString[i_cbr[i]+1: ]

    ## Overwrite previous string
    myString = myString_new
    print("Section VI: Sections done")

    ## __________________________________________________
    ## Section VII: APPARATUS
    ## This section changes apparatus
    myString = apparatus(myString)
    print("Section VII: Apparatus replacement done")

    
    
    text_file.write
    text_file.write(myString)
    text_file.close()
    f.close()
    print('The entire process is done!')
