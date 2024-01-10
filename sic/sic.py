# 導入 SIC_Instruction 模塊和 defaultdict
import SIC_Instruction
from collections import defaultdict

# 函數：刪除註解
def remove_comment(line: str) -> str:
    # 刪除註解
    for i in range(len(line)):
        if '.' in line[i]:
            return line[:i].strip()
    return line.strip()

# 函數：處理 BYTE 指令
def process_byte(thrd: str) -> tuple:
    mode, data = thrd[0], ""

    if mode == "C":
        data += ''.join([hex(ord(c))[2:] for c in thrd[2:-1]]).upper()
    elif mode == "X":
        data += thrd[2:-1]
    else:
        raise ValueError("ERROR BYTE")

    return len(data) // 2, data

# 函數：處理 WORD 指令
def process_word(thrd: str) -> tuple:
    value, data = int(thrd), ""

    if value >= 0:
        data = hex(value)[2:].upper().zfill(6)
    else:
        HEX = "1000000"
        data = hex(int(HEX, 16) + value)[2:].upper().zfill(6)

    return len(data) // 2, data

# 函數：處理 RESB 指令
def process_resb(thrd: str) -> tuple:
    return int(thrd), ""

# 函數：處理 RESW 指令
def process_resw(thrd: str) -> tuple:
    return int(thrd) * 3, ""

# 主組譯器函數
def assembler() -> None:
    LOCATION, ADD = 0, 0
    RESULT, FUNC_LOC = [], defaultdict(int)

    # 讀取輸入文件 "input.txt"
    with open("input.txt", "r", encoding="UTF-8") as inp:
        lines = inp.readlines()

        for line in lines:
            line = remove_comment(line).strip()
            fst, snd, thrd, obj_code = "", "", "", ""

            if not line:
                continue

            if LOCATION == 0:
                # 處理起始位置
                if line.split()[-1] == "START":
                    print("ERROR START")
                    exit()

                LOCATION = int(line.split()[-1], 16)
                fst, snd, thrd = line.split()[0], line.split()[1], ""

                RESULT.append(["", fst, snd, thrd, obj_code])
                continue

            else:
                if len(line.split()) == 1:
                    # 處理只有一個指令的情況
                    snd = line.split()[0]
                    obj_code = SIC_Instruction.instruction.get(snd, "ERROR") + "0000"
                else:
                    # 處理其他指令
                    tokens = line.split()
                    snd = tokens[0] if len(tokens) == 2 else tokens[1]

                    if snd in SIC_Instruction.instruction:
                        thrd = tokens[-1]
                        ADD = 3

                        if len(tokens) == 3:
                            fst = tokens[0]
                            FUNC_LOC[fst] = LOCATION
                    else:
                        if snd == "END":
                            ADD = 0
                            thrd = tokens[-1]
                        else:
                            fst, snd, thrd = tokens[0], tokens[1], tokens[2]
                            FUNC_LOC[fst] = LOCATION

                            if snd == "BYTE":
                                ADD, obj_code = process_byte(thrd)
                            elif snd == "WORD":
                                ADD, obj_code = process_word(thrd)
                            elif snd == "RESB":
                                ADD, obj_code = process_resb(thrd)
                            elif snd == "RESW":
                                ADD, obj_code = process_resw(thrd)

            RESULT.append([hex(LOCATION)[2:].upper(), fst, snd, thrd, obj_code])
            LOCATION += ADD

        for idx in range(len(RESULT)):
            if RESULT[idx][0] == "":
                continue
            elif RESULT[idx][2] in ["END", "BYTE", "WORD", "RESB", "RESW"]:
                continue
            else:
                if not RESULT[idx][4]:
                    if ",X" in RESULT[idx][3]:
                        RESULT[idx][4] = SIC_Instruction.instruction.get(RESULT[idx][2], "ERROR") + hex(FUNC_LOC[RESULT[idx][3]] + int("8000", 16))[2:].upper().zfill(4)
                    else:
                        RESULT[idx][4] = SIC_Instruction.instruction.get(RESULT[idx][2], "ERROR") + hex(FUNC_LOC[RESULT[idx][3]])[2:].upper()

    # 將結果寫入輸出文件 "output.txt"
    with open("output.txt", "w", encoding="UTF-8") as fi:
        for i in range(len(RESULT)):
            fi.write(f"{(i + 1) * 5:<10}{RESULT[i][0].zfill(6):<10}{RESULT[i][1]:<10}{RESULT[i][2]:<10}{RESULT[i][3]:<10}{RESULT[i][4].zfill(6):<10}\n")

# 如果腳本被直接運行，執行組譯器函數
if __name__ == "__main__":
    assembler()
