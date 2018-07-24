import xml.dom.minidom

dom = xml.dom.minidom.parse("fare_rules.xml")
book = xml.dom.minidom.parse("booking.xml")

dom.normalize()
book.normalize()

#FARE-RULES
SubSection = dom.getElementsByTagName("SubSection")[5]

#print("name = " + SubSection.nodeName)
#print("SubTitle = " + SubSection.getAttribute("SubTitle"))

Paragraph = SubSection.getElementsByTagName("Paragraph")[0]

Text = Paragraph.getElementsByTagName("Text")[0]
print("text = " + Text.firstChild.nodeValue)

#BOOKING
Status = book.getElementsByTagName("Status")[2]

#print("name = " + Status.nodeName)
print("value = " + Status.childNodes[0].nodeValue)
