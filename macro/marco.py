# 打開檔案並讀取內容
f = open('./1.txt', 'r')
Input = f.readlines()
f.close()

# 解析第一行，初始化主程式列表
temp = Input[0].replace('\n', '').split(' ')
if len(temp) == 3:
    main = [[5, temp[0], temp[1], temp[2]]]
else:
    main = [[5, '', temp[0], temp[1]]]

# 初始化巨集字典和巨集狀態
macro = {}
in_macro = [False, '']

line = 5
# 迭代處理每一行輸入
for i in Input[1:]:
    line += 5

    if i[0] == '.':
        continue

    i = i.replace('\n', '').split(' ')

    if len(i) == 1:
        now = [line, '', i[0], '']
    elif len(i) == 2:
        now = [line, '', i[0], i[1]]
    else:
        now = [line, i[0], i[1], i[2]]

    # 檢查是否進入巨集定義
    if now[2] == 'MACRO':
        in_macro = [True, now[1]]
        macro[now[1]] = [now[3].split(','), []]
        continue
    elif now[2] == 'MEND':
        in_macro = [False, '']
        continue

    # 如果在巨集中，將當前行添加到巨集中
    if in_macro[0]:
        macro[in_macro[1]][1].append(now)
    else:
        # 如果當前行是巨集調用
        if now[2] in macro:

            function_ = now[1]

            if now[1] != '':
                now[1] = f'.{now[1]}'
            
            main.append(now.copy())
            
            # 解析巨集引數
            parms = {}
            now[3] = now[3].split(',')
            for n, p in enumerate(macro[now[2]][0]):
                parms[p] = now[3][n]
            
            # 將巨集內容添加到主程式中
            macro[now[2]][1][0][1] = function_
            for n, j in enumerate(macro[now[2]][1]):
                j = j.copy()
                j[0] = str(line) + chr(ord('a')+n)
                for k in parms.keys():
                    if k in j[3]:
                        j[3] = j[3].replace(k, parms[k])

                main.append(j.copy())

        else:
            main.append(now)

# 輸出結果
print(" %-10s %-10s %-10s %-10s"%('行數', '', '原始碼', ''))
for i in main:
    if i[1] == '.':
        print(" %-10s %-10s %-10s %-39s"%(i[0], i[1], i[2], i[3]))
    else:
        print(" %-10s %-10s %-10s %-10s"%(i[0], i[1], i[2], i[3]))