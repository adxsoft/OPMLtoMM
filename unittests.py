#!/usr/bin/python
# -*- coding: utf-8 -*-# opmltomm.py
# unittests.py version 1
#
# History
# V1 - original version uploaded to github

import unittest
import unittest.runner
import opmltomm
import os
import shutil
import re
import datetime
import difflib
from difflib import SequenceMatcher

###########################################################################
## Utility functions
###########################################################################
def print_diffs(expected,actual):
    a=expected
    b=actual
    s = SequenceMatcher(None,a,b)
    print '\n'
    ctr=0
    for block in s.get_matching_blocks():
        apos=block[0]
        bpos=block[0]
        aendpos=apos+block[2]
        bendpos=bpos+block[2]
        achunk=expected[apos:aendpos]
        bchunk=actual[bpos:bendpos]
        # print "a[%d] and b[%d] match for %d elements" % block
        print '\nACTUAL has matching Error at '+str(aendpos)
        print 'Expected ='+expected[bendpos:bendpos+100]+'\nFound    ='+actual[aendpos:aendpos+100]
        print 'Matched values from 0 to '+str(aendpos-1)+' are'
        print ' EXPECTED='+bchunk
        print ' ACTUAL  ='+achunk
        print ''
        if ctr==0:
            break
        else:
            ctr+=1

###########################################################################
## Unit Tests - OPML to MM conversions
###########################################################################
#
# These tests are designed to run in the local project folder opmltomm

class TestConversions(unittest.TestCase):

    def setUp(self):
        self.opml2mm = opmltomm.Opml2Mm()
        
    def runconversion(self,filesuffix):
        inputfile='TestData/from'+filesuffix+'.opml'
        outputfile='TestData/output.mm'
        f=open('TestData/from'+filesuffix+'.mm')
        self.expectedresult=f.read()
        f.close()
        self.opml2mm.convert_to_mm(inputfile,outputfile)
        f=open('TestData/output.mm')
        self.actualresult=f.read()
        f.close()

    def test_scrivenerrichtextimport(self):
        self.runconversion('scrivenerrichtext')
        if self.actualresult<>self.expectedresult:
            print_diffs(self.expectedresult,self.actualresult)
        self.assertEqual(self.expectedresult,self.actualresult)
    def test_scrivenerplaintextimport(self):
        self.runconversion('scrivenerplaintext')
        if self.actualresult<>self.expectedresult:
            print_diffs(self.expectedresult,self.actualresult)
        self.assertEqual(self.expectedresult,self.actualresult)
    def test_oo3import(self):
        self.runconversion('oo3')
        if self.actualresult<>self.expectedresult:
            print_diffs(self.expectedresult,self.actualresult)
        self.assertEqual(self.expectedresult,self.actualresult)
    def test_fromfreeplaneimport(self):
        self.runconversion('freeplane')
        if self.actualresult<>self.expectedresult:
            print_diffs(self.expectedresult,self.actualresult)
        self.assertEqual(self.expectedresult,self.actualresult)
    def test_sampleimport(self):
        self.runconversion('sample')
        if self.actualresult<>self.expectedresult:
            print_diffs(self.expectedresult,self.actualresult)
        self.assertEqual(self.expectedresult,self.actualresult)

suite = unittest.TestLoader().loadTestsFromName("unittests")
unittest.TextTestRunner(verbosity=3).run(suite)
