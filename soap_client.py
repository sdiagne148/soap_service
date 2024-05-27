# coding=utf-8
""" Suds Client caches WSDL file or URL for one day by default, 
so I added cache=NoCache() into its constructure to apply every changes when I edit SOAP application. """
from suds.client import Client
from suds.cache import NoCache

my_client = Client('http://127.0.0.1:8000/soap_service/?WSDL', cache=NoCache())
print(my_client)
print ('Function create_compte: ', my_client.service.create_compte(20000,'2024-05-23','dépot via client python'))
print ('Function add: ', my_client.service.add(10, 20))