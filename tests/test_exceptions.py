import unittest
from pywps.app import Process, Service, xpath_ns, WPS, OWS
from tests.common import client_for
import lxml.etree



class ExceptionsTest(unittest.TestCase):

    def setUp(self):
        self.client = client_for(Service(processes=[]))

    def test_invalid_parameter_value(self):
        resp = self.client.get('?service=wms')
        exception_el = resp.xpath('/ows:ExceptionReport/ows:Exception')[0]
        assert exception_el.attrib['exceptionCode'] == 'OperationNotSupported'
        assert resp.status_code == 501
        assert resp.headers['Content-Type'] == 'text/xml'

    def test_missing_parameter_value(self):
        resp = self.client.get()
        exception_el = resp.xpath('/ows:ExceptionReport/ows:Exception')[0]
        assert exception_el.attrib['exceptionCode'] == 'MissingParameterValue'
        assert resp.status_code == 400
        assert resp.headers['Content-Type'] == 'text/xml'

    def test_missing_request(self):
        resp = self.client.get("?service=wps")
        exception_el = resp.xpath('/ows:ExceptionReport/ows:Exception/ows:ExceptionText')[0]
        assert exception_el.text == 'request'
        assert resp.headers['Content-Type'] == 'text/xml'

    def test_bad_request(self):
        resp = self.client.get("?service=wps&request=xyz")
        exception_el = resp.xpath('/ows:ExceptionReport/ows:Exception')[0]
        assert exception_el.attrib['exceptionCode'] == 'InvalidParameterValue'
        assert resp.headers['Content-Type'] == 'text/xml'

def load_tests(loader=None, tests=None, pattern=None):
    if not loader:
        loader = unittest.TestLoader()
    suite_list = [
        loader.loadTestsFromTestCase(ExceptionsTest),
    ]
    return unittest.TestSuite(suite_list)
