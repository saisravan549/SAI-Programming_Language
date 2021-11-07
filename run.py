import main
import sys
global_symbols= main.symbolTable()
global_symbols.set('null', main.Number.null)
global_symbols.set("false",main.Number.false)
global_symbols.set("true",main.Number.true)
global_symbols.set("print",main.BuiltInFunction.print)
global_symbols.set('print_ret',main.BuiltInFunction.print_ret)
global_symbols.set('input',main.BuiltInFunction.input)
global_symbols.set('input_int',main.BuiltInFunction.input_int)
global_symbols.set('clear',main.BuiltInFunction.clear)
global_symbols.set('append',main.BuiltInFunction.append)
global_symbols.set('pop',main.BuiltInFunction.pop)



def run():
    file_pointer=sys.argv[1]
    fp=open(file_pointer,'r')
    input_text=fp.readlines()
    
    txt=""
    if len(input_text)==0:
        print("Type some code!")
        return
    for i in range(len(input_text)):
        input_text[i]=input_text[i].strip()
    i=0
    while i<=len(input_text)-1:
        if input_text[i]=='':
            del input_text[i]
        else:
            i+=1
        
    lis=[]
    
    lis.append(input_text[0])
    i=1
    ctr=0
    endcount=0
    thencount=0
    
    while i<=len(input_text)-2:
        if input_text[i][0:2]=='if':
            ctr=0

        
        if input_text[i]=='then':
            endcount=0
            thencount=0
            
            
            j=i+1
            strr=""
            while j<=len(input_text)-1:
                
                
                if input_text[j]=='then' and not input_text[j-1][0:4]=='elif':
                    thencount+=1
                    print("then",thencount)
                
                
                if input_text[j]=='end':
                    
                       
                    endcount+=1
                    print("end",endcount)
                if input_text[j]=='end' and endcount==thencount+1:
                    break
                strr=strr+';'+input_text[j]
                j+=1



            
            a=lis.pop()
            
            lis.append(a+';'+input_text[i]+strr)
            
            i=j+1
            continue
        elif input_text[i][0:4]=='elif':
            ctr+=1
            a=lis.pop()
            if ctr>1:
                lis.append(a+input_text[i])
            else:

                

            
                lis.append(a+';'+input_text[i])
            i+=1
            continue
        
        elif input_text[i]=='else':
            ctr=0
            a=lis.pop()
            lis.append(a+';'+input_text[i]+';'+input_text[i+1])
            i+=2
            continue
        elif input_text[i]=='end':
           
            i+=1
            continue
        lis.append(input_text[i])
        i+=1

   
        
        
    if len(input_text)>2 and input_text[-2]!='then' and input_text[-2]!='else' and input_text[-1]!='end' and i<=len(input_text) :
        lis.append(input_text[-1])   
   
  
    
    
    line=0
    print(lis)
    print(input_text)
    
    parser=0
    a=0
    line=0
    for i in lis:
        
        

            
        a=line+1

        program_input=main.Lexer(i,-1)
        tokens=program_input.create_tokens()
        if tokens[1]!=None:
            print(tokens[1], f"At Line {a}, At Position {program_input.pos}")
            break
                
        else:

                
            if a:parser=main.Parser(tokens[0],a)
            else: parser=main.Parser(tokens[0])

           
            
            

            tokies=parser.tokens
            output = parser.parse()
            line=output[1]
            print(line)
            output=output[0]
            
            
            
           
            if not isinstance(output,main.IllegalParsingError) and not isinstance(output, main.RuntimeError) and not isinstance(output,main.DivideByZeroError) and not isinstance(output,main.IllegalLexingError):
            
                
                interpreter=main.interpreter
                interpreter.symbols=global_symbols
                
                
                interpreter.tokies=tokies
                int1=interpreter()
                result=int1.visit(output,[])
                
                if isinstance(result,main.IllegalParsingError) or isinstance(result, main.RuntimeError) or isinstance(result,main.DivideByZeroError) or  isinstance(result,main.IllegalLexingError):
                    print(result)
                    break
                 
                                      
        
            else:
                print(output)
                break
                    
            


run()