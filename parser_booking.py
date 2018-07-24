import xml.dom.minidom

dom = xml.dom.minidom.parse("booking.xml")

dom.normalize()

Status = dom.getElementsByTagName("Status")[2]

print("name = " + Status.nodeName)
print("value =" + Status.childNodes[0].nodeValue)


