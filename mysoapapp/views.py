# mysoapapp/views.py
from spyne import Application, rpc, ServiceBase, Integer, Date, Unicode, ComplexModel, Array
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from django.views.decorators.csrf import csrf_exempt

# In-memory storage for Items
items = {}
current_id = 1

# Define the Compte model
class Compte(ComplexModel):
    id = Integer
    solde = Integer
    dateCreation = Date
    description = Unicode

class SoapService(ServiceBase):
    @rpc(Integer, Integer, _returns=Integer)
    def add(ctx, a, b):
        return a + b
    
    @rpc(Integer(nillable=False), Date, Unicode, _returns=Compte)
    def create_compte(ctx, solde, dateCreation, description):
        global current_id
        item = Compte(id=current_id, solde=solde, dateCreation= dateCreation, description=description)
        items[current_id] = item
        current_id += 1
        return item

    @rpc(Integer(nillable=False), _returns=Compte)
    def get_compte(ctx, id):
        return items.get(id)

    @rpc(Integer(nillable=False), Integer(nillable=False), Date, Unicode, _returns=Compte)
    def update_compte(ctx, id, solde, dateCreation, description):
        if id in items:
            items[id].solde = solde
            items[id].dateCreation = dateCreation
            items[id].description = description
            return items[id]
        else:
            return None

    @rpc(Integer(nillable=False), _returns=Unicode)
    def delete_compte(ctx, id):
        if id in items:
            del items[id]
            return "Compte deleted"
        else:
            return "Compte not found"
        
    @rpc(Integer(nillable=False), _returns=Compte)
    def conversionEuroToDh(ctx, amount):
        return 11 * amount
    
    @rpc(_returns=Array(Compte))
    def get_comptes(ctx):
      return list(items.values())

soap_app = Application([SoapService],
    tns='mysoapapp.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(),
)

django_soap_app = DjangoApplication(soap_app)
my_soap_application = csrf_exempt(django_soap_app)
