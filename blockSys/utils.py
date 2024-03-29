import os

try:
    from . import blockApp
    from . import intergrator
except:
    from . import blockApp
    from . import intergrator
import time

BASE_DIR = os.path.dirname(__file__)

"""
    This file defines some top level utility methods that you can perform on the
    underlying blockchains, each block chain is represented by a single file in the 
    Chains folder, PLEASE AVOID interacting with the files directly-this may make the blocks
    invalid.
    always keep a back-up of the chains on a separate computer
"""


def GetAllChainsAsList():
    path = os.path.join(os.path.dirname(__file__), "Chains")
    chains = os.listdir(path)
    chain_list = []
    for chain in chains:
        chain = intergrator.ReadChainFromFile(chain.strip(".json"))
        chain_list.append(chain)
    return chain_list


def ValidateAllChains():
    path = os.path.join(os.path.dirname(__file__), "Chains")
    chains = os.listdir(path)
    Allvalid = True
    infolist = []
    for chain in chains:
        chainModel = intergrator.ReadChainFromFile(chain.strip(".json"))
        valid = chainModel.CheckValidity()
        if valid:
            dic = {"chain": chainModel, "id": chain.strip(".json"), "valid": True}
            infolist.append(dic)
        else:
            Allvalid = False
            dic = {"chain": chain, "valid": False}
            infolist.append(dic)
    out = {"AllValid": Allvalid, "info": infolist}
    return out


def ClearAllChains():
    path = os.path.join(os.path.dirname(__file__), "Chains")
    chains = os.listdir(path)
    for chain in chains:
        chainModel = intergrator.ReadChainFromFile(chain.strip(".json"))
        chainModel.blockchain.chain.clear()
        chainModel.DumpChain(chain.strip(".json"))


def DeleteAllChains():
    path = os.path.join(os.path.dirname(__file__), "Chains")
    chains = os.listdir(path)
    for chain in chains:
        path_to_chain = os.path.join(BASE_DIR, "Chains")
        path_to_chain = os.path.join(path_to_chain, chain)
        os.remove(path_to_chain)


def DeleteChain(id):
    path = os.path.join(os.path.dirname(__file__), "Chains")
    chains = os.listdir(path)
    for chain in chains:
        if chain.strip(".json") == str(id):
            path_to_chain = os.path.join(BASE_DIR, "Chains")
            path_to_chain = os.path.join(path_to_chain, chain)
            os.remove(path_to_chain)
            return


def getChainViaParty(party_name, target):
    t_chains = []
    print(party_name)
    if target == "buyer":
        chains = GetAllChainsAsList()
        for chain in chains:
            if str(chain.getBlockById(1).data_dic.get("buyer")) == str(party_name):
                t_chains.append(chain)
    return t_chains

