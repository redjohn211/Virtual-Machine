def main():
    Memory = []
    Registers = []
    for x in range(0,pow(2,16)):
        Memory.append("0"*16)
    for x in range(0,8):
        Registers.append("0"*16)
    NZP = "000"
    iPointer = 0
    iRegister = "randomValue"
    while(True):
        print("Commands: [LOAD fname addr], REGISTERS, DUMP, STATE, RUN, CLEAR")
        print("\n")
        instruction = input("Enter your command").split(" ")
        if(instruction[0] == "LOAD"):
            iPointer = Load(iPointer,instruction[1],instruction[2])[0]
            binaryInstruct = Load(iPointer,instruction[1],instruction[2])[1]
            for x in range(len(binaryInstruct)):
                Memory[x] = binaryInstruct[x]
            iRegister = Memory[int(iPointer,2)]
        if(instruction[0] == "REGISTERS"):
            print("Register:")
            for x in Registers:
                print(x[0:4]+" "+x[4:8]+" "+x[8:12]+" "+x[12:16])
        if(instruction[0] == "DUMP"):
            Dump(iPointer,Memory)
            
        if(instruction[0] == "STATE"):
            Dump(iPointer,Memory)
            print("Register:")
            for x in Registers:
                print(x[0:4]+" "+x[4:8]+" "+x[8:12]+" "+x[12:16])               
            print("NZP:")
            print(NZP)
            print("Instruction Pointer:")
            print(iPointer)
            print("Instruction Register:")
            print(iRegister)
            
        if(instruction[0] == "RUN"):
            while(iRegister[:4]!="0000"):
                iRegister = Memory[int(iPointer,2)]
                iPointer = bin(int(iPointer,2)+1)
                Registers,NZP,iPointer,iRegister,Memory = decode(iRegister,Registers,NZP,iPointer,iRegister,Memory)

        if(instruction[0] == "CLEAR"):
            Memory = []
            Registers = []
            for x in range(0,pow(2,16)):
                Memory.append("0"*16)
            for x in range(0,8):
                Registers.append("0"*16)
            NPZ = "000"
            iPointer = 0
            iRegister = "randomValue"
        if(instruction[0] == "DECODE"):
            result = decode("1010000011111110", Registers,NZP,iPointer,iRegister,Memory)
            result = decode("1010110011111110", Registers,NZP,iPointer,iRegister,Memory)
            Registers = result[0]
            NZP = result[1]
            print(Registers)
        if(instruction[0] == "DECODE1"):
            #Registers[0] = "0000000011111111"
            result = decode("0001000000111111", Registers,NZP,iPointer,iRegister,Memory)
            Registers = result[0]
            NZP = result[1]
            iPointer = result[2]
def Load(iPointer,instruction,addr):
        inFile = open(instruction)
        binaryInstruct = []
        for line in inFile:
            binaryInstruct.append(line)
        iPointer = bin(int(addr))
        return iPointer, binaryInstruct
def Dump(iPointer,Memory):
    temp = iPointer[:7]
    y = 0
    for x in range(pow(2,16)):
        if(Memory[x][0:7] == temp):
            print(hex(y)[1:],":", Memory[x])
            y+=1
    y = 0 

def setNZP(temp):
    a=""
    if(int(temp)< 0):
            a = "100"
    if(int(temp)== 0):
            a = "010"
    if(int(temp) > 0):
            a = "001"
    return a
def ADD(x,Registers,nzp,iPointer,iRegister,Memory):
    DR =int(("0b"+x[4:7]),2)
    SR1 = int(("0b"+x[7:10]),2)
    
    if(x[10] == "1"):
        imm5=x[11:]
        leading = x[11]
        while(len(imm5)<16):
            imm5 = leading+imm5
        imm5 = "0b"+imm5
        temp1 = signedInt("0b"+Registers[SR1])+signedInt(str(imm5))
        temp = signedBin(temp1,16)[2:]
        nzp = setNZP(signedInt("0b"+temp))
    if(x[10] == "0"):
        SR2 = int(("0b"+x[13:]),2)
        temp1 = signedInt("0b"+Registers[SR1])+signedInt("0b"+Registers[SR2])
        temp = signedBin(temp1,16)[2:]
        nzp = setNZP(signedInt("0b"+temp))
    while(len(temp)<16):
        temp = "0"+temp
    Registers[DR] = temp
        
    return Registers,nzp,iPointer,iRegister,Memory
def HALT(x,Registers,nzp,iPointer,iRegister,Memory):
    return Registers,nzp,iPointer,iRegister,Memory
def AND(x,Registers,nzp,iPointer,iRegister,Memory):
    DR = int(("0b"+x[4:7]),2)
    SR1 = int(("0b"+x[7:10]),2)
    if(x[10] == "1"):
        imm5 = x[13:]
        if(imm5[0] == "0"):
            while(len(imm5)<17):
                imm5="0"+imm5
        if(imm5[0] == "1"):
            while(len(imm5)<17):
                imm5="1"+imm5
        temp = and2(Registers[SR1],imm5)
        
    if(x[10] == "0"):
        SR2 = int(("0b"+x[13:]),2)
        temp = and2(Registers[SR1],Registers[SR2])
    Registers[DR]= temp
    nzp = setNZP(signedInt("0b"+temp))
    return Registers,nzp,iPointer,iRegister,Memory
def and2(x,y):
    result = ""
    for i in range(len(x)):
        if(x[i] == "1" and y[i] == "1"):
            result+="1"
        else:
            result+="0"
    return result
        
def NOT(x,Registers,nzp,iPointer,iRegister,Memory):
    DR = int(("0b"+x[4:7]),2)
    SR = Registers[int("0b"+x[7:10],2)]
    sr = ""
    for x in range(len(SR)):
        if(SR[x] =="1"):
            sr+="0"
        else:
            sr+="1"
    Registers[DR] = sr
    nzp = "001"
    return Registers,nzp,iPointer,iRegister,Memory
    
def LD(x,Registers,nzp,iPointer,iRegister,Memory):
    DR = int(("0b"+x[4:7]),2)
    iPointer = iPointer[2:]
    while(len(iPointer)<16):
        iPointer = "0"+iPointer
    a = iPointer[:7]+x[7:]
    Registers[DR] = Memory[int(("0b"+a),2)]
    nzp = setNZP(signedInt("0b"+Registers[DR]))
    iPointer = "0b"+iPointer
    return Registers,nzp,iPointer,iRegister,Memory
def LDI(x,Registers,nzp,iPointer,iRegister,Memory):
    DR = int(("0b"+x[4:7]),2)
    iPointer = iPointer[2:]
    while(len(iPointer)<16):
        iPointer = "0"+iPointer
    temp = Memory[int(("0b"+iPointer[:7]+x[7:]),2)]
    temp = int("0b"+temp,2)
    nzp = setNZP(signedInt("0b"+Registers[DR]))
    Registers[DR] = Memory[temp]
    iPointer = "0b"+iPointer
    return Registers,nzp,iPointer,iRegister,Memory
def LDR(x,Registers,nzp,iPointer,iRegister,Memory):
    print("LDR","R"+str(int(("0b"+x[4:7]),2)),"R"+str(int(("0b"+x[7:10]),2)),x[10:])
    return Registers,nzp,iPointer,iRegister,Memory
def ST(x,Registers,nzp,iPointer,iRegister,Memory):
    iPointer = iPointer[2:]
    while(len(iPointer)<16):
        iPointer = "0"+iPointer
    SR1 = int(("0b"+x[4:7]),2)
    Memory[int(("0b"+iPointer[:7]+x[7:]),2)] = Registers[SR1]
    iPointer = "0b"+iPointer
    return Registers,nzp,iPointer,iRegister,Memory
def STI(x,Registers,nzp,iPointer,iRegister,Memory):
    iPointer = iPointer[2:]
    while(len(iPointer)<16):
        iPointer = "0"+iPointer
    SR1 = int(("0b"+x[4:7]),2)
    temp = Memory[int(("0b"+iPointer[:7]+x[7:]),2)]
    Memory[int("0b"+temp,2)] = Registers[SR1]
    iPointer = "0b"+iPointer
    return x,Registers,nzp,iPointer,iRegister,Memory
def STR(x,Registers,nzp,iPointer,iRegister,Memory):
    print("STR","R"+str(int(("0b"+x[4:7]),2)),"R"+str(int(("0b"+x[7:10]),2)),x[10:])
    return Registers,nzp,iPointer,iRegister,Memory

def GET(x,Registers,nzp,iPointer,iRegister,Memory):
    Input = input("Enter your value")
    DR = int(("0b"+x[4:7]),2)
    if(x[7] == "0"):
        a = signedBin(Input,16)[2:]
        while(len(a)<16):
            a = "0"+a
        Registers[DR] = a
        nzp = setNZP(Input)
    if(x[7] == "1"):
        a = bin(ord(Input))[2:]
        while(len(a)<16):
            a = "0"+a
        Registers[DR] = a
    return Registers,nzp,iPointer,iRegister,Memory


def PUT(x,Registers,nzp,iPointer,iRegister,Memory):
    DR = int(("0b"+x[4:7]),2)
    if(x[7] == "0"):
        setNZP(signedInt("0b"+Registers[DR]))
        print(signedInt("0b"+Registers[DR]))
    if(x[7] == "1"):
        temp = int("0b"+Registers[DR],2)
        print(chr(temp))
        nzp = "001"
        if(temp == 0):
            nzp = "010"
    return Registers, nzp,iPointer,iRegister,Memory
def BR(x,Registers,nzp,iPointer,iRegister,Memory):
    iPointer = iPointer[2:]
    while(len(iPointer)<16):
        iPointer = "0"+iPointer
    iPointer = "0b"+iPointer
    temp = ""
    if(nzp[0] == "1"):
        temp+="n"
    elif(nzp[1] == "1"):
        temp+="z"
    elif(nzp[2] == "1"):
        temp+="p"
            
            
    nzp1 = ""
    
    if(x[4] == "1"):
        nzp1+="n"
    if(x[5] == "1"):
        nzp1+="z"
    
    if(x[6] == "1"):
        nzp1+="p"
        
    if(temp in nzp1):
        iPointer = iPointer[:9]+x[7:]
    return Registers, nzp,iPointer,iRegister,Memory
def JMP(x,Registers,nzp,iPointer,iRegister,Memory):
    iPointer = iPointer[2:]
    while(len(iPointer)<16):
        iPointer = "0"+iPointer
    if(x[4] == "0"):
        iPointer = "0b"+iPointer[:7]+x[7:]
    else:
        Registers[7] = iPointer
        iPointer = "0b"+iPointer[:7]+x[7:]
    return Registers, nzp,iPointer,iRegister,Memory
def JMPR(x,Registers,nzp,iPointer,iRegister,Memory):
    if(x[4] == "0"):
        print("JMPR","R"+str(int(("0b"+x[7:10]),2)),x[10:])
    else:
        print("JSRR","R"+str(int(("0b"+x[7:10]),2)),x[10:])
    return Registers, nzp,iPointer,iRegister,Memory     
def RET(x,Registers,nzp,iPointer,iRegister,Memory):
    iPointer = Registers[7]
    return Registers, nzp,iPointer,iRegister,Memory
def decode(code,Registers,nzp,iPointer,iRegister,Memory):
    tasks = {"ADD":ADD, "HALT":HALT, "AND":AND,"NOT":NOT,"LD":LD,"LDI":LDI,"LDR":LDR,"ST":ST,"STI":STI,"STR":STR,"GET":GET,"GETC":GET,"PUT":PUT,"PUTC":PUT,"BR":BR,"JMP":JMP,"JSR":JMP,"JMPR":JMPR,"JSRR":JMPR,"RET":RET}
    if(code[:4] == "0001"):
        a = tasks["ADD"](code,Registers,nzp,iPointer,iRegister,Memory)
    elif(code[:4] == "0000"):
        a = tasks["HALT"](code,Registers,nzp,iPointer,iRegister,Memory)
    elif(code[:4]=="0010"):
        a = tasks["AND"](code,Registers,nzp,iPointer,iRegister,Memory)
    elif(code[:4] == "0011"):
        a = tasks["NOT"](code,Registers,nzp,iPointer,iRegister,Memory)
    elif(code[:4] == "0100"):
        a = tasks["LD"](code,Registers,nzp,iPointer,iRegister,Memory)
    elif(code[:4] == "0101"):
        a = tasks["LDI"](code,Registers,nzp,iPointer,iRegister,Memory)
    elif(code[:4] == "0110"):
        a = tasks["LDR"](code,Registers,nzp,iPointer,iRegister,Memory)
    elif(code[:4] == "0111"):
        a = tasks["ST"](code,Registers,nzp,iPointer,iRegister,Memory)
    elif(code[:4]=="1000"):
        a = tasks["STI"](code,Registers,nzp,iPointer,iRegister,Memory)
    elif(code[:4] == "1001"):
        a = tasks["STR"](code,Registers,nzp,iPointer,iRegister,Memory)
    elif(code[:4] == "1010"):
        a = tasks["GET"](code,Registers,nzp,iPointer,iRegister,Memory)
    elif(code[:4] == "1011"):
        a = tasks["PUT"](code,Registers,nzp,iPointer,iRegister,Memory)
    elif(code[:4] == "1100"):
        a = tasks["BR"](code,Registers,nzp,iPointer,iRegister,Memory)
    elif(code[:4] == "1101"):
        a = tasks["JMP"](code,Registers,nzp,iPointer,iRegister,Memory)
    elif(code[:4] == "1110"):
        a = tasks["JMPR"](code,Registers,nzp,iPointer,iRegister,Memory)
    elif(code[:4] == "1111"):
        a = tasks["RET"](code,Registers,nzp,iPointer,iRegister,Memory)
    return a

"***************************************************************************"

def binNbits(num,bits):
    result = ""
    if(num<0):
        result = result+"-0b"
        num = num *-1
    else:
        result = result +"0b"
    c = ""
    if(num<pow(2,bits)):
        while(bits>=0):
            a = num//pow(2,bits)
            c = c+str(a)
            num = num%pow(2,bits)
            bits = bits-1    
        c = c[1:]
    else:
        raise ValueError("not enough bits")
        
    result = result + c
    return result


def binNbit(num,bits):
    if(num<0 and num*-1<pow(2,bits)):
        a = bits - len(bin(num))+3
        b=""
        for x in range(0,a,1):
            b=b+"0"
      
        
        return bin(num)[:3]+b+bin(num)[3:]
    elif(num>=0 and num<pow(2,bits)):
        a = bits - len(bin(num))+2
        b=""
        for x in range(0,a,1):
            b=b+"0"
            
        return bin(num)[:2]+b+bin(num)[2:]
    else:
        raise ValueError("not enough bits")
def invert(result):
    for x in range(0,len(result),1):
            if(result[x] == "0"):
                return result[:x]+"1"+result[x+1:]
            if(result[x] == "1"):
                return result[:x]+"0"+result[x+1:]
def signedBin(num, bits): 
    result = ""
    num = int(num)
    if(num <0 and (num*-1)<=pow(2,bits)/2):
        num = num*-1
        result = binNbits(num,bits)
        result = result[2:]
        for x in range(0,len(result),1):
            if(result[x] == "0"):
                result = result[:x]+"1"+result[x+1:]
            else:
                result = result[:x]+"0"+result[x+1:]
        result = int(("0b"+result),2)+1
        result = "0b"+bin(result)[2:]
    elif(num >=0 and num < pow(2,bits)/2) :
        result = binNbits(num,bits)
    else:
        raise ValueError("not enough bits")
    return result

def checkBin(a):
    b = set(a)
    s = {"0","1"}
    return (s ==b or b =={"0"} or b =={"1"})

def signedInt0(binNum):
    if(binNum[0] == "0" and  binNum[1] == "b" and checkBin(binNum[2:]) == True):
        if(binNum[2] == "1"):
            result = binNum[2:]
            for x in range(0,len(result),1):
                if(result[x] == "0"):
                    result = result[:x]+"1"+result[x+1:]
                else:
                    result = result[:x]+"0"+result[x+1:]
            result = "0b"+result
            result = (int(result,2)*-1)-1
            return result
        else:
            return int(binNum,2)

    else:
        raise TypeError("not in binary format")

def signedInt(binNum):
    if(binNum[2] == "1"):
        result = binNum[2:]
        for x in range(0,len(result),1):
            if(result[x] == "0"):
                result = result[:x]+"1"+result[x+1:]
            else:
                result = result[:x]+"0"+result[x+1:]
        result = "0b"+result
        result = (int(result,2)*-1)-1
        return result
    else:
        return int(binNum,2)

    

def binAddition(bin1,bin2):
    if(checkBin(bin1[2:]) and checkBin(bin2[2:])):
        b = "0"*((abs(len(bin1)-len(bin2)))+1)
        if(len(bin2)>len(bin1)):
            bin1 = b+bin1[2:]
            bin2 = "0"+bin2[2:]
        else:
            bin2 = b+bin2[2:]
            bin1 = "0"+bin1[2:]
        bin1 = list(bin1)
        bin2 = list(bin2) 
        bin1 = [ int(x) for x in bin1 ]
        bin2 = [ int(x) for x in bin2 ]
        add = "0"*(len(bin2))
        add = list(add)
        add = [ int(x) for x in add]
        c = len(bin1)-1
        carry = 0
        while(c >=0):
            if(bin1[c]+bin2[c]+carry == 0):
                carry = 0
                add[c] = 0
            elif(bin1[c] + bin2[c] +carry == 1):
                carry= 0
                add[c] = 1
            elif(bin1[c] + bin2[c] +carry == 2):
                carry = 1
                add[c] = 0
            elif(bin1[c] + bin2[c] +carry == 3):
                carry = 1
                add[c] = 1
            c = c-1

             
    else:
        raise TypeError("input is not in binary")
     # it has an extra digit in the beginning to take care of
                        #carryovers
    if(add[0] == 1):
        raise ValueError("Not enough bits to store the result")
    final = "0b"
    for x in range(1,len(add),1):
        final = final + str(add[x])
    return final

def fraction(num,expB):
    c = ""
    for x in range(1,expB+1,1):
        a = x*-1
        b = (num//pow(2,a))
        num = num-(pow(2,a)*b)        
        c = c+ str(int(b))
    return c

def decimal(num):
    a = 0
    for x in range(1,len(num)+1,1):
        b = x*-1
        a = a + pow(2,b)*int(num[x-1])
    return a
        
            
def float2bin(num,byte):
    if(byte == 1):
        expB = 3
        manB = 4
    elif(byte == 2):
        expB = 6
        manB=9
    elif(byte == 6):
        expB = 8
        manB=23
    elif(byte == 8):
        expB = 11
        manB = 52
    if(num<0):
        num = num*-1
        sign = "1"
    else:
        sign = "0"
    bias = pow(2,(expB-1))-1
    wholeNum = int(num)
    binNum = bin(wholeNum)[2:]
    binFrac = fraction(num%wholeNum,expB)
    binExp = bin((len(binNum) - 1 + bias))[2:]
    man = binNum+binFrac
    print("whole:",man,"Num:",binNum,"Frac:",binFrac)
    lenExp = len(binNum)
    maxExp = 0
    print("bias",bias)
    print("lenExp",lenExp)
    print("maxExp",maxExp)
    binExp = binExp[:expB]
    if((bias+1<lenExp)):
        binExp = "1"*expB
    result = sign+" " + binExp+" "+man[1:manB+1]
    return result

    
def bin2float(binNum):
    if(len(binNum)==8):
        lenExp = 3
        lenMan = 4
    elif(len(binNum)==16):
        lenExp = 6
        lenMan=9
    elif(len(binNum)==32):
        lenExp = 8
        lenMan=23
    elif(len(binNum)==64):
        lenExp = 11
        lenMan = 52
    else:
        raise TypeError("Please enter number with length 2^n;n>2")
    
    result = "" 
    if(binNum[0] == "0"):
        result = "+"
    else:
        result = "-"
    
    bias = pow(2,(lenExp-1))-1
    exp = "0b"+binNum[1:lenExp+1]
    man = binNum[lenExp+1:]
    if(binNum[1:lenExp+1] == "1"*lenExp):
        if(man == "0"*len(man)):
            raise ValueError("The number is infinite")
        else:
            raise ValueError("It is not a number")
    intExp = int(exp,2)
    intExp = intExp-bias
    b = ""
    a = man
    for x in range(1,intExp+1,1):
        a = man[x:]
        b = b+man[x-1]
    result = result + "1"+b+"."+a
    result = result.split(".")
    value = int("0b"+str(result[0][1:]),2)
    decimal1 = decimal(a)
    return value + decimal1   
        

        

    
    
        
