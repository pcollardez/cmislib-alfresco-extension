'''
Created on 27 mai 2011

@author: pcollardez
'''
import unittest
from unittest import TestSuite, TestLoader
import cmislibalf
from cmislib import CmisClient
from time import time

REPOSITORY_URL = 'http://localhost:8080/alfresco/s/api/cmis'
USERNAME = 'admin'
PASSWORD = 'admin'
EXT_ARGS = {}
TEST_ROOT_PATH = '/cmislibalf'


class CmisAlfTestBase(unittest.TestCase):

    """ Common ancestor class for most cmislib unit test classes. """

    def setUp(self):
        """ Create a root test folder for the test. """
        self._cmisClient = CmisClient(REPOSITORY_URL, USERNAME, PASSWORD, **EXT_ARGS)
        self._repo = self._cmisClient.getDefaultRepository()
        self._rootFolder = self._repo.getObjectByPath(TEST_ROOT_PATH)
        self._folderName = " ".join(['cmislibalf', self.__class__.__name__, str(time())])
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
        self.assertTrue(otherDoc.hasAspect('P:cm:titled'))
        titledAspectObjectType = self._repo.getTypeDefinition('P:sys:temporary')
        self.assertFalse(otherDoc.hasAspect(titledAspectObjectType))
        
        self.assertEqual(3, len(otherDoc.getAspects()))
        
        aspect = otherDoc.findAspect('cm:title')
        self.assertEqual('P:cm:titled', aspect.getTypeId())
        
        newDoc.addAspect('P:cm:summarizable')
        self.assertTrue(newDoc.hasAspect('P:cm:summarizable'))
        props = {'cm:summary': 'bla bla bla'}
        newDoc.updateProperties(props)
        self.assertEqual('bla bla bla', newDoc.getProperties()['cm:summary'])
        
        newDoc.removeAspect('P:cm:summarizable')
        self.assertFalse(newDoc.hasAspect('P:cm:summarizable'))
        self.assertTrue(newDoc.getProperties().get('cm:summary') is None)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    tts = TestSuite()
    tts.addTests(TestLoader().loadTestsFromTestCase(HookTest))
    unittest.TextTestRunner().run(tts)