def displayConvo(convo):
    if convo.name == 'start':
        return 'start2'
    elif convo.name == "start":
        return None

def getConversation(conversationName, conversations):
    for x in conversations:
        if x.name == conversationName:
            return (x)

def talkToNPC(conversations):
    convo = getConversation ('start', conversations)
    nextConvo = displayConvo(convo)
    while nextConvo != None:
        convo = getConversation (nextConvo, conversations)
        nextConvo = displayConvo(convo)
           
           