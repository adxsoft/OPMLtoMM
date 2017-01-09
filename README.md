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

# Run opmltomm.py script directly from Freeplane
Whilst you can run opmltomm.py script from normal python,it is possible to run this script from within Freeplane in the Tools/Scripts menu. In order to do this you have to set up Freeplane to run a [jython](www.jython.org) script. There are some guidelines in the Freeplane help for jython however I found the script had dependencies that needed the full jython libraries not just jython.jar. 

The following steps set up Freeplane for executing python scripts in general. Once I'd completed all the steps I was able to choose opmltomm in the Tools/Script menu and run the script. 

*I have tested this in Windows 10 and Mac OSX El Capitan using Jython 2.5 with Java 1.8 runtime environment (JRE).*

## A. Instal Java 1.8
Freeplane won't run unless you alrady have java installed. If for some reason you do not have java installed already, go to [java download site](https://java.com/download) and download and install java (I recommend java 1.8 which I use)

## B. Instal Jython 2.5 
Download Jython 2.5 from  [jython](www.jython.org) and install into a folder of your choice eg ~/Jython on Mac or c:\Jython on Windows

## C. Adjust Freeplane Preferences
1. In Freeplane menu go to Freeplane/Preferences
2. Choose Plugins tab
3. Scroll down to the Scripting section
4. ***Script execution*** dropdown should be set to ***Yes***
5. ***Permit file read operations*** should be checked *(even though not recommended its needed for opmltomm.py script to save the converted .mm output file)*
6. ***Permit file read operations*** should be ***checked***
7. ***Permit to execute other applications*** should be ***checked***
8. ***File extensions not to be compiled*** should be set to '***py***'. *(If you have other file extensions already in this setting you should add ',py'. Note if you don't change this setting no python script will appear in the Tools/Scripts menu)*
9. ***Script classpath*** should be set to ***lib***. *(If you have other libraries than add 'lib' to the list)*
9. Close Freeplane to save the settings

## D. Setting up Freeplane user library for Jython
1. Go to the Jython folder set up in step B
2. Copy all files in the Jython Folder to the clipboard
3. Open Freeplane
4. In the Tools menu choose 'Open user directory' *(By opening this folder via Freeplane you ensure you get the correct folder that Freeplane references for any user libraries and scripts)*
5. Open the ***lib*** folder
5. Paste the Jython files from the clipboard into the ***lib*** folder. *(This ensures all the libraries for Jython are present. The Freeplane documentation says to just put jython.jar in lib folder but this didn't pick up some of my imports. Copying the whole jython folder contents avoids any missing imports)*

## Move python script to Freeplane user directory
1. Open Freeplane application
2.  In the Tools menu choose 'Open user directory' 
3. open the ***scripts*** folder
4. copy the python script *opmltomm.py* to the ***scripts*** folder
5. close and re-open Freeplane *(By doing this Freeplane will reload the scripts in the Tools/Scripts menu)
6. Check that *opmltomm.py* appears in the Tools/Scripts menu. If it does not appear then check you have followed all of the previous steps.

# Running other python scripts
To add any other python scripts you simply copy them in the ***scripts*** folder in the Freeplane user directory *(In Freeplane go to Tools/Open user directory)*

Once this setup is done you can add python scripts to the scripts menu and they will generally run well. 

I found that python print statements are directed to the Freeplane log files in the user directory and have the text 'STDOUT' in the log entry. 

Jython does have some limitations the main one I have found is that you cannot use python GUI libraries and have to use swing libraries. Swing is actually a very nice library and easy to use. The example below is a jython script *filechooser.py* that asks the user to choose a file

    # filechooser.py 
    import sys
    import javax.swing as swing
    from javax.swing.filechooser import FileNameExtensionFilter

    def popup(msg):
        swing.JOptionPane.showMessageDialog(None, msg)
    # Choose the input opml file in File dialog
    inputdlg=swing.JFileChooser()
    inputdlg.setDialogTitle("OPML to MM Conversion - Choose OPML File")
    inputdlg.setAcceptAllFileFilterUsed(False)
    inputdlg.setMultiSelectionEnabled(False)
    filter = FileNameExtensionFilter("opml files", ["opml"])
    inputdlg.addChoosableFileFilter(filter)
    dlg=inputdlg.showOpenDialog(None)
    if inputdlg.selectedFile<>None:
        input_opml_file=str(inputdlg.currentDirectory)+"/"+str(inputdlg.selectedFile.name)

        # set output file nme same as input file name
        # but with suffix .mm
        # outputfile is saved in same directory as input file
        output_mm_file=input_opml_file[:-len('.opml')]+'.mm'

        # allow user to rename output file if required
        frame = swing.JFrame();
        result = swing.JOptionPane.showInputDialog(
                    frame, 
                    "Proposed mm file name\nWIll be stored in\n"+ \
                    str(inputdlg.currentDirectory),
                    inputdlg.selectedFile.name[:-len('.opml')]+'.mm'
                    )

        if result==None:
            # rename dialog cancelled so exit script
            popup('Script cancelled by user')
            sys.exit()
        else:
            msg='Success! \n\nInput file is %s \nOutput file is %s' % \
                (input_opml_file,
                 output_mm_file)
            popup(msg)

    else:
        # no input file selected so exit script
        print 'Script cancelled by user'
        sys.exit()
