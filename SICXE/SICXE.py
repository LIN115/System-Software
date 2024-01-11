import json
import math

# 定義寄存器編號和十六進制數字的字典
num_of_register = {'A': 0, 'X': 1, 'L': 2, 'B': 3,
                   'S': 4, 'T': 5, 'F': 6, 'PC': 8, 'SW': 9}

# 定義十進制轉十六進制的字典
HexDict = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
           8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}

# 定義十六進制轉十進制的字典
DecDict = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
           '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}

# 將二進制轉換為十六進制
def Bin2Hex(Bin):
    Hex = ''
    if (len(Bin) > 4):
        fill = (4 - (len(Bin) % 4))
        if (fill == 4):
            fill = (fill - 4)

        Bin = ('0'*fill + Bin)

        for i in range(0, len(Bin), 4):
            Hex += Bin2Hex(Bin[i:(i*4+4)])
    else:
        Dec = 0
        for i, digit in enumerate(Bin):
            Dec += (int(digit) * math.pow(2, (3-i)))
        Hex = Dec2Hex(Dec)

    return Hex

# 將十進制轉換為十六進制
def Dec2Hex(Dec: int):
    Hex = ''
    while (Dec >= 16):
        Hex = (HexDict[Dec % 16] + Hex)
        Dec //= 16

    Hex = (HexDict[Dec] + Hex)
    return Hex

# 將十六進制轉換為十進制
def Hex2Dec(Hex: str):
    Dec = 0
    times = 0
    while (len(Hex) > 0):
        Dec += int(DecDict[Hex[-1]] * math.pow(16, times))
        Hex = Hex[:-1]
        times += 1

    return Dec

# 處理BYTE指令
def BYTE(parms):
    mode = parms[0]
    data = parms[2:-1]
    objCode = ''
    if (mode == 'C'):
        for i in data:
            objCode += (Dec2Hex(ord(i))).zfill(2)
    elif (mode == 'X'):
        objCode += data
    else:
        print('BYTE Error')

    location_add = (len(objCode)//2)
    return location_add, objCode

# 處理WORD指令
def WORD(parms):
    if (int(parms) >= 0):
        objCode = Dec2Hex(int(parms)).zfill(6)
    else:
        full_hex = Hex2Dec('1000000')
        objCode = Dec2Hex(full_hex + int(parms)).zfill(6)
    location_add = (len(objCode)//2)
    return location_add, objCode

# 處理RESB指令
def RESB(parms):
    objCode = ' '
    location_add = int(parms)
    return location_add, objCode

# 處理RESW指令
def RESW(parms):
    objCode = ' '
    location_add = (int(parms) * 3)
    return location_add, objCode

# 暫存器類
class Register():
    A = False
    X = False
    L = False
    B = False
    S = False
    T = False
    F = False
    PC = False
    SW = False
    
# 載入暫存器值
    def Load(self, instrucet, parms):
        if (instrucet == 'LDA'):
            self.A = parms
        elif (instrucet == 'LDX'):
            self.X = parms
        elif (instrucet == 'LDL'):
            self.L = parms
        elif (instrucet == 'LDB'):
            self.B = parms
        elif (instrucet == 'LDS'):
            self.S = parms
        elif (instrucet == 'LDT'):
            self.T = parms
        elif (instrucet == 'LDF'):
            self.F = parms
# 清除暫存器值
    def Clear(self, parms):
        if (parms == 'A'):
            self.A = 0
        elif (parms == 'X'):
            self.X = 0
        elif (parms == 'L'):
            self.L = 0
        elif (parms == 'B'):
            self.B = 0
        elif (parms == 'S'):
            self.S = 0
        elif (parms == 'T'):
            self.T = 0
        elif (parms == 'F'):
            self.F = 0
        elif (parms == 'PC'):
            self.PC = 0
        elif (parms == 'SW'):
            self.SW = 0
            
# 獲取暫存器地址
    def Location_of_rigster(self):
        if self.A:
            self.A = self.Parms_computing(self.A)
        elif self.X:
            self.X = self.Parms_computing(self.X)
        elif self.L:
            self.L = self.Parms_computing(self.L)
        elif self.B:
            self.B = self.Parms_computing(self.B)
        elif self.S:
            self.S = self.Parms_computing(self.S)
        elif self.T:
            self.T = self.Parms_computing(self.T)
        elif self.F:
            self.F = self.Parms_computing(self.F)
            
# 將指令參數的值計算出來
    def Parms_computing(self, parms):
        if (parms[0] == '#'):
            parms = parms[1:]
            return function_[parms]

# 創建 Register 類的實例
register = Register()

f = open('./Input.txt', 'r')
Input = f.readlines()
f.close()

# 從 JSON 檔案中讀取指令集
with open('./instrucetion_SICXE.json', 'r', encoding='utf-8') as j:
    instrucetion = json.load(j)

function_ = {}

# 處理輸入的第一行指令，並初始化相應的變數
temp = Input[0].replace('\n', '').split(' ')
if (len(temp) == 3):
    information = [[5, temp[2].zfill(4), temp[0], temp[1], temp[2], ' ']]
    function_[temp[0]] = Hex2Dec(information[0][4])
else:
    information = [[5, temp[2].zfill(4), '', temp[0], temp[1], ' ']]

line = 10
location = Hex2Dec(information[0][4])
for i in Input[1:]:
    line += 5
    
# 如果是註解行，則將其加入信息列表中
    if (i[0] == '.'):
        information.append([line, '', '.', i.replace(
            '.', '').replace('\n', ''), '', ' '])
        continue
    
# 將指令行拆分為單詞
    i = i.replace('\n', '').split(' ')
    
# 根據指令行的單詞數量不同，選擇相應的處理邏輯
    if (len(i) == 1):
        information.append(
            [line, Dec2Hex(location).zfill(4), '', i[0], '', ''])
    elif (len(i) == 2):
        information.append(
            [line, Dec2Hex(location).zfill(4), '', i[0], i[1], ''])
    elif (len(i) == 3):
        information.append(
            [line, Dec2Hex(location).zfill(4), i[0], i[1], i[2], ''])
        
# 將指令和對應的地址加入字典中
        function_[i[0]] = Dec2Hex(location).zfill(4)
        
# 根據指令類型和內容，更新程序計數器（location）
    if (information[-1][3][0] == '+'):
        location += 4
    elif (information[-1][3] not in instrucetion['pseudo']):
        location += int(instrucetion['instrucetion'][information[-1][3]][1])
        
# 如果是 CLEAR 指令，清除相應的寄存器
        if (information[-1][3] == 'CLEAR'):
            register.Clear(information[-1][4])
    else:
        # 根據偽操作的類型處理相應的邏輯
        if (information[-1][3] == 'BYTE'):
            location_add, objectCode = BYTE(information[-1][4])
        elif (information[-1][3] == 'RESB'):
            location_add, objectCode = RESB(information[-1][4])
        elif (information[-1][3] == 'RESW'):
            location_add, objectCode = RESW(information[-1][4])
        elif (information[-1][3] == 'WORD'):
            location_add, objectCode = WORD(information[-1][4])
        elif (information[-1][3] == 'BASE'):
            # 如果是 BASE 指令，將其值載入到暫存器
            register.Load(information[-2][3], information[-2][4])
            information[-1][1] = ''
            information[-1][5] = ' '
            continue
        elif (information[-1][3] == 'END'):
            # 如果是 END 指令，將信息行的地址部分設置為空，目標代碼設置為空格
            information[-1][1] = ''
            objectCode = ' '
            
# 根據偽操作的結果更新程序計數器（location）
        location += location_add
        information[-1][-1] = objectCode
        
# 計算暫存器的地址
register.Location_of_rigster()

# 處理信息列表中每條指令的目標代碼
for now_index, infor in enumerate(information):
    infor = infor.copy()
    next_index = now_index
    
    # 如果目標代碼為空，則進行特定處理邏輯
    if infor[5] == '':
        # 如果指令格式為2
        if (instrucetion["instrucetion"][infor[3].replace('+', '')][1] == '2'):
            infor[4] = infor[4].split(',')
            # 根據指令的不同，生成相應的目標代碼
            if (len(infor[4]) == 2):
                information[now_index][5] = f'{instrucetion["instrucetion"][infor[3]][0]}{num_of_register[infor[4][0]]}{num_of_register[infor[4][1]]}'
            else:
                information[now_index][5] = f'{instrucetion["instrucetion"][infor[3]][0]}{num_of_register[infor[4][0]]}0'
        # 如果指令格式為3
        elif (instrucetion["instrucetion"][infor[3].replace('+', '')][1] == '3'):
            # 如果是 RSUB 指令，生成特殊的目標代碼
            if (infor[3] == 'RSUB'):
                information[now_index][5] = '4F0000'
                continue
            # 查找下一個非空指令，更新程序計數器
            next_index += 1
            while information[next_index][1] == '':
                next_index += 1

            register.PC = information[next_index][1]
            
            # 處理指令的位址表示法
            if (infor[4][0] == '@'):
                infor[4] = infor[4][1:]
                n, i = 1, 0
            elif (infor[4][0] == '#'):
                infor[4] = infor[4][1:]
                n, i = 0, 1
            else:
                n, i = 1, 1
                
            # 處理指令中的索引位址（帶有 ',X'）
            if ',X' in infor[4]:
                infor[4] = infor[4].replace(',X', '')
                x = 1
            else:
                x = 0
                
            # 處理擴展模式（Extended Mode）標誌
            if (infor[3][0] == '+'):
                infor[3] = infor[3][1:]
                e = 1
            else:
                e = 0

            opcode = f'{instrucetion["instrucetion"][infor[3]][0]}0'

            b, p = 0, 0
            
            # 處理擴展模式和指令類型的不同，生成相應的目標代碼
            if e:
                if (not n and i and (infor[4].isdigit())):
                    address = Dec2Hex(int(infor[4])).zfill(5)
                else:
                    address = function_[infor[4]].zfill(5)

                information[now_index][5] = f'{Dec2Hex(Hex2Dec(opcode) + Hex2Dec(Bin2Hex(f"{n}{i}{x}{b}{p}{e}"))).zfill(3)}{address}'

            else:
                if (not n and i and (infor[4].isdigit())):
                    disp = Dec2Hex(int(infor[4])).zfill(3)
                else:
                    disp = (
                        Hex2Dec(function_[infor[4]]) - Hex2Dec(register.PC))

                    if x:
                        disp -= register.X
                        
                    # 處理相對位址和基底位址的情況
                    if ((disp >= 4096) or ((disp <= -4096))):
                        b, p = 1, 0
                        disp = (
                            Hex2Dec(function_[infor[4]]) - Hex2Dec(register.B))

                        if x:
                            disp -= register.X
                    else:
                        b, p = 0, 1

                    if (disp < 0):
                        disp = Dec2Hex(disp + Hex2Dec('1000')).zfill(3)
                    else:
                        disp = Dec2Hex(disp).zfill(3)

                information[now_index][5] = f'{Dec2Hex(Hex2Dec(opcode) + Hex2Dec(Bin2Hex(f"{n}{i}{x}{b}{p}{e}"))).zfill(3)}{disp[-3:]}'

# 輸出結果
print(" %-10s %-10s %-10s %-10s %-10s %-17s" %
      ('Line', 'Location', '', 'Original', '', 'Object code'))
for i in information:
    if (i[2] == '.'):
        print(" %-10s %-10s %-10s %-39s" % (i[0], i[1], i[2], i[3]))
    else:
        print(" %-10s %-10s %-10s %-10s %-10s %-17s" %
              (i[0], i[1], i[2], i[3], i[4], i[5]))
