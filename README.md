# OPMLtoMM
Python script to convert OPML files to Freeplane/Freemind files

## Background
I'm a keen Freeplane user but use other mindmapping tools on my mobile devices.
Would be nice if Freeplane had a mobile app :-)

I set up this script to import opml files I send to my desktop Freeplane environment.

## Pre-requisites
This script assumes you have previously installed Python 2.7. 
(It has not been tested with Python 3)

## Installation
Simply download the zip file and unzip wherever you wish. 
Leave the folder structure as is so the unittests can be run correctly

## opmltomm.py
Before you run this script you MUST change the following lines to set up your input and output
file locations.

<pre>
# ==========================================================================
# =========== CHANGE THE FOLLOWING SETTINGS BEFORE YOU RUN THIS SCRIPT!!
# ==========================================================================
#
# Full path to the input .opml file
input_opml_file='YOURFULLPATH/YOURINPUTOPMLFILE.opml'

# Full path to the output .mm which can be imported into Freemind 1.x or FreePlane 1.5.x
output_mm_file='YOURFULLPATH/YOUROUTPUTMMFILE.opml.mm'

# ==========================================================================
# ==========================================================================
</pre>

## Running the script
Execute the script as follows from the terminal

<B>python opmltomm.py</B>

## Script operation

The script will import each 'outline' element in the opml file as a freeplane/freemind node. 
 
If the outline element contains an attribute named '_note' 
   this will be imported as a plain text node note 

   NOTE. Your original note is preserved if possible 
          i.e. the note data in the _note tag in the opml file
               has valid xml/html syntax
          
          If the note data is invalid xml/html then it is still added but
          the html symbols are escaped e.g. < becomes &lt;
          this avoids any confusion for the Freemind/Freeplane parsers
          which interpret the note
          
## unittests.py
Run this script to execute several test conversions from 
opml format to .mm files (Freeplane and Freemind format)
included are tests for 
- scrivener exported opml files with rich and plain text notes
- freeplane exported opml (freeplane does not export notes only nodes at this time)
- omnioutliner 3 opml with rich and plain text notes
- mindly opml with plain text notes

Execute the script as follows from the terminal

<B>python unittests.py</B>

Note. This script must be run in the folder you unzipped into during the installation step
which has the <B>TestData</B> folder expected by the unittests module
