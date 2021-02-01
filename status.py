# status page
defi=[['username','difficultly','record','time'],
['-',1,999.99,'-'],
['-',1,999.99,'-'],
['-',1,999.99,'-'],
['-',2,999.99,'-'],
['-',2,999.99,'-'],
['-',2,999.99,'-'],
['-',3,999.99,'-'],
['-',3,999.99,'-'],
['-',3,999.99,'-']]  # 初始化资料库用
import csv
import pygame
import operator
import inputbox
import mine

def getandmakeStatus():  # 获取并制作数据
    exf=open('status.csv') # 获取
    reader=csv.reader(exf)
    stlist=list(reader)
    dif1,dif2,dif3=[],[],[] # 分三难度资料
    for i in stlist:  
        if i[1]=='1':
            i[2]=float(i[2])
            dif1.append(i)
        elif i[1]=='2':
            i[2]=float(i[2])
            dif2.append(i)
        elif i[1]=='3':
            i[2]=float(i[2])
            dif3.append(i)
    dif1.sort(key=operator.itemgetter(2),reverse=False) # 分别依用时排序（低到高
    dif2.sort(key=operator.itemgetter(2),reverse=False)
    dif3.sort(key=operator.itemgetter(2),reverse=False)
    ars=[dif1,dif2,dif3]
    avt,tt=[],[] # 平均时，总时
    for j in ars:
        a=0 # 总时间（各难度
        for k in j:
            if k[0]!='-': # 不为预设
                a=a+k[2] 
        try:
            avt.append('{:.2f}'.format(a/(len(j)-3))) # 平均
        except ZeroDivisionError:
            avt.append('0')
        tt.append('{:.2f}'.format(a))  # 总时
    # 三难度（已排序，平均时，各个难度完成次数，总时间
    return(dif1,dif2,dif3,avt,[len(dif1),len(dif2),len(dif3)],tt)

def showStatus(): # 数据主页面
    pygame.init()
    s=pygame.display.set_mode((510,550))
    pygame.display.set_caption('Minesweeper Status')
    a,b,c,av,st,tt=getandmakeStatus() # 获取数据
    tips='TIP: R to reset your score.' # 按r刷掉数据
    mail='MAIL: chrispeng12345@163.com' # 我的邮箱(*/ω＼*)
    sure=False # 是否确定
    while True:
        for event in pygame.event.get(): 
            if event.type==pygame.QUIT: # 退出（回标题
                mine.main1()
            elif event.type==pygame.KEYDOWN: # 键盘
                if event.key==pygame.K_q: # 退标题
                    mine.main1()
                elif event.key==pygame.K_r: # 刷掉数据（有确认）
                    tips='TIP: are you sure? (Y/N)'
                    sure=True
                elif event.key==pygame.K_y and sure: # 按下y刷掉，下略
                    exf=open('status.csv','w',newline='')
                    writer=csv.writer(exf)
                    for line in defi:
                        writer.writerow(line)
                    exf.close()
                    sure=False
                    tips='TIP: Reset successfully.'
                elif event.key==pygame.K_n and sure: # 按n取消
                    tips='TIP: R to reset your score.'
                    sure=False
                elif event.key==pygame.K_a: # 按a进入列表页
                    showAll()
        s.fill((0,100,0)) # 浅绿背景 下面打印全部数据，略
        drawText(s,' Q to quit A to show all',0,0,15,(255,255,255))
        drawText(s,'Minesweeper Status',110,20,30,(255,255,0))
        drawText(s,'Easy Top 3',195,65,20,(255,0,0))
        drawText(s,'1.Username: '+a[0][0]+' Record:'+str(a[0][2])+' Time:'+a[0][3],10,90,16,(255,255,255))
        drawText(s,'2.Username: '+a[1][0]+' Record:'+str(a[1][2])+' Time:'+a[1][3],10,120,16,(255,255,255))
        drawText(s,'3.Username: '+a[2][0]+' Record:'+str(a[2][2])+' Time:'+a[2][3],10,150,16,(255,255,255))
        drawText(s,'Hard Top 3',195,175,20,(255,0,0))
        drawText(s,'1.Username: '+b[0][0]+' Record:'+str(b[0][2])+' Time:'+b[0][3],10,200,16,(255,255,255))
        drawText(s,'2.Username: '+b[1][0]+' Record:'+str(b[1][2])+' Time:'+b[1][3],10,230,16,(255,255,255))
        drawText(s,'3.Username: '+b[2][0]+' Record:'+str(b[2][2])+' Time:'+b[2][3],10,260,16,(255,255,255))
        drawText(s,'Expert Top 3',185,285,20,(255,0,0))
        drawText(s,'1.Username: '+c[0][0]+' Record:'+str(c[0][2])+' Time:'+c[0][3],10,310,16,(255,255,255))
        drawText(s,'2.Username: '+c[1][0]+' Record:'+str(c[1][2])+' Time:'+c[1][3],10,340,16,(255,255,255))
        drawText(s,'3.Username: '+c[2][0]+' Record:'+str(c[2][2])+' Time:'+c[2][3],10,370,16,(255,255,255))
        drawText(s,'Average Time',60,395,20,(255,0,0))
        drawText(s,'Easy:'+av[0]+' Hard:'+av[1]+' Expert:'+av[2],10,420,16,(255,255,255))
        drawText(s,'Easy:'+str(st[0]-3)+' Hard:'+str(st[1]-3)+' Expert:'+str(st[2]-3),310,420,16,(255,255,255))
        drawText(s,'Succeeded Times',310,395,20,(255,0,0))
        drawText(s,'Total Time Used',180,445,20,(255,0,0))
        drawText(s,'Easy:'+tt[0]+' Hard:'+tt[1]+' Expert:'+tt[2],105,470,16,(255,255,255))
        drawText(s,tips,30,500,16,(255,255,255))
        drawText(s,mail,230,500,16,(255,255,255))
        pygame.display.flip()

def showAll(): # 显示全部数据
    exf=open('status.csv') # 开文件，存内容
    reader=csv.reader(exf)
    al=list(reader)
    pygame.init()
    s=pygame.display.set_mode((510,550))
    pygame.display.set_caption('Minesweeper Status-All')
    tp=1
    while True: 
        for event in pygame.event.get():
            if event.type==pygame.QUIT: # 退回数据主页
                showStatus()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q: # 同上
                    showStatus()
                elif event.key==pygame.K_RIGHT: # 下一页
                    tp+=1
                elif event.key==pygame.K_LEFT: # 上一页
                    tp-=1
        if tp<=0: # 页数不可小于1
            tp=1
        s.fill((0,100,0)) # 浅绿背景
        le=len(al) # 数据行数
        if tp>int((le-9)/25)+1: # 页数不可超过
            tp=int((le-9)/25)+1
        if le>=35: # 第一页若不满35（每页25，前10个是预设不显示）就为其总数
            bb=35
        else:
            bb=le
        if tp==1: # 若第一页
            for kk in range(10,bb): # 印10-35（或不到
                drawText(s,str(al[kk]),10,(kk-10)*20+5+20,10,(255,255,255))
        try: # 若超过35，印每一页25行，若总数-10不是25的倍数会报错，懒得判定了。
            if bb!=le and tp>1: # 直接try expect（逃 ε=ε=ε=┏(゜ロ゜;)┛
                for kk in range(10+(tp-1)*25,bb+(tp-1)*25):
                    drawText(s,str(al[kk]),10,(kk-10-25*(tp-1))*20+5+20,10,(255,255,255))
        except IndexError: len('') # 经典空过（？
        drawText(s,'username     level       record(sec)      time',10,5,15,(255,255,255))
        drawText(s,'page.'+str(tp),400,500,16,(255,255,255)) # 页数
        drawText(s,'Q to quit',400,10,16,(255,255,255))
        pygame.display.flip() # 显示
    exf.quit() # 退文档

# 字体（这里又不会卡，不用像之前一样
def drawText(self,text,posx,posy,textHeight,fontColor=(0,0,0),backgroudColor=None):
    fontObj = pygame.font.Font('game.ttf', textHeight)
    textSurfaceObj = fontObj.render(text,True,fontColor,backgroudColor)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.left = posx
    textRectObj.top = posy
    self.blit(textSurfaceObj, textRectObj)

def writeStatus(dif,rec,time): # 写入数据（只有赢了才会
    screen = pygame.display.set_mode((320,240))
    name=inputbox.ask(screen,'Type your name here')
    exf=open('status.csv','a',newline='')
    writer=csv.writer(exf)
    writer.writerow([name,dif,rec,time])
    exf.close()

def showCmd(): # 打印到控制台
    exf=open('status.csv')
    reader=csv.reader(exf)
    i=list(reader)
    for a in i:
        print(a)
        
if __name__ == '__main__':
    showCmd()
    showStatus()