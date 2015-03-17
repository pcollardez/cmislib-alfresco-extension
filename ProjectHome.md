# Alfresco cmislib Extension #

Aspects are an essential tool to model metadata in [Alfresco](http://www.alfresco.com/). The CMIS specification does not define aspects or something similar, but it defines several extension points. Alfresco uses these extensions point to send aspect data back and forth between a CMIS client and the server.

CMIS extensions are XML fragments placed in different parts of a CMIS object. The Alfresco aspect fragments are documented on the [Alfresco Wiki](http://wiki.alfresco.com/wiki/CMIS#Aspect_Support). So, theoretically, they are available to all CMIS clients out there including cmislib.

In reality, dealing with CMIS extensions isn't fun and can require quite a lot of code. cmislib does all the XML parsing for you but, since it doesn't know anything about aspects, it can't provide pretty interfaces.

That's where the "Alfresco cmislib Extension" steps in. It seamlessly merges aspect properties with object properties and provides interfaces to get, add and remove aspects.

## Setting it up ##

The "Alfresco cmislib Extension (Release 0.3.2)" requires cmislib 0.5.1.
If you use [easy\_install](http://peak.telecommunity.com/DevCenter/EasyInstall), this requirement will be automatically satisfied.

The extension dynamically injects new methods in cmislib objects.
To activate the extension, simply import cmislibalf.

```
# The following import injects new methods into cmislib classes
import cmislibalf
from cmislib import CmisClient

cmisClient = CmisClient("http://localhost:8080/alfresco/service/cmis", "admin", "admin")
repo = cmisClient.getDefaultRepository()
aDoc = repo.getObjectByPath('/someFolder/aDoc')

# documents and folders have new methods related to aspects
if (len(aDoc.getAspects()) > 0) and aDoc.hasAspect('P:cm:summarizable'):
    aspect = aDoc.findAspect('cm:summarizable')
    # aspects' properties are mixed with regular properties
    if aDoc.getProperties()['cm:summary'] == "some summary":
        ...
    ...
    aDoc.removeAspect('P:cm:summarizable')
else:
    aDoc.addAspect('P:cm:summarizable')
    props = {'cm:summary': 'some summary'}
    aDoc.updateProperties(props)
    ...
```