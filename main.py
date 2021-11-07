
import error_pointer as ep
import os

######Lexer######



numbers='0123456789'
addition='ADD'
identifier='ID'
access='access'
keyword='key'
equals='eq'
multiplication='MUL'
division='DIV'
subtraction='SUB'
left_para='LPARA'
right_para='RPARA'
int_sai='INT'
float_sai='FLOAT'
string_sai='string'
lsquare='lsquare'
rsquare='rsquare'
EOF='EOF'
EE='EE'
LE='LE'
GE='GE'
LT='LT'
GT='GT'
NE='NE'
EOL='EOL'
power='POW'
colon="colon"
col='col'
alpha='abcdefghijklmnopqrstuvwxyz'
alpha_numbers=alpha+numbers
comma='comma'

KEYWORDS=['var', 'and','or',
'if','then','elif','else','for','to','step','while','fun','end']
class Token:
    def __init__(self,token_type,token_value=None):
        self.token_type=token_type
        self.token_value=token_value
    def matches(self,type_,value):
        return self.token_type==type_ and self.token_value==value
    def __repr__(self):
        if self.token_value==None:
            return f'{self.token_type}'
        else:
            return f'{self.token_type}:{self.token_value}'
class Error:
    def __init__(self,reason,details=None):
        self.reason=reason
        self.details=details
class IllegalLexingError(Error):
    def __init__(self,details):
        super().__init__('Illegal Lexing: \n')
        self.details=details
        
    def __repr__(self):
        return f'{self.reason} {self.details},'
class IllegalParsingError(Error):
    def __init__(self,details,values):
        super().__init__('Illegal Parsing : \n')
        self.details=details
        self.values=values
    def __repr__(self):
        return f'{self.reason} {self.details}, \'{self.values}\''
class RuntimeError(Error):
    def __init__(self, details,values):
        super().__init__('Runtime Error() - ')
        self.details=details
        self.values=values
    def __repr__(self):
        return f'{self.reason}{self.details},\'{self.values}\''
class DivideByZeroError:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.reason='Illegal Division Operation:\n'
        
    def __repr__(self):
        return f'{self.reason} {self.x},\'{self.y}\''
class ExpectedCharError(Error):
    def __init__(self,details):
        super().__init__('Expected Character "~": \n')
        self.details=details
        
    def __repr__(self):
        return f'{self.reason} {self.details},'
    
class Lexer:
    def __init__(self, text,pos):
        self.text=text
        self.pos=pos
        
        self.line=1
        self.current_char=None
        self.counter()
    def counter(self):
        self.pos+=1
        
        if self.pos<len(self.text):
            self.current_char=self.text[self.pos]
            if self.current_char=='\n':
                self.counter()
                self.line+=1
               
                
        else:
            self.current_char=None
    def make_num(self):
        num=''
        point=0
        while self.current_char!=None and self.current_char in numbers+'.':
            if self.current_char=='.':
                if point==0:
                    point=1
                else:
                    return 'error'
            num+=self.current_char
            self.counter()
        if point==1:
            return Token(float_sai,float(num))
        return Token(int_sai,int(num))
    def make_identifier(self):
        temp_id=''
        while self.current_char !=None and self.current_char in alpha_numbers+'_':
            temp_id+=self.current_char
            self.counter()
        if temp_id in KEYWORDS:
            token_type=keyword
        else:
            token_type=identifier
        
        return Token(token_type,temp_id)
    def make_string(self):
        string=''
        char_sai=False
        self.counter()
        escape_sequences={
            'n':'\n',
            't':'\t'

        }
        while self.current_char!=None and (self.current_char!='"' or char_sai):
            if char_sai:
                string+=escape_sequences.get(self.current_char,self.current_char)
            
            if self.current_char=='\\':
                char_sai=True
            else:

                string+=self.current_char
            self.counter()
            char_sai=False
        self.counter()
        return Token(string_sai,string)





    def make_not_equals(self):
        self.counter()
        if self.current_char=='~':
            self.counter()
            return Token(NE),None
        
        return None, ExpectedCharError(ep.make_pointer(self.pos,self.text))
    def make_less_than(self):
        self.counter()
        if self.current_char=="=":
            self.counter()
            return Token(LE)
        
        return Token(LT)
    def make_greater_than(self):
        self.counter()
        if self.current_char=="=":
            self.counter()
            return Token(GE)
        
        return Token(GT)
    
    def create_tokens(self):
        tokens=[]
        while self.current_char!=None:

            if self.current_char=='P':
                tokens.append(Token(addition))
                self.counter()
            elif self.current_char=='M':
                tokens.append(Token(subtraction))
                self.counter()
            elif self.current_char=='L':
                tokens.append(Token(multiplication))
                self.counter()
            elif self.current_char=='D':
                tokens.append(Token(division))
                self.counter()
            elif self.current_char=='(':
                tokens.append(Token(left_para))
                self.counter()
            elif self.current_char==')':
                tokens.append(Token(right_para))
                self.counter()
            elif self.current_char=='[':
                tokens.append(Token(lsquare))
                self.counter()
            elif self.current_char==']':
                tokens.append(Token(rsquare))
                self.counter()
            elif self.current_char=='=':
                tokens.append(Token(equals))
                self.counter()    

            elif self.current_char=='^':
                tokens.append(Token(power))
                self.counter()
            elif self.current_char in [';', '\n']:
                tokens.append(Token(EOL))
                self.counter()
            elif self.current_char==',':
                tokens.append(Token(comma))
                self.counter()
            elif self.current_char==":":
                tokens.append(Token(colon))
                self.counter()

            elif self.current_char==' ':
                self.counter()
            elif self.current_char in numbers:
                tokens.append(self.make_num())
            elif self.current_char == '"':
                tokens.append(self.make_string())

            elif self.current_char in alpha:
                tokens.append(self.make_identifier())
            elif self.current_char=='!':
                tokie, error=self.make_not_equals()
                if error:
                    return [], error
                tokens.append(tokie)
            elif self.current_char==':':
                tokens.append(Token(col))
                self.counter()

            elif self.current_char=='~':
                tokens.append(Token(EE))
                self.counter()
            elif self.current_char=='?':
                tokens.append(Token(access))
                self.counter()

            elif self.current_char=='<':
                tokens.append(self.make_less_than())
                
            elif self.current_char=='>':
                tokens.append(self.make_greater_than())
            
                
                   
            else:
                return [], IllegalLexingError(ep.make_pointer(self.pos,self.text))   
                #raise an error
        tokens.append(Token(EOF))
        return tokens, None

######Parser######
class StringNode:
    def __init__(self,token,num,line):
        self.token_type=token
        self.num=num
        self.line=line
    def __repr__(self):
        return f'{self.token_type}'
class ListNode:
    def __init__(self,token,num,line):
        self.token_type=token
        self.num=num
        self.line=line

class IdAccessNode:
    def __init__(self, var_name_token,num,line):
        self.var_name_token=var_name_token
        self.num=num
        self.line=line

class Idnode:
    def __init__(self,var_name, mini_expression,num,line):
        self.var_name=var_name
        self.mini_expression=mini_expression
        self.num=num
        self.line=line
class Assign:
    def __init__(self,left_val,right_val,num,line):
        self.left_val=left_val
        self.right_val=right_val
        self.num=num
        self.line=line

class Value:
    def __init__(self,token,num,line):
        self.token_type=token
        self.num=num
        self.line=line
    def __repr__(self):
        return f'{self.token_type}'
class Access:
    def __init__(self,list,i,num,line):
        self.list=list
        self.i=i
        self.num=num
        self.line=line
class Operation:
    def __init__(self,value_left,operator,value_right,num,line):
        self.value_left=value_left
        self.operator=operator
        self.value_right=value_right
        self.num=num
        self.line=line
    def __repr__(self):
        return f'({self.value_left}->{self.operator}->{self.value_right})'

class IfNode:
    def __init__(self,cases,else_case,num,line):
        self.cases=cases
        self.else_case=else_case
        self.num=num
        self.line=line

class ForNode:
    def __init__(self,var_name_tok,start_value_node, end_value_node,step_value_node,body_node,num,line):
        self.var_name_tok=var_name_tok
        self.start_value_node=start_value_node
        self.end_value_node=end_value_node
        self.step_value_node=step_value_node
        self.body_node=body_node
        self.num=num
        self.line=line
class WhileNode:
    def __init__(self,condition_node,body_node,num,line):
        self.condition_node=condition_node
        self.body_node=body_node
        self.num=num
        self.line=line

class FuncDefNode:
    def __init__(self,var_name_tok,arg_name_toks,body_node,num,line):
        self.var_name_tok=var_name_tok
        self.arg_name_toks=arg_name_toks
        self.body_node=body_node
        self.num=num
        self.line=line

class CallNode:
    def __init__(self,node_to_call,arg_nodes,num,line):
        self.node_to_call=node_to_call
        self.arg_node=arg_nodes
        self.num=num
        self.line=line
        

class Condition:
    def __init__(self,left_expression,num,line,operator=None,right_expression=None):
        self.left_expression=left_expression
        self.operator=operator
        self.right_expression=right_expression
        self.num=num
        self.line=line
    def __repr__(self):
        if self.operator==None and self.right_expression==None:
            return f'({self.left_expression})'

        return f'({self.left_expression}->{self.operator}->{self.right_expression})'
class FRun:
    def __init__(self,left,operator,right):
        self.left=left
        self.operator=operator
        self.right=right
        
        
    def __repr__(self):
        return f'({self.left}->{self.operator}->{self.right})'
class SignedVal:
    def __init__(self,op,val,num,line):
        self.op=op
        self.val=val
        self.num=num
        self.line=line
    def __repr__(self):
        return f'{self.op}{self.val}'
class Parser:
    def __init__(self, tokens,a=0):
        self.line=a
        self.token_number=-1
        self.tokens=tokens
        self.move()
        
    def move(self):
        self.token_number+=1
        if self.token_number<len(self.tokens):
            self.current_token=self.tokens[self.token_number]
        return self.current_token
    def for_expr(self):
        if not self.current_token.matches(keyword,'for'):
            return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \'for\')')
        self.move()
        if self.current_token.token_type!=identifier:
            IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \'identifier\')')
        var_name=self.current_token
        self.move()
        if self.current_token.token_type!=EE:
            IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \'=\')')
        self.move()
        start_value=self.final_run()
        if isinstance(start_value,IllegalParsingError):
            return start_value
        if not self.current_token.matches(keyword,'to'):
            IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \'to\')')
        self.move()
        end_value=self.final_run()
        if isinstance(end_value,IllegalParsingError):
            return end_value
        if self.current_token.matches(keyword,'step'):
            self.move()
            step_value=self.final_run()
            if isinstance(step_value,IllegalParsingError):
                return step_value
        else:
            step_value=None
        
        if self.current_token.token_type!=EOL:
            return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Illegal Syntax)')
        self.line+=1
        self.move()

        
        if not self.current_token.matches(keyword,'then'):
            return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \'then\')')

        self.move()
        if  self.current_token.token_type!=EOL:
            return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Illegal Syntax)')
        self.line+=1
        self.move()
        body=[]
        while self.current_token.token_type!=EOF and not self.current_token.matches(keyword,'end'):
            if self.current_token.token_type==EOL:
                self.line+=1
                self.move()
            else:
                result=self.final_run()
                if isinstance(result,IllegalParsingError):
                    return result
                body.append(result)

        if self.current_token.matches(keyword,'end'):
            self.line+=1
            self.move()
        
        
        return ForNode(var_name,start_value,end_value,step_value,body,self.token_number,self.line)
    def func_def(self):
        if not self.current_token.matches(keyword,'fun'):
            return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \'fun\')')
        self.move()
        if self.current_token.token_type==identifier:
            var_name_tok=self.current_token
            self.move()
            if self.current_token.token_type!=left_para:
                return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \'(\')')
        else:
            var_name_tok=None
            if self.current_token.token_type!=left_para:
                return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected identifier or \'(\')')

        self.move()
        arg_name_toks=[]
        if self.current_token.token_type ==identifier:
            arg_name_toks.append(self.current_token)
            self.move()
            while self.current_token.token_type==comma:
                self.move()
                if self.current_token.token_type!=identifier:
                    return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected identifier)')
                arg_name_toks.append(self.current_token)
                self.move()
            if self.current_token.token_type!=right_para:
                return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \')\')')   
        else:
            if self.current_token.token_type!=right_para:
                return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected identifier or \')\')')
        self.move()
        if self.current_token.token_type!=colon:
            return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected  \':\')')
        self.move()
        
        node_to_return=self.final_run()
        if isinstance(node_to_return,IllegalParsingError):
            return node_to_return
        return FuncDefNode(var_name_tok,arg_name_toks,node_to_return,self.token_number,self.line)

    def while_expr(self):
        if not self.current_token.matches(keyword,'while'):
            return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \'while\')')
        self.move()
        condition=self.final_run()
        if isinstance(condition,IllegalParsingError):
            return condition
        if self.current_token.token_type!=EOL:
            return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Illegal Syntax)')
        self.line+=1
        self.move()
        if not self.current_token.matches(keyword,'then'):
            return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \'then\')')
        self.move()
        if self.current_token.token_type!=EOL:
            return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Illegal Syntax)')
        self.line+=1
        self.move()
        body=[]
        while self.current_token.token_type!=EOF and not self.current_token.matches(keyword,'end'):
            if self.current_token.token_type==EOL:
                self.line+=1
                self.move()
            else:
                result=self.final_run()
                if isinstance(result,IllegalParsingError):
                    return result
                body.append(result)
        if self.current_token.matches(keyword,'end'):
            self.line+=1
            self.move()

       
       
        return WhileNode(condition,body,self.token_number,self.line)
    def lis_expr(self):
        
        elements=[]
        if self.current_token.token_type!=lsquare:
            return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \'[\')') 
        self.move()
        if self.current_token.token_type==rsquare:
            self.move()
        else:
            a=self.final_run()
           
            if isinstance(a,IllegalParsingError):
                return a
            elements.append(a)
        
            
            while self.current_token.token_type==comma:
                self.move()
                para_result=self.final_run()
                if isinstance(para_result,IllegalParsingError):
                     return para_result
                elements.append(para_result)

            if self.current_token.token_type!=rsquare:
                return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \')\')')
            self.move()
        return ListNode(elements,self.token_number,self.line)
            
    def if_expr(self):
        cases=[]
        else_case=None
        if not self.current_token.matches(keyword,'if'):
            return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \'if\')')
        self.move()
        condition=self.final_run()
        if isinstance(condition,IllegalParsingError):
            return condition
        elif not isinstance(condition,Condition) and not isinstance(condition,FRun) and not isinstance(condition,Assign):
            condition=Condition(condition,self.token_number,self.line)
        if self.current_token.token_type!=EOL:
            return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Illegal Syntax)')
        self.line+=1
        self.move()

        if not self.current_token.matches(keyword,'then'):
            return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \'then\')')
        self.move()
        if self.current_token.token_type!=EOL:
            return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Illegal Syntax)')
        self.line+=1
        self.move()
        body=[]
        while not self.current_token.matches(keyword,'elif') and not self.current_token.matches(keyword,'else') and not self.current_token.matches(keyword,'end') and self.current_token.token_type!=EOF:
            if self.current_token.token_type==EOL:
                self.line+=1
                self.move()
            else:

                expr=self.final_run()
                if isinstance(expr,IllegalParsingError):
                    return expr
                body.append(expr)
        if self.current_token.matches(keyword,'end'):
            
            self.move()
            cases.append((condition,body))
            return IfNode(cases,else_case,self.token_number,self.line)
        
            
       

        
        cases.append((condition,body))
        
        
        if self.current_token.matches(keyword,'elif'):

            while self.current_token.matches(keyword,'elif'):
                self.move()
           
                condition=self.final_run()
                if isinstance(condition,IllegalParsingError):
                    return condition
                elif not isinstance(condition,Condition) and not isinstance(condition,FRun) and not isinstance(condition,Assign):
                    condition=Condition(condition,self.token_number,self.line)
                if self.current_token.token_type!=EOL:
                    return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Illegal Syntax)')
                self.line+=1
                self.move()
                if not self.current_token.matches(keyword,'then'):
                    return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \'then\')')
                self.move()
                if self.current_token.token_type!=EOL:
                    return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Illegal Syntax)')
                self.line+=1
                self.move()
                body=[]
                while not self.current_token.matches(keyword,'elif') and not self.current_token.matches(keyword,'else') and not self.current_token.matches(keyword,'end') and self.current_token.token_type !=EOF:
                    if self.current_token.token_type==EOL:
                        self.line+=1
                        self.move()
                    else:

                        expr=self.final_run()
                        if isinstance(expr,IllegalParsingError):
                            return expr
                        body.append(expr)
                if self.current_token.matches(keyword,'end'):
                    
                    self.move()
                    cases.append((condition,body)) 
                    return IfNode(cases,else_case,self.token_number,self.line) 
                elif self.current_token.matches(keyword,'elif'):
                    self.line+=1
                    
                elif self.current_token.matches(keyword,'else'):
                    self.line+=1
                    

   
            
               
                cases.append((condition,body))  
           
            
                 
        
        if self.current_token.matches(keyword,'else'):
            self.move()
            if self.current_token.token_type!=EOL:
                return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Illegal Syntax)')
            self.line+=1
            self.move()
            body=[]
            while  not self.current_token.matches(keyword,'end') and self.current_token.token_type !=EOF:
                if self.current_token.token_type==EOL:
                    self.line+=1
                    self.move()
                else:

                    expr=self.final_run()
                    if isinstance(expr,IllegalParsingError):
                        return expr
                    body.append(expr)
            if self.current_token.matches(keyword,'end'):
                self.line+=1
                self.move()
               
            else_case=body
        return IfNode(cases,else_case,self.token_number,self.line)
   

    def call(self):
        fac=self.current_token

        a=self.token_number
        b=self.line
        self.move()
        
        if self.current_token.token_type==left_para:
            self.move()
            arg_nodes=[]
            if self.current_token.token_type==right_para:
                self.move()
            else:
                para_res=self.final_run()
                if isinstance(para_res,IllegalParsingError):
                    return para_res
                arg_nodes.append(para_res)
                while self.current_token.token_type==comma:
                    self.move()
                    para_result=self.final_run()
                    if isinstance(para_result,IllegalParsingError):
                        return para_result
                    arg_nodes.append(para_result)

                if self.current_token.token_type!=right_para:
                    return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \')\')')
                self.move()
            return CallNode(IdAccessNode(fac,a,b),arg_nodes,self.token_number,self.line)
        return IdAccessNode(fac,a,b)

    def gen_factor(self):
        token=self.current_token
        

        if token.token_type in (addition,subtraction):

            op=token.token_type
            
            self.move()
                      
            val=self.gen_factor()
            if not isinstance(val,IllegalParsingError):
                return SignedVal(op,val,self.token_number,self.line)
            else:
                return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected an Int or Float or an Identifier)')
            
        elif token.token_type in (int_sai,float_sai):
            self.move()
            
            return Value(token.token_value,self.token_number,self.line)
        elif token.token_type == string_sai:
            self.move()
            return StringNode(token.token_value,self.token_number,self.line)
        elif token.token_type ==identifier:
            ret=self.call()
            return ret

            
        
        elif token.token_type == left_para:
            self.move()
            res=self.final_run()
            if isinstance(res,IllegalParsingError):
                return res
            if self.current_token.token_type==right_para:
                self.move()
                return res
            else:
                return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected \')\')')
        elif token.token_type==lsquare:
            lis=self.lis_expr()
            return lis



        elif token.matches(keyword,'if'):
            if_expr=self.if_expr()
            return if_expr 
        elif token.matches(keyword,'for'):

            for_expr=self.for_expr()
            return for_expr 
        elif token.matches(keyword,'while'):
            while_expr=self.while_expr()
            return while_expr
        elif token.matches(keyword,'fun'):
            func_def=self.func_def()
            return func_def
        
        


       

            
            
               
        return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected an Int or Float or an Identifier)')
    
    def gen_term(self):
        left_value=self.gen_factor()
        if isinstance(left_value,IllegalParsingError):
            return left_value
        if self.current_token.token_type ==access:
            self.move()
            
            i=self.gen_factor()
            self.move()
            

            return Access(left_value,i,self.token_number,self.line)
           
        
        
        
        while self.current_token.token_type in (multiplication,division,power):
            operator=self.current_token.token_type
            self.move()
            right_value=self.gen_factor()
            if isinstance(right_value,IllegalParsingError):

                return right_value

            left_value=Operation(left_value,operator,right_value,self.token_number,self.line)
       

        return left_value
    def gen_expression(self):
        #if self.current_token.matches(keyword,'var'):
         #   self.move()
          #  if self.current_token.token_type != identifier:
           #     return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected Identifier)')
           # var_name=self.current_token
            #self.move()
            #if self.current_token.token_type!=equals:
             #   return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected an Assignment)')
            #self.move()
            #mini_expression=self.gen_expression()
            #if isinstance(mini_expression,IllegalParsingError):
             #   return mini_expression
            #return Idnode(var_name,mini_expression, self.token_number,self.line)
       
        






        left_value=self.gen_term()
        if isinstance(left_value,IllegalParsingError):
            return left_value
        #while self.current_token.token_type ==equals :
         #   self.move()
          #  expr=self.gen_expression()
           # if isinstance(expr,IllegalParsingError):
            #    return expr

            #return Assign(left_value,expr,self.token_number,self.line)
        

            
       
        while self.current_token.token_type in (addition,subtraction):
            operator=self.current_token.token_type
            self.move()
            right_value=self.gen_term()
            if isinstance(right_value,IllegalParsingError):
                return right_value
            left_value= Operation(left_value,operator,right_value,self.token_number,self.line)
        
        return left_value
    
    def conditional_expressions(self):
        
        
        
        left_expression=self.gen_expression()
        if isinstance(left_expression,IllegalParsingError):
            return left_expression
      
        while self.current_token.token_type in (EE, LE, GE, LT,GT, NE):
            operation=self.current_token.token_type
            self.move()
            right_expression=self.gen_expression()
            if isinstance(right_expression,IllegalParsingError):
                return right_expression
            left_expression = Condition(left_expression,self.token_number,self.line,operation,right_expression) 
        
        
        return left_expression
    def final_run(self):
        if self.current_token.matches(keyword,'var'):
            self.move()
            if self.current_token.token_type != identifier:
                return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected Identifier)')
            var_name=self.current_token
            self.move()
            if self.current_token.token_type!=equals:
                return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected an Assignment)')
            self.move()
            mini_expression=self.final_run()
            if isinstance(mini_expression,IllegalParsingError):
                return mini_expression
            
            return Idnode(var_name,mini_expression, self.token_number,self.line)
        
            

            
        left=self.conditional_expressions()
        if isinstance(left,IllegalParsingError):
            return left
        while self.current_token.token_type ==equals :
            self.move()
            expr=self.final_run()
            if isinstance(expr,IllegalParsingError):
                return expr

            return Assign(left,expr,self.token_number,self.line)
        while self.current_token.token_value in ('and','or'):
            operation=self.current_token.token_value
            self.move()
            right=self.conditional_expressions()
            if isinstance(right,IllegalParsingError):
                return right
            left=FRun(left,operation,right)
       
        return left

    def parse(self):
        output=self.final_run()

        if not isinstance(output,IllegalParsingError) and self.current_token.token_type !=EOF:
            return IllegalParsingError(ep.parse_pointer(self.token_number,self.tokens),f'Line {self.line} (Expected P,M,L,D or logival operators except NOT )'),self.line

        return output,self.line
    




class List:
    def __init__(self,elements):
        self.elements=elements
    def added_to(self,other):
        new_list=self.copy()
        new_list.elements.append(other.value)
        return new_list
    def mul_to(self,other):
        if isinstance(other,List):
            new_lis= self.copy()
            new_lis.elements.extend(other.elements)
            return new_lis

        else:
            return "Error1"
    def sub_to(self,other):
        if isinstance(other,Number):
            new_lis=self.copy()
            try:
                new_lis.elements.pop(other.value)
                return new_lis
            except:
                return "Error1"
        else:
            return "Error1"
    def copy(self):
        copy=List(self.elements)
        return copy
    def access(self,i):
        

        return self.elements[i.value]
        
    def __repr__(self):
        return f'[{",".join([str(x) for x in self.elements])}]'

class BaseFunction():
    def __init__(self,name):
       
        self.name=name or "<anonymous>"
        self.symb={}
    def check_args(self,arg_names,args):
        if len(args)>len(arg_names):
            return f"{len(args)-len(arg_names)} too many aguments are passed into '{self}'"

        if len(args)<len(arg_names):
            return f"{len(arg_names)-len(args)} too few aguments are passed into '{self}'"
        
        return None
    def populate_args(self,arg_names,args):
        for i in range(len(args)):
            arg_name=arg_names[i]
            arg_value=args[i]
            
            self.symb[arg_name]=arg_value
    def check_and_populate_args(self,arg_names,args):
        p=self.check_args(arg_names,args)
        if p!=None:
            return p
        
        self.populate_args(arg_names,args)
        return None



    






class Function:
    def __init__(self,name,body_node,arg_names):
        self.name=name or "<anonymous>"
        self.body_node=body_node
        self.arg_names=arg_names
        self.symb={}
    def execute(self,args):
        inter=interpreter()
        if len(args)>len(self.arg_names):
            return f"{len(args)-len(self.arg_names)} too many aguments are passed into '{self}'"

        if len(args)<len(self.arg_names):
            return f"{len(self.arg_names)-len(args)} too few aguments are passed into '{self}'"
        for i in range(len(args)):
            arg_name=self.arg_names[i]
            arg_value=args[i]
            self.symb[arg_name]=arg_value
        
        value=inter.visit(self.body_node,self.symb)
        return value
    def copy(self):
        copy=Function(self.name,self.body_node,self.arg_names)
        return copy
    def __repr__(self):
        return f'<function {self.name}>'





class String:
    def __init__(self,value):
        self.value=value
    def added_to(self,other):
        if isinstance(other,String):
            return String(self.value + other.value)
        return "Check for the Data types before concatinating"
    
    def mul_to(self,other):
        if isinstance(other,Number):
            
            return String(self.value * other.value)
        return "Check for the Data types before string multiplication"
    def NE(self,other):
        if isinstance(other,String):
            return self.value!=other.value
        else:
            return "Check for the Data types before comparing"
    def GE(self,other):
        if isinstance(other,String):
            return self.value>=other.value
        return "Check for the Data types before comparing"
    def LE(self,other):
        if isinstance(other,String):
            return self.value<=other.value
        return "Check for the Data types before comparing"
    def LT(self,other):
        if isinstance(other,String):
            return self.value<other.value
        return "Check for the Data types before comparing"
    def GT(self,other):
        if isinstance(other,String):
            return self.value>other.value
        return "Check for the Data types before comparing"
    def EE(self,other):
        if isinstance(other,String):
            return self.value==other.value
        return "Check for the Data types before comparing"
    def access(self,i):
        try:
            return self.value[i.value]
        except:
            raise IndexError()

    
          
    
    def sub_to(self,other):
        
        return "Cannot Substract Strings :)"
   
    def div_to(self,other):
        return "Cannot Divide Strings :)"
        
    def pow_to(self,other):
        return "Cannot exponentiate Strings :)"
    def is_true(self):
        return len(self.value)>0
    def copy(self):
        copy=String(self.value)
        return copy
  
    def __repr__(self):
        return str(self.value)
class Number(Value):
    def __init__(self,value):
        self.value=value
        
    def NE(self,other):
        if isinstance(other,Number):
            return self.value!=other.value
        else:
            return "Check for the Data types before comparing"
    def GE(self,other):
        if isinstance(other,Number):
            return self.value>=other.value
        return "Check for the Data types before comparing"
    def LE(self,other):
        if isinstance(other,Number):
            return self.value<=other.value
        return "Check for the Data types before comparing"
    def LT(self,other):
        if isinstance(other,Number):
            return self.value<other.value
        return "Check for the Data types before comparing"
    def GT(self,other):
        if isinstance(other,Number):
            return self.value>other.value
        return "Check for the Data types before comparing"
    def EE(self,other):
        if isinstance(other,Number):
            return self.value==other.value
        return "Check for the Data types before comparing"

    
          
    def added_to(self,other):
        if isinstance(other,Number):
            return Number(self.value + other.value)
        return "Check for the Data types before adding"
    def sub_to(self,other):
        if isinstance(other,Number):
            return Number(self.value - other.value)
        return "Check for the Data types before Substracting"
    def mul_to(self,other):
        if isinstance(other,Number):
            return Number(self.value * other.value)
        return "Check for the Data types before Multiplying"
    def div_to(self,other):
        if isinstance(other,Number):
            try:
                result=self.value / other.value
                
                

            except ZeroDivisionError:
                return 'Error'
            return result
        
    def pow_to(self,other):
        if isinstance(other, Number):

            return Number(self.value**other.value)
        return "Check for the Data types before exponentiating"
    

    def __repr__(self):
        return str(self.value)

Number.null=Number(0)
Number.false= Number(0)
Number.true=Number(1)
class BuiltInFunction(BaseFunction):
    def __init__(self,name):
        super().__init__(name)
    def execute(self,args):
        method_name=f'execute_{self.name}'
        method=getattr(self,method_name,self.no_visit_method)
        a=self.check_and_populate_args(method.arg_names,args)
        if a !=None:
            return a
        b=method()
        return b
    def no_visit_method(self,node):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy=BuiltInFunction(self.name)
        return copy
    def __repr__(self):
        return f"<Built-in function {self.name}>"

    def execute_print(self):
        print(str(self.symb.get('value')))
        return Number.null
    execute_print.arg_names=['value']
    def execute_print_ret(self):
        return String(str(self.symb.get('value')))
    execute_print_ret.arg_names=['value']
    def execute_input(self):
        text=input()
        return String(text)
    execute_input.arg_names=[]
    def execute_input_int(self):
       
        while True:
             text=input()
     
          
             try:
                 number=int(text)
                 break
             except ValueError:
                 print(f'{text} must be an interger !')
        return Number(number)
    execute_input_int.arg_names=[]
    def execute_clear(self):
        os.system('cls' if os.name=='nt' else 'clear')
        return Number.null
    execute_clear.arg_names=[]
    def execute_append(self):
        lis=self.symb.get("list")
        value=self.symb.get("value")
        if not isinstance(lis,List):
            return "First argument must be a list"
        lis.elements.append(value)
        return Number.null
    execute_append.arg_names=['list','value']
    def execute_pop(self):
        lis=self.symb.get("list")
        index=self.symb.get("index")
        if not isinstance(lis,List):
            return "First argument must be a list"
        if not isinstance(index,Number):
            return "Second argument must be a Number"
        try:

            element=lis.element.pop(index.value)
        except:
            return "Elements at this index could not be removed!"
        return element
    execute_pop.arg_names=['list','index']
BuiltInFunction.print=BuiltInFunction("print")
BuiltInFunction.print_ret=BuiltInFunction("print_ret")
BuiltInFunction.input=BuiltInFunction("input")
BuiltInFunction.input_int=BuiltInFunction("input_int")
BuiltInFunction.clear=BuiltInFunction("clear")
BuiltInFunction.append=BuiltInFunction("append")
BuiltInFunction.pop=BuiltInFunction("pop")


######iNTERPRETER######
class symbolTable:
    def __init__(self):
        self.symbols={}
        
    def get(self,name):
        value=self.symbols.get(name,None)
        if value==None and self.parent:
            return self.parent.get(name)
        return value
    def set(self,name,value):
        self.symbols[name]= value
    def remove(self,name):
        del self.symbols[name]


class interpreter:
    def __init__(self):
        self.sub=1
        
        
     
    def visit(self,node,p):
        method_name=f'visit_{type(node).__name__}'
        method=getattr(self,method_name, self.no_visit_method)
        return method(node,p)

    def no_visit_method(self,node,p):
        raise Exception(f'visit_{type(node).__name__} method Undefined')
    
    def visit_Value(self,node,p):
        a=self.sub
        self.sub=1
        return Number(node.token_type * a)
    def visit_ListNode(self,node,p):
        elements=[]
        for i in node.token_type:
            a=self.visit(i,p)
            if isinstance(a,RuntimeError) or isinstance(a,DivideByZeroError):
                return a
            elements.append(a)
        return List(elements)



    def visit_FRun(self,node,p):
        
        left=self.visit(node.left,p)
        if isinstance(left,DivideByZeroError) or isinstance(left, RuntimeError) :
            return left

        right=self.visit(node.right,p)
        if isinstance(right,DivideByZeroError) or isinstance(right,RuntimeError):
            return right
        if node.operator=='and':
            if isinstance(left,tuple):
                left=left[1]
            if isinstance(right,tuple):
                right=right[1]
            if not isinstance(left,bool):
                if (left.value==" " or left.value==0):

                    left=False
                else:
                    left=True
            if not isinstance(right,bool):
                if (right.value==" " or right.value==0):

                    right=False
                else:
                    right=True
            
            return (None,left and right)
            
        elif node.operator=='or':
            if isinstance(left,tuple):
                left=left[1]
            if isinstance(right,tuple):
                right=right[1]
            if not isinstance(left,bool):
                if (left.value==" " or left.value==0):

                    left=False
                else:
                    left=True
            if not isinstance(right,bool):
                if (right.value==" " or right.value==0):

                    right=False
                else:
                    right=True
            
            return (None,left or right)
       
       
    def visit_StringNode(self,node,p):
        
        return String(node.token_type)


    def visit_ForNode(self,node,p):
        elements=[]
        start_value=self.visit(node.start_value_node,p)
        if isinstance(start_value,RuntimeError):
            return start_value
        end_value=self.visit(node.end_value_node,p)
        if isinstance(end_value,RuntimeError):
            return end_value
        if node.step_value_node:
            step_value=self.visit(node.step_value_node,p)
            if isinstance(step_value,RuntimeError):
                return step_value
        else:
            step_value=Number(1)
        i=start_value.value
        if step_value.value>=0:
            condition=lambda:i<end_value.value
        else:
            condition=lambda:i>end_value.value
        while condition():
            self.symbols.set(node.var_name_tok.token_value,Number(i))
            i+=step_value.value
            for l in node.body_node:

                a=self.visit(l,p)
                if isinstance(a,RuntimeError):
                    return a
                elements.append(a)
        return List(elements)
    
    def visit_WhileNode(self,node,p):
        elements=[]
        while True:
            condition=self.visit(node.condition_node,p)
            if isinstance(condition,RuntimeError):
                return condition
            if isinstance(condition,Number) and condition.value<=0:
                break
            elif isinstance(condition,String) and condition.value==" ":
                break
            elif not isinstance(condition,Number) and not isinstance(condition,String):
                 if not condition[1]:break
            for l in node.body_node:
                a=self.visit(l,p)
                elements.append(a)
        return List(elements)



    def visit_Condition(self,node,p):
        
        result=None
        left=self.visit(node.left_expression,p)
        if isinstance(left,DivideByZeroError) or isinstance(left, RuntimeError) :
            return left
        if node.right_expression !=None:

            right=self.visit(node.right_expression,p)
            if isinstance(right,DivideByZeroError) or isinstance(right,RuntimeError):
                return right
        if node.operator==NE:
            if isinstance(left,tuple):

                result= left[0].NE(right)
            else:
                result=left.NE(right)
        elif node.operator==GE:
            if isinstance(left,tuple):
                result= left[0].GE(right)
            else:

                result=left.GE(right)
        elif node.operator==LE:
            if isinstance(left,tuple):
                result= left[0].LE(right)
            else:

                result=left.LE(right)
        elif node.operator==GT:
            if isinstance(left,tuple):
                result= left[0].GT(right)
            else:

                result=left.GT(right)
        elif node.operator ==EE:
            if isinstance(left,tuple):
                result= left[0].EE(right)
            else:

                result=left.EE(right)

        elif node.operator==LT:
            if isinstance(left,tuple):
                result= left[0].LT(right)
            
            else:
                result=left.LT(right)
        elif node.operator==None and (isinstance(left,Number) or isinstance(left,String)):
            if left.value==" " or left.value==0 or left.value=="":
                return(None, False)
            else:
                return(None,True)

        
        if result==False:

            return (None,False)
        
        
        return (None,True)


    def visit_IfNode(self,node,p):
        for condition, expr in node.cases:
            if isinstance(condition,RuntimeError):
                return condition
            condition_value=self.visit(condition,p)
            if isinstance(condition_value,RuntimeError):
                return condition_value
            if condition_value[1]==True:
                expr_value=[]
                for l in expr:
                    a=self.visit(l,p)
                    if isinstance(a,RuntimeError):
                        return a

                    expr_value.append(a)
                
                return List(expr_value)
        if node.else_case:
            expr_else=[]
            for l in node.else_case:
                a=self.visit(l,p)
                if isinstance(a,RuntimeError):
                    return a
                expr_else.append(a)

                

            
            
            return List(expr_else)        
        return None
    def visit_Operation(self,node,p):
        
        left=self.visit(node.value_left,p)
        if isinstance(left,DivideByZeroError) or isinstance(left, RuntimeError):
            return left
        
        
        right= self.visit(node.value_right,p)
        if isinstance(right,DivideByZeroError) or isinstance(right,RuntimeError):
            return right
        elif right==None:
            return RuntimeError(ep.parse_pointer(node.num,self.tokies),f'Line {node.line} (Expected Int, Float or an Identifier)')
        

        if node.operator==addition:
            result=left.added_to(right)
        elif node.operator==subtraction:
            result=left.sub_to(right)
        elif node.operator==multiplication:
            result=left.mul_to(right)
        
        elif node.operator==division:
            result=left.div_to(right)
        elif node.operator==power:
            result=left.pow_to(right)
        elif node.operator==access:
            result=left.access(right)
        if result=='Error':
        
            return DivideByZeroError(ep.parse_pointer(node.num,self.tokies),f'Line {node.line} (Cannot divide a number with zero)')
        elif result=="Error1":
            return RuntimeError(ep.parse_pointer(node.num,self.tokies),f'Line {node.line} (Check for Illegal List Operations)')

        elif result=="Check for the Data types before exponentiating":
            return RuntimeError(ep.parse_pointer(node.num,self.tokies),f'Line {node.line} (Check for the Data types before exponentiating)')

        elif result=="Check for the Data types before Multiplying":
            return RuntimeError(ep.parse_pointer(node.num,self.tokies),f'Line {node.line} (Check for the Data types before Multiplying)')
        elif result=="Check for the Data types before Substracting":
            return RuntimeError(ep.parse_pointer(node.num,self.tokies),f'Line {node.line} (Check for the Data types before Substracting)')

        elif result=="Check for the Data types before adding":
            return RuntimeError(ep.parse_pointer(node.num,self.tokies),f'Line {node.line} (Check for the Data types before adding)')

        elif result=="Check for the Data types before comparing":
            return RuntimeError(ep.parse_pointer(node.num,self.tokies),f'Line {node.line} (Check for the Data types before comparing)')

        return result
    def visit_Access(self,node,p):
        a=self.visit(node.list,p)
        if isinstance(a,RuntimeError):
            return a
        b=self.visit(node.i,p)
        if isinstance(b,RuntimeError):
            return b
        if (isinstance(a,List) and isinstance(b,Number)) or (isinstance(a,String) and isinstance(b,Number)):
            return a.access(b)
        else:
            return RuntimeError(ep.parse_pointer(node.num,self.tokies),f'Line {node.line} (Incorrect way of Indexing)')

        
    def visit_SignedVal(self,node,p):


        
        
        if node.op==subtraction:
            self.sub*=-1

            

       
        
        return self.visit(node.val)
    
    def visit_IdAccessNode(self,node,p):
        id=node.var_name_token.token_value
        
        if id not in self.symbols.symbols and id not in p:
            return RuntimeError(ep.parse_pointer(node.num,self.tokies),f'Line {node.line} -- variable not defined')
        if id in p:
            return p[id]
        return self.symbols.symbols[id]
    def visit_Idnode(self, node,p):
        var_name=node.var_name.token_value
        
        value=self.visit(node.mini_expression,p)
        if isinstance(value,tuple):
            if len(p)>0:
                p[var_name]=value[1]
            else:

                self.symbols.set(var_name,value[1])

        else:
            if len(p)>0:
                p[var_name]=value
            else:


                self.symbols.set(var_name,value)
            
            
      
        return value
    def visit_Assign(self,node,p):
        if not isinstance(node.left_val,IdAccessNode):
            return RuntimeError(ep.parse_pointer(node.num,self.tokies),f'Line {node.line} (Value to the left of the equation must be an identifier)')
        elif node.left_val.var_name_token.token_value not in self.symbols.symbols:
             return RuntimeError(ep.parse_pointer(node.num,self.tokies),f'Line {node.line} -- variable not defined')

        var_name=node.left_val.var_name_token.token_value
        value=self.visit(node.right_val,p)
        
        
        if isinstance(value,tuple):

            self.symbols.set(var_name,value[1])
            
            
        else:
            self.symbols.set(var_name,value)
            


        return value
    def visit_FuncDefNode(self,node,p):
        func_name=node.var_name_tok.token_value if node.var_name_tok else None
        body_node=node.body_node
        arg_names=[arg_name.token_value for arg_name in node.arg_name_toks]
        func_value=Function(func_name,body_node,arg_names)
        if node.var_name_tok:
            self.symbols.set(func_name,func_value)
        
        return func_value
    def visit_CallNode(self,node,p):
        args=[]
        value_to_call=self.visit(node.node_to_call,p)
        if isinstance(value_to_call,RuntimeError):
            return value_to_call
        value_to_call=value_to_call.copy()

        for i in node.arg_node:
            a=self.visit(i,p)
            
            if isinstance(a,RuntimeError):
                return a
            args.append(a)
        value=value_to_call.execute(args)
        return value
            




    

        