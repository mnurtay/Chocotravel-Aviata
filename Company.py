import xml.dom.minidom

from getStatus import Status

class Company:

    booking = ""
    fareRule = ""
    nameCompamy = ""
    totalFare = 0
    baseFare = 0
    taxes = []

    def __init__(self):
        self.booking = self.__get_xml_dom("booking")
        self.fareRule = self.__get_xml_dom("fare_rules1")

        self.nameCompamy = self.__get_name()
        self.totalFare = self.__get_total_fare()
        self.baseFare = self.__get_base_fare()

        self.taxes = self.__get_taxes()

    def __get_name(self):
        return self.booking.getElementsByTagName("OperatingAirline")[1].firstChild.nodeValue

    def __get_total_fare(self):
        return self.booking.getElementsByTagName("TotalFare")[2].firstChild.nodeValue

    def __get_base_fare(self):
        return self.booking.getElementsByTagName("BaseFare")[1].attributes.item(0).value

    def __get_taxes(self):
        taxes = self.booking.getElementsByTagName("Taxes")[1]

        listt = []

        for tax in taxes.childNodes:
            if tax.nodeType != tax.TEXT_NODE:
                arr = []
                arr.append(tax.childNodes[3].firstChild.nodeValue)
                arr.append(tax.childNodes[5].firstChild.nodeValue)
                listt.append(arr)
            
        return listt
        # for tax in taxes.childNodes:
        #     print(tax.childNodes[0].nodeValue)
    
    def __get_xml_dom(self, file_name):								# get dom_object from xml_file
        xml_dom = xml.dom.minidom.parse(file_name + '.xml')
        xml_dom.normalize()

        return xml_dom
    
    def __get_status(self):							# get current status from booking.xml dom
        departureDate = self.booking.getElementsByTagName("DepartureDate")[0]
        status = Status(departureDate.firstChild.nodeValue)

        return status.get()
    
    def __get_rules(self, xml_dom):								# get fare_rule_text from fare_rules.xml dom_object
        subSection = xml_dom.getElementsByTagName("SubSection")[5]

        # print("name = " + SubSection.nodeName)
        # print("SubTitle = " + SubSection.getAttribute("SubTitle"))

        paragraph = subSection.getElementsByTagName("Paragraph")[0]
        rules = paragraph.getElementsByTagName("Text")[0]

        return rules.firstChild.nodeValue

    def calculate(self):
        if not self.__get_status():
            return "Status was not open"

        return self.taxes






