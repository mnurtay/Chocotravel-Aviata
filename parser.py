import xml.dom.minidom

dom = xml.dom.minidom.parse("fare_rules.xml")

dom.normalize()

SubSection = dom.getElementsByTagName("SubSection")[5]

print("name = " + SubSection.nodeName)
print("SubTitle = " + SubSection.getAttribute("SubTitle"))

Paragraph = SubSection.getElementsByTagName("Paragraph")[0]

Text = Paragraph.getElementsByTagName("Text")[0]
print("text = " + Text.firstChild.nodeValue)
