# opml2mm.py
"""Copyright 2016 ADXSoft

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
 IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

"""Python script to convert an opml file to Freemind/Freeplane format

   assumes you have previously installed Python 2.7)

   The script will import each 'outline' element in the opml file as a node. 
 
   If the outline element contains an attribute named '_note' 
   this will be imported as a plain text node note 

   NOTE. Your original note is preserved if possible 
          i.e. notes data has valid xml/html syntax
          
          If the note data is invalid xml/html then it is still added but
          the html symbols are escaped e.g. < becomes &lt;
          this avoids any confusion for the Freemind/Freeplane parsers
          which interpret the note
          

   The import works with opml files saved from the following tools

     - Omni Outliner 3 (plain and rich text notes seem ok)
     - Mindly (imports ok)
     - Mindnode Pro (V1) (imports ok)
     - Scrivener (does not seem to export rich text in 
                  correct html tags in the _note attributes 
                  of it opml tags)
"""

# ==========================================================================
# =========== CHANGE THE FOLLOWING SETTINGS BEFORE YOU RUN THIS SCRIPT!!
# ==========================================================================
#
# Full path to the input .opml file
input_opml_file='/Users/allandavies/Developer/Python/MyProjects/opmltomm/TestData/fromsample.opml'

# Full path to the output .mm which can be imported into Freemind 1.x or FreePlane 1.5.x
output_mm_file='/Users/allandavies/Developer/Python/MyProjects/opmltomm/TestData/fromsample.mm'

# ==========================================================================
# ==========================================================================

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import iterparse
import sys, getopt
from HTMLParser import HTMLParser
import cgi

class Opml2Mm:

    def __init__(self):
        self.nodetree = []          #tree that will contain the elements for the .mm output file 
        self.nodetree.append("")    #initialise tree
        self.previous_level = 0     #initialise depth control

    # def open(self, inputfile):
    #     """ get opml data and load into ElementTree tree """
    #     if inputfile.endswith('.opml'):
    #         try:
    #             # self.tree = ET.parse(inputfile)
    #             return self.tree
    #         except:
    #             print "Cannot open file "+inputfile+'\n' \
    #                   "File may not exist or file may not be a valid xml file\n" \
    #                   "\nUSAGE\n"
    #             closedown()

    def convert_to_mm(self, inputfile,outputfile):
        """write output .mm file"""

        # Create the tree self.mm and add the map element
        self.mm = ET.Element("map",version="1.5.9")
        
        depth = 0

        # Iterate through the opml file looking for 'outline' tags
        for (event, node) in iterparse(inputfile, ['start', 'end', 'start-ns', 'end-ns']):
            
            # end of outline tag encountered
            if event == 'end':
                if node.tag=='outline':
                    # drop back a level
                    depth -= 1
                
            # start of outline tag encountered
            if event == 'start' and node.tag=='outline':
                
                #bump the depth 
                depth += 1
                
                # get the outline tags text
                # may be in the node.text field or the text attribute
                if node.text==None or node.text.strip()=='':
                    try:
                        nodetext=node.attrib['text'].strip()
                    except:
                        nodetext=''
                else:
                    nodetext=node.text.strip()
                
                # log where we're at
                print depth*' ',depth,'Added',node.tag,'text => '+nodetext+''
                
                # if at new level create a node element
                if depth > self.previous_level:
                    self.nodetree.append("")
                    attributes={}
                    attributes['TEXT']=nodetext
                    self.nodetree[depth] = ET.SubElement(self.nodetree[depth-1], "node",attrib=attributes)
                    
                    # if theres a note in the 'outline' tag ie attribute with tag '_node'
                    # create the note element
                    try:
                        # obtain note
                        node_note=node.attrib['_note']
                        
                        # remove any non ascii characters to avoid unicode problems
                        node_note=self.removeNonAscii(node_note)
                    except:
                        # couldn't get a note for this node so set blank
                        node_note=''
                        
                    #if we have a note then add the richcontent element Freemind and Freeplane expect
                    if node_note<>'':
                            try:                                
                                # create richnote tag with note details embedded 
                                attributes={}
                                attributes['TYPE']='DETAILS'
                                note_element='<html><head></head><body>'+ \
                                        node_note + \
                                    '</body></html>'
                                self.nodetree[depth] = ET.SubElement(self.nodetree[depth], "richcontent",attrib=attributes)                                
                                
                                # inserting the note into node tag
                                # if note contains html and it is valid note is added as html
                                # 
                                # however if ElementTree rejects note due to parsing errors
                                # such as badly formed html then the exception below will be 
                                # triggered and note is added with raw 'escaped' text
                                # for example <b> is &lt:b&gt;

                                self.nodetree[depth].append(ET.fromstring(note_element))  
                                
                                # log result
                                print depth*' ','++ Added Note',node_note
                            except:
                                # ElementTree could not parse the opml note in the current outline tag
                                # so no note is added
                                
                                # note data is invalid xml so add the note data as xml CDATA tag
                                print '!!Warning: Invalid data. Note added as raw character data\nNote data=',node_note
  
                                # unescape html characters to avoid clashes with Freemind/Freeplane parsers
                                node_note=HTMLParser.unescape.__func__(HTMLParser, node_note)
                                
                                # remove any non ASCII characters from note
                                node_note=self.removeNonAscii(node_note)

                                # wrap escaped note in CDATA tag
                                note_element='<html><head></head><body>'+ \
                                    '<![CDATA['+ \
                                        node_note + \
                                    ']]>' + \
                                    '</body></html>'
                                
                                self.nodetree[depth].append(ET.fromstring(note_element))  
                 
                else:
                    # finished at current level so jump back a level
                    self.previous_level = depth-1

            if event == 'start' and node.tag=='title':
                # log title found
                print 'Added tag ',node.tag,'==>',node.text
                
                # add title tag as the first node
                self.nodetree[0]=ET.SubElement(self.mm, "node", attrib={'TEXT':node.text})

        # get the output data
        tree = ET.ElementTree(self.mm)
        root=tree.getroot()
        outputdata=ET.tostring(root)
        # print outputdata
        
        # create the output .mm file
        f=open(outputfile,'w')
        f.write(self.removeNonAscii(outputdata))
        f.close()
        
        return

    def removeNonAscii(self,s): 
        return "".join(i for i in s if ord(i)<128) #this gem gets rid of unicode characters

def closedown():
    print __doc__
    quit()
def main():
    opml2mm = Opml2Mm()
    opml2mm.convert_to_mm(input_opml_file,output_mm_file)
    print output_mm_file + " created."

if __name__ == "__main__":
    main()
    
