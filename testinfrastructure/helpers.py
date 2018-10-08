def pp(strng,env,comment=""):
    pe(strng,env,comment)
    

def pe(strng,env,comment=""):
    print('############################################')
    print(comment+"\n"+strng+"=:")
    print(eval(strng,env))
    print('############################################')

