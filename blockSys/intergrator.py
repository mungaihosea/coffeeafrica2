try:
    from .blockApp import Block_Chain
except:
    from .blockApp import Block_Chain
import time

'''
    This File is the linker or intergrator of the order concept and the underlying blockapp
    without it, there is no connection, use the Chain_Model to design your transaction models
    and the methods attached to perform more functions
    allways remember to dump a chain after editing it from a file
'''


class Chain_Model:
    def __init__(self):
        self.blockchain = Block_Chain()

    def addTochain(self, order_object):
        date_placed = order_object.date_placed
        order_id = order_object.pk
        buyer = order_object.buyer.pk
        employee = order_object.employee.pk
        auction = order_object.auction.pk
        expected_date = order_object.expected_date
        try:
            expected_date = f"{expected_date.year}/{expected_date.month}/{expected_date.day}"
        except:
            pass
        amount = order_object.amount
        status = order_object.status
        shipping_address = order_object.shipping_address
        shipment_id =order_object.shipment_id

        data = {
            'id': order_id,
            'auction_id': auction,
            'amount': amount,
            'status': status,
            'date_placed': f"{date_placed.year}/{date_placed.month}/{date_placed.day}",
            'expected_date': expected_date,
            'buyer': buyer,
            'employee': employee,
            'shipping_address': shipping_address,
            'shipping_id': shipment_id
        }

        self.blockchain.addBlock(data, 2)
    def DumpChain(self, chain_id):
        #if a similar chain exists its overwritten
        self.blockchain.DumpChain(str(chain_id))
    
    def CheckValidity(self):
        return self.blockchain.ValidateChain()
    
    def getChainDataAsList(self):
        return self.blockchain.chain
    
    def getBlockById(self, id):
        try:
            block = self.blockchain.chain[id]
            return block
        except:
            return None
    
    def getBlockStatus(self, id):
        try:
            status = {}
            status['value'] = self.blockchain.chain[id].data_dic.get('status')
            f = self.blockchain.chain[id].data_dic.get('status')
            if f == 0:
                status['info'] = 'sent'
            elif f == 1:
                status['info'] = 'pending'
            elif f == 2:
                status['info'] = 'accepted'
            elif f == 3:
                status['info'] = 'processed'
            return status
        except:
            return None

    def deleteBlock(self, id):
        try:
            block = self.blockchain.chain[id]
            self.blockchain.chain.remove(block)
        except:
            print(Warning("id not available"))
    
    def FlushChain(self):
        self.blockchain.chain.clear()
    
    def enumerate(self):
        print(self.blockchain.__dict__)
        return self.blockchain.__dict__
    def getBlockData(self, id):
        try:
            block = self.blockchain.chain[id]
            return block.data_dic
        except:
            return None


def ReadChainFromFile(chain_id):
    chain_id = str(chain_id)
    chain = Chain_Model()
    chain.blockchain.GetChainFromFile(chain_id)
    return chain
