from cmislib import model

ALFRESCO_NS = 'http://www.alfresco.org'
APPLIED_ASPECTS = 'appliedAspects'
SET_ASPECTS = 'alf:setAspects'
ASPECTS_TO_ADD = 'alf:aspectsToAdd'
ASPECTS_TO_REMOVE = 'alf:aspectsToRemove'


def _initData(self):
    model.CmisObject._initData(self)
    self._aspects = {}

def _findAlfrescoExtensions(self):
    if not hasattr(self, '_aspects'):
        self._aspects = {}
    if self._aspects == {}:
        if self.xmlDoc == None:
            self.reload()
        appliedAspects = self.xmlDoc.getElementsByTagNameNS(ALFRESCO_NS, APPLIED_ASPECTS)
        for node in appliedAspects:
            aspectType = self._repository.getTypeDefinition(node.childNodes[0].data)
            self._aspects[node.childNodes[0].data] = aspectType

def hasAspect(self, arg):
    result = False
    if arg is not None:
        self._findAlfrescoExtensions()
        if isinstance(arg, model.ObjectType):
            result = arg.getTypeId() in self._aspects
        else:
            result = arg in self._aspects
    return result

def getAspects(self):
    self._findAlfrescoExtensions()
    return self._aspects.values()

def findAspect(self, propertyId):
    self._findAlfrescoExtensions()
    if (propertyId is not None) and (len(self._aspects) > 0):
        for id, aspect in self._aspects.iteritems():
            props = aspect.getProperties()
            if propertyId in props:
                return aspect
    return None

def _updateAspects(self, addAspects=None, removeAspects=None):
    if addAspects or removeAspects:
        selfUrl = self._getSelfLink()
        xmlEntryDoc = model.getEntryXmlDoc()
        # Patch xmlEntryDoc
        #propertiesElement = xmlEntryDoc.getElementsByTagNameNS(model.CMIS_NS, 'cmis:properties')
        entryElement = xmlEntryDoc.getElementsByTagNameNS(model.ATOM_NS, "entry")
        entryElement[0].setAttribute('xmlns:alf', ALFRESCO_NS)
        objectElement = xmlEntryDoc.getElementsByTagNameNS(model.CMISRA_NS, 'object')
        propertiesElement = xmlEntryDoc.createElementNS(model.CMIS_NS, 'cmis:properties')
        objectElement[0].appendChild(propertiesElement)
        setAspectsElement = xmlEntryDoc.createElementNS(ALFRESCO_NS, SET_ASPECTS)
        propertiesElement.appendChild(setAspectsElement)
        
        if addAspects:
            addAspectElement = xmlEntryDoc.createElementNS(ALFRESCO_NS, ASPECTS_TO_ADD)
            valText = xmlEntryDoc.createTextNode(addAspects)
            addAspectElement.appendChild(valText)
            setAspectsElement.appendChild(addAspectElement)
        
        if removeAspects:
            removeAspectElement = xmlEntryDoc.createElementNS(ALFRESCO_NS, ASPECTS_TO_REMOVE)
            valText = xmlEntryDoc.createTextNode(removeAspects)
            removeAspectElement.appendChild(valText)
            setAspectsElement.appendChild(removeAspectElement)
        
        updatedXmlDoc = self._cmisClient.put(selfUrl.encode('utf-8'),
                                             xmlEntryDoc.toxml(encoding='utf-8'),
                                             model.ATOM_XML_TYPE)
    
        self.xmlDoc = updatedXmlDoc
        self._initData()

def addAspect(self, arg):
    if arg is not None:
        aspect_id = arg
        if isinstance(arg, model.ObjectType):
            aspect_id = arg.getTypeId()
        self._updateAspects(addAspects=aspect_id)

def removeAspect(self, arg):
    if arg is not None:
        aspect_id = arg
        if isinstance(arg, model.ObjectType):
            aspect_id = arg.getTypeId()
        self._updateAspects(removeAspects=aspect_id)

# Types' hooks
model.Document._initData = _initData
model.Document._findAlfrescoExtensions = _findAlfrescoExtensions
model.Document.hasAspect = hasAspect
model.Document.getAspects = getAspects
model.Document.findAspect = findAspect
model.Document._updateAspects = _updateAspects
model.Document.addAspect = addAspect
model.Document.removeAspect = removeAspect

model.Folder._initData = _initData
model.Folder._findAlfrescoExtensions = _findAlfrescoExtensions
model.Folder.hasAspect = hasAspect
model.Folder.getAspects = getAspects
model.Folder.findAspect = findAspect
model.Folder._updateAspects = _updateAspects
model.Folder.addAspect = addAspect
model.Folder.removeAspect = removeAspect
