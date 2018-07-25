import xml.dom.minidom

def get_status(xml_dom):										# get current status fro booking.xml dom
	status = xml_dom.getElementsByTagName("Status")[2]

	# print("name = " + Status.nodeName)

	status = status.childNodes[0].nodeValue

	return status


def get_rules(xml_dom):											# get fare rule text from fare_rules.xml dom
	subSection = xml_dom.getElementsByTagName("SubSection")[5]

	# print("name = " + SubSection.nodeName)
	# print("SubTitle = " + SubSection.getAttribute("SubTitle"))

	paragraph = subSection.getElementsByTagName("Paragraph")[0]

	rules = paragraph.getElementsByTagName("Text")[0]
	
	return rules.firstChild.nodeValue

def get_xml_dom(text):											# get dom object from xml file
	xml_dom = xml.dom.minidom.parse(text + '.xml')
	xml_dom.normalize()

	return xml_dom

def main():
	fare_rules = get_xml_dom('fare_rules')
	booking = get_xml_dom('booking')

	print(get_rules(fare_rules))

	print(get_status(booking))

if __name__ == '__main__':
	main()