import inspect
from string import Template
def pp(var_name,env,comment=""):
    thisframe=inspect.currentframe()
    callerFrame=thisframe.f_back
    callerName=callerFrame.f_code.co_name
    value=eval(var_name,env)
    text=Template("${n} = ${v}\n type: ${t}").substitute(
            n=var_name,
            v=value,
            t=type(value))
    printOut(callerName,text)
    

def pe(strng,env,comment=""):
    # this function is just nice for debugging
    # it prints out the variable along with its 
    # name.
    thisframe=inspect.currentframe()
    callerFrame=thisframe.f_back
    callerName=callerFrame.f_code.co_name
    value=eval(strng,env)
    text=Template("${n} = ${v}\n type: ${t}").substitute(
            n=strng,
            v=value,
            t=type(value))
    printOut(callerName,text)

def printOut(callerName,txt):
    print('############################################')
    print(Template("in function: ${cn}").substitute(cn=callerName))
    print(txt)
    print('############################################')

def warning(txt):
    print('############################################')
    calling_frame=inspect.getouterframes(inspect.currentframe(),2)
    func_name=calling_frame[1][3]
    print("Warning in function {0}:".format(func_name))
    print(txt)

def deprecation_warning(txt):
    print('############################################')
    calling_frame=inspect.getouterframes(inspect.currentframe(),2)
    func_name=calling_frame[1][3]
    print("The function {0} is deprecated".format(func_name))
    print(txt)
