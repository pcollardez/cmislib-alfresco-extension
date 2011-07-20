#
#      Licensed to the Apache Software Foundation (ASF) under one
#      or more contributor license agreements.  See the NOTICE file
#      distributed with this work for additional information
#      regarding copyright ownership.  The ASF licenses this file
#      to you under the Apache License, Version 2.0 (the
#      "License"); you may not use this file except in compliance
#      with the License.  You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#      Unless required by applicable law or agreed to in writing,
#      software distributed under the License is distributed on an
#      "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#      KIND, either express or implied.  See the License for the
#      specific language governing permissions and limitations
#      under the License.
#

import unittest
from unittest import TestSuite, TestLoader
import cmislibalf
from cmislib import CmisClient
from cmislib.exceptions import *
from time import time

REPOSITORY_URL = 'http://localhost:8080/nuxeo/atom/cmis'
USERNAME = 'Administrator'
PASSWORD = 'Administrator'
EXT_ARGS = {}
TEST_ROOT_PATH = '/default-domain/workspaces/cmislibnux'


class CmisAlfTestBase(unittest.TestCase):

    """ Common ancestor class for most cmislib unit test classes. """

    def setUp(self):
        """ Create a root test folder for the test. """
        self._cmisClient = CmisClient(REPOSITORY_URL, USERNAME, PASSWORD, **EXT_ARGS)
        self._repo = self._cmisClient.getDefaultRepository()
        self._rootFolder = self._repo.getObjectByPath(TEST_ROOT_PATH)
        self._folderName = " ".join(['cmislibnux', self.__class__.__name__, str(time())])
        self._testFolder = self._rootFolder.createFolder(self._folderName)

    def tearDown(self):
        """ Clean up after the test. """
        self._testFolder.deleteTree()

class HookTest(CmisAlfTestBase):

    def testHook(self):
        documentName = 'testDocument'
        newDoc = self._repo.createDocument(documentName, parentFolder=self._testFolder)
        self.assertEquals(documentName, newDoc.getName())
        self.assertFalse(newDoc.hasAspect('P:cm:summarizable'))
        
        otherDoc = self._repo.getObjectByPath(TEST_ROOT_PATH + '/testAspects')
        self.assertEqual(0, len(otherDoc.getAspects()))
        
        aspect = otherDoc.findAspect('cm:title')
        self.assertEqual(None, aspect)
        
        self.assertRaises(InvalidArgumentException, newDoc.addAspect, 'P:cm:summarizable')
        self.assertFalse(newDoc.hasAspect('P:cm:summarizable'))
        props = {'cm:summary': 'bla bla bla'}
        self.assertRaises(InvalidArgumentException, newDoc.updateProperties, props)
        self.assertEqual(None, newDoc.getProperties().get('cm:summary'))
        
        self.assertEqual(newDoc.properties, newDoc.getProperties())
        
        self.assertRaises(InvalidArgumentException, newDoc.removeAspect, 'P:cm:summarizable')
        self.assertFalse(newDoc.hasAspect('P:cm:summarizable'))
        self.assertTrue(newDoc.getProperties().get('cm:summary') is None)
                
        self.assertRaises(InvalidArgumentException, newDoc.addAspect, 'P:no:aspect')
        self.assertRaises(InvalidArgumentException, newDoc.updateProperties, props)
        
        self.assertTrue(newDoc.getProperties().get('cm:summary') is None)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    tts = TestSuite()
    tts.addTests(TestLoader().loadTestsFromTestCase(HookTest))
    unittest.TextTestRunner().run(tts)