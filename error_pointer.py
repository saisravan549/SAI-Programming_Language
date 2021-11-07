
def make_pointer(pos,text):
    text=text[0:pos+1]
    text+=' <--'
    return text
def parse_pointer(index,tokens):
    text=''
    for i in range(0,index):
        if tokens[i].token_value !=None:
            
            text+=' '+str(tokens[i].token_value)
        else:
            
            if tokens[i].token_type =='ADD':
                text+=' '+'P'
            elif tokens[i].token_type =='MUL':
                text+=' '+'L'
            elif tokens[i].token_type =='DIV':
                text+=' '+'D'
            elif tokens[i].token_type =='SUB':
                text+=' '+'M'
            elif tokens[i].token_type =='LPARA':
                text+=' '+'('
            elif tokens[i].token_type =='RPARA':
                text+=' '+')'
            elif tokens[i].token_type =='POW':
                text+=' '+'^'
            elif tokens[i].token_type =='eq':
                text+=' '+'='
            elif tokens[i].token_type =='GT':
                text+=' '+'>'
            elif tokens[i].token_type =='LT':
                text+=' '+'<'
            elif tokens[i].token_type =='GE':
                text+=' '+'>~'
            elif tokens[i].token_type =='LE':
                text+=' '+'<~'
            elif tokens[i].token_type =='EE':
                text+=' '+'~'
            elif tokens[i].token_type =='colon':
                text+=' '+':'
            elif tokens[i].token_type =='comma':
                text+=' '+','
            
            
    return text + ' <--'
        