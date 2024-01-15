# edition_TEX_XML

This folder contains data and scrips associated with the publication of the text critical edition of Hrómundar sögur and conversion from TEX to XML.

*BEFORE THE CONVERSION*

To convert TEX files of a text-critical edition with apparatus into TEI XML with replacement_TEX_XML.py (and apparatus_function_def.py) your TEX file has to be encoded following the reledmac guidelines, with \edtext and \Afootnote, etc. 

Your shelfmarks have to follow the pattern A601, B11109 (letters followed by numbers, no spaces, no special characters) etc., see the edition file  app_B11109_edition.tex 


*AFTER THE CONVERSION*

After the conversion from LaTeX to XML with our script, the following elements have to be checked and fixed:

1. Search for one of the brackets [*] used for unclear and replace with the <unclear></unclear> tag

2. Search for one of the brackets ⟨*⟩ used for supplied text and replace it with the <supplied></supplied> tag = MATHEMATICAL RIGHT AND LEFTANGLE BRACKET U+27E8 and U+27E9 

3. Search for one of the insertion marks  ⸌*⸍ used for scribal insertions  and replace it with the <add></add> tag = LEFT & RIGHT RAISED OMISSION BRACKET U+2E0C and U+2E0D

4. Search for  * Deletion marks (not in Unicode but Oxygen finds them) and replace them with del-tags <del></del>

5. Search for '{' or '}' to make sure no TeX markup is left in your file. /app

6. Paste the output into the body of your TEI XML file and add divs and metadata according to your needs.

7. Make sure that <ex> is not incorrectly used within the notes (with XPath), if it is replace it with <q>

8. Format and indent and then Search for superfluous blank spaces, common examples include: ‘</app> .’, ‘</app> ,’ , ‘ </lem>’, ‘ </rdg>’
