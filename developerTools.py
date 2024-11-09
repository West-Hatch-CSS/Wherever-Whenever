import npcStructure, pickle

toolsMenu = """Here are the following tools we can use to automate some things:
    1. NPC Maker
    2. View all NPC Data
    
Pick an option by typing the number:"""

print(toolsMenu)
tool = int(input())

if tool == 1:
    npcFile = open("NPCs.pkl", "rb")
    npcDatabase = pickle.load(npcFile)
    npcFile.close()
    

    newNPC = npcStructure.NPC.automateMakingNPC()
    npcDatabase.append(newNPC)

    npcFile = open("NPCs.pkl", "wb")
    pickle.dump(npcDatabase, npcFile)
    npcFile.close()
elif tool == 2:
    npcFile = open("NPCs.pkl", "rb")
    npcDatabase = pickle.load(npcFile)
    npcFile.close()

    for thisNPC in npcDatabase:
        print("")
        print("-----------------------")
        print("Name:", thisNPC.name)

        numConversations = len(thisNPC.conversations)
        print("No. of conversations:", numConversations)

        if numConversations > 0:
            for thisConversation in thisNPC.conversations:
                print("")
                print("    Conversation Name:", thisConversation.name)
                print("")
                print("    " + thisConversation.text)

                numResponses = len(thisConversation.responses)
                print("    No. of responses:", numResponses)
                if numResponses > 0:
                    for thisResponse in thisConversation.responses:
                        print("")
                        print("        Possible Reply:", thisResponse.responseText)
                        print("        Following Conversation:", thisResponse.nextConversation)