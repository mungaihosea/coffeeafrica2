import hashlib
from hashlib import sha256
import time
import json
import pprint
import os
from . import utils
verbose = False

'''
    This is the Main BlockChain System App, it contains the essenstial classes that
    define how a given block behaves and is represented.
    The Genesis block is the initial block in any chain. it's considered to be of no effect and
    thus its hash calculation is insignificant though removing it renders all other blocks invalid

    the Block Class defines the Basic Block and the BlockChain class allows you to define
    a chain which can have multiple blocks. this chain can be saved using a unique index.
'''

class Genesis_Block:
    def __init__(self):
        self.index = 0
        self.hash = '0'
        self.data_dic = {'blockType': 'Genesis Block'}
        self.dificulty = 0
        self.nonce = 0
        self.previoushash = None

    def get_hash(self):
        my_hasher = sha256(
            str(self.index).encode('utf-8')+ str(self.nonce).encode('utf-8') + str(self.previoushash).encode('utf-8') + str(self.data_dic).encode('utf-8'))
        self.hash = my_hasher.hexdigest()
        limit_sample = self.get_crunch_sample(self.dificulty, self.hash)
        while not self.checkWork(limit_sample):
            self.hash = my_hasher.hexdigest()
            limit_sample = self.get_crunch_sample(self.dificulty, self.hash)
            self.nonce += 1
            
            my_hasher.update(str(self.index).encode('utf-8')+ str(self.nonce).encode('utf-8') + str(self.previoushash).encode('utf-8') + str(self.data_dic).encode('utf-8'))
        return self.hash

    def get_crunch_sample(self, dificulty, hash):
        charlist = []
        for n in range(dificulty):
            charlist.append(hash[n])
            n += 1
        return charlist
    # this method is used to confirm that the given hash sample has attained the minimal
    # amount of values requied by the system
    def checkWork(self, hash_sample):
        truth_table = []
        for _ in range(len(hash_sample)):
            truth_table.append(1)

        for x in range(len(truth_table)):
            if hash_sample[x] == '0':
                truth_table[x] = 0
            elif hash_sample[x] != '0':
                truth_table[x] = 1
        if sum(truth_table) != 0:
            return False
        else:
            return True

    def log_block(self):
        info = {
            "index": self.index,
            "previous_hash":self.previoushash,
            "data":self.data_dic,
            "nonce":self.nonce,
            "hash":self.hash
        }
        if verbose:
            print("\n.....................")
            print('Block :', self.index)
            print('Previous Hash :', self.previoushash)
            print('Data :', self.data_dic)
            print('mining dificulty:', self.dificulty)
            print('work level: ', self.nonce)
            print('hash: ', self.hash)
            print("......................")
        return info

    def get_block_dic(self):
        dic = {
            'index': self.index,
            'previous hash': self.previoushash,
            'dificulty': self.dificulty,
            'work level': self.nonce,
            'data': self.data_dic,
            'hash': self.hash
        }
        return dic


class Block:
    def __init__(self, index, data_dic, previoushash):
        self.index = index
        self.previoushash = previoushash
        self.data_dic = data_dic
        self.nonce = 0
        self.hash = ''
        # anything above 4 takes 3+ min to mine
        self.dificulty = 3

    def get_hash(self):
        self.nonce = 0
        my_hasher = sha256(
            str(self.index).encode('utf-8') +str(self.nonce).encode('utf-8') + str(self.previoushash).encode('utf-8') + str(self.data_dic).encode('utf-8'))
        self.hash = my_hasher.hexdigest()
        limit_sample = self.get_crunch_sample(self.dificulty, self.hash)
        if not self.checkWork(limit_sample): 
            while not self.checkWork(limit_sample):
                self.hash = my_hasher.hexdigest()
                limit_sample = self.get_crunch_sample(self.dificulty, self.hash)
                self.nonce += 1
                my_hasher.update(str(self.index).encode('utf-8') + str(self.nonce).encode('utf-8') + str(self.previoushash).encode('utf-8') + str(self.data_dic).encode('utf-8'))
        else:
            if verbose:
              print("[+]valid hash found: " + self.hash)
            return self.hash
        return self.hash

    def get_crunch_sample(self, dificulty, hash):
        charlist = []
        for n in range(dificulty):
            charlist.append(hash[n])
            n += 1
        return charlist

    def checkWork(self, hash_sample):
        truth_table = []
        for _ in range(len(hash_sample)):
            truth_table.append(1)

        for x in range(len(truth_table)):
            if hash_sample[x] == '0':
                truth_table[x] = 0
            elif hash_sample[x] != '0':
                truth_table[x] = 1
        if sum(truth_table) != 0:
            return False
        else:
            return True
    def isValid(self):
        myhash = self.hash
        newhash = self.get_hash()
        if myhash == newhash:
            return True
        else:
            return False
    def log_block(self):
        info = {
            "index": self.index,
            "previous_hash":self.previoushash,
            "data":self.data_dic,
            "nonce":self.nonce,
            "hash":self.hash
        }
        if verbose:
            print("\n.....................")
            print('Block :', self.index)
            print('Previous Hash :', self.previoushash)
            print('Data :', self.data_dic)
            print('mining dificulty:', self.dificulty)
            print('work level: ', self.nonce)
            print('hash: ', self.hash)
            print("......................")
        return info

    def set_dificulty(self, int_value):
        self.dificulty = int_value

    def get_block_dic(self):
        dic = {
            "index": self.index,
            "previous hash": self.previoushash,
            "dificulty": self.dificulty,
            "work level": self.nonce,
            "data": self.data_dic,
            "hash": self.hash
        }
        return dic


class Block_Chain:
    def __init__(self):
        self.lenght = 0
        self.chain = []
        self.raw_chain = []

    def addBlock(self, data_dic, difficulty):
        if self.lenght == 0:
            genblock = Genesis_Block()
            genblock.get_hash()
            prevhash = genblock.hash
            self.lenght += 1
            self.chain.append(genblock)
        else:
            prevhash = self.chain[self.lenght-1].hash
        if verbose:
            print("\n[*]Adding Block " + str(self.lenght) + " to chain...")
            print('[*]Calculating Hash...')
        block = Block(self.lenght, data_dic, prevhash)
        block.set_dificulty(difficulty)
        block.get_hash()
        self.chain.append(block)
        self.lenght += 1
        return block

    def ValidateChain(self):
        limit = len(self.chain)
        if verbose:
            print("\n[*]CHECKING CHAIN VALIDITY")
        while limit >= 1:
            current_block = self.chain[limit-1]
            current_block_hash = self.chain[limit - 1].hash
            actualhash = current_block.get_hash()
            if current_block_hash != current_block.get_hash():
                # hash mismatch
                if verbose:
                    print('[!]INTEGRITY ERROR: hash mismatch at block',
                      self.chain[limit - 1].index, 'in the chain')
                    print('[-]CURRENT HASH ----> ' + current_block_hash +'\n   ACTUAL HASH  ----> '+ actualhash)
                return False
            previous_block_hash = self.chain[limit-2].hash
            apparent_previous_block_hash = self.chain[limit-1].previoushash
            if previous_block_hash != apparent_previous_block_hash:
                # wrong pointer
                if self.chain[limit-1].index == 0:
                    if verbose:
                        print("[+]Hashes Valid")
                else:
                    if verbose:
                        print('[!]invalid block', self.chain[limit-1].index)
                    return False
            limit -= 1
        sequence = [0, 1, 2, 3]
        state = False
        for block in self.chain:
            #Pending
            if block.index == 1:
                if block.data_dic.get('status') == sequence[0]:
                    state = True
                else:
                    state = False
            #Approved
            elif block.index == 2:
                if block.data_dic.get('status') == sequence[1]:
                    state = True
                else:
                    state = False
            #Processed
            elif block.index == 3:
                if block.data_dic.get('status') == sequence[2]:
                    state = True
                else:
                    state = False
            #Arrived
            elif block.index == 4:
                if block.data_dic.get('status') == sequence[3]:
                    state = True
                else:
                    state = False
        if state:
            if verbose:
                print('[+]Block Flow Valid')
        else:
            if verbose:
                print('[!]Block Flow invalid')
        return state

    def addRawBlock(self, block):
        self.chain.append(block)

    def getChainList(self):
        listL = []
        for block in self.chain:
            info = block.get_block_dic()
            listL.append(info)
        listL = json.dumps(listL, indent=4)
        return listL

    def DumpChain(self, filename):
        path = __file__
        path = os.path.join(os.path.dirname(path), 'Chains')
        path = os.path.join(path,filename)
        isFile = os.path.isfile(path+'.json')
        try:
            file = open(path+'.json', 'w')
            for block in self.chain:
                self.raw_chain.append(block.get_block_dic())
            data = json.dumps(self.raw_chain, indent=4)
            if isFile:
                print(f"[+]BLOCK-CHAIN (Update)------> [transaction pk : {filename}]")
            else:
                print(f"[+]BLOCK-CHAIN (Create)------> [transaction pk : {filename}]")
            file.writelines(data)
        except:
            pass

    def GetChainFromFile(self, file_name):
        path = __file__
        path = os.path.join(os.path.dirname(path), 'Chains')
        path = os.path.join(path,file_name)
        try:
            file = open(path + '.json')
        except:
            return 'Error No such Chain'
        data = file.readlines()
        string = ''
        for line in data:
            string = string + line
        
        data = string
        a = json.JSONDecoder()
        chain = a.decode(data)
        n = len(chain)-1
        x = 0
        try:
            while x <= n:
                block = chain[x]
                data = chain[x].get('data')

                keys = data.keys()
                data2 = {}
                for key in keys:
                    valuekey = str(key)
                    if 'id' in key:
                        try:
                            data2[valuekey] = int(data.get(key))
                        except:
                            data2[valuekey] = str(data.get(key))
                    else:
                        try:
                            int(data.get(key))
                            data2[valuekey] = int(data.get(key))
                        except:
                            data2[valuekey] = str(data.get(key))
                previoushash = str(block.get('previous hash'))
                myhash = str(block.get('hash'))
                index = int(block.get('index'))
                nonce = int(block.get('work level'))
                dificulty = int(block.get('dificulty'))

                if index == 0:
                    blockTemplate = Genesis_Block()
                    blockTemplate.get_hash()
                else:
                    blockTemplate = Block(index, data, previoushash)
                    blockTemplate.hash = myhash
                    blockTemplate.dificulty = dificulty
                    blockTemplate.data_dic = data
                    blockTemplate.nonce = nonce
                self.addRawBlock(blockTemplate)
                x += 1
                self.lenght +=1
        except:
            return None
    

def setVerbosity(boolValue):
    global verbose
    verbose = boolValue
        
