# -*- coding: utf-8 -*-
# 这个是个扫雷游戏，包含游戏本身，历史记录，三个难度。
# 如此简单的小游戏本人却用了两个py文件，加起来近600行才写完，属实拉跨，轻喷
# 此文件包含：__pycache__，game.ttf，mine.py，status.py，status.csv，inputbox.py
# status.py:数据记录 status.csv：数据记录 inputbox.py 输入栏 game.ttf 自定义字体
# imports 不多，良心了好吧（误） 记得装 pygame,csv,operator，这几个少见，你大概没有(doge)

import pygame
import random
import status
import time

# 棋盘长宽&每格长宽&旗帜数
NUMS=['',10,18,24]
BLWD=['',50,30,25]
FLAG=['',10,40,99]

# 起始画面
def sp():
    pygame.init()
    scr=pygame.display.set_mode((500,500))
    pygame.display.set_caption('set difficulty')
    while True:
        dif=checkEvents() # 检查事件
        scr.fill((0,100,0)) # 浅绿色背景
        drawStartPage(scr)  # 按钮和文字
        pygame.display.flip() 
        if dif in [1,2,3]: 
            return dif

def checkEvents():
    for event in pygame.event.get(): # 退出
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    pygame.quit()
                if event.key==pygame.K_a:
                    status.showStatus()
            elif event.type==pygame.MOUSEBUTTONDOWN: # 鼠标
                if event.button==1:  # 左键
                    mx,my=pygame.mouse.get_pos() # 获取点位
                    if mx>=100 and mx<=400:
                        if my>=60 and my<=140:
                            return 1    # 简单
                        elif my>=200 and my<=280:
                            return 2    # 中等
                        elif my>=340 and my<=420:
                            return 3    # 困难
                    if mx>=350 and mx<=460:
                        if my>=450 and my<=480: # 查看数据
                            status.showStatus() 

def drawStartPage(scr): # 主页的按钮
    pygame.draw.rect(scr,(0,200,0),((100,60),(300,80)))
    pygame.draw.rect(scr,(0,200,0),((100,200),(300,80)))
    pygame.draw.rect(scr,(0,200,0),((100,340),(300,80)))
    pygame.draw.rect(scr,(0,200,0),((350,450),(110,30)))
    drawText(scr,'Easy (size: 10x10 10 bm )',250,100,23)
    drawText(scr,'Hard (size: 18x18 40 bm )',250,240,23)
    drawText(scr,'Expt (size: 24x24 99 bm )',250,380,23)
    drawText(scr,'Difficultly',250,35,20,(255,255,255))
    drawText(scr,'Leaderboard',405,465,15)


# 游戏界面 必须确认第一次按的是空地，避免太差的体验，所以复杂了点（ps：参数为难度
def main(diff): 
    pygame.init()
    COUNT=pygame.USEREVENT+1 # 自定义pygame事件（计时
    pygame.time.set_timer(COUNT,1)
    outrun=True # 外循环结束条件 因为内部循环需要多次结束并重新赋值参数
    fcx,fcy=0,0 # 局第一次点击（矫正安全对局用
    firstclick=True # 是否第一次点（每一局）
    while outrun: # 外循环（如果第一次点的不是空格，会跳出来继续循环）
        arr=[] # 模拟排雷位置用的
        for ii in range(NUMS[diff]**2): # 平方为总格数
            arr.append(ii) # 赋值0到地板的数量
        # 围着左上角的三个格子不能方雷（因为写的太烂了不让放（答应我别说出去
        del arr[1],arr[NUMS[diff]-1],arr[NUMS[diff]-1]
        lei=[] # 雷区
        if diff==1: # 依难度
            sx,sy=50*10,50*10+50  # 以难度窗口计算长宽（高留50计时
            lei.append(random.sample(arr,10)) # 随机抽几个位子放雷
        elif diff==2: # 下同
            sx,sy=30*18,30*18+50
            lei.append(random.sample(arr,40))
        elif diff==3:
            sx,sy=25*24,25*24+50
            lei.append(random.sample(arr,99))
        scr=pygame.display.set_mode((sx,sy)) # 依照难度设置窗口大小
        pygame.display.set_caption('minesweeper') # 扫雷
        ground=[] # 地面，内装一堆Block对象
        for i in range(NUMS[diff]**2):  # 设置地面，竖排数下来
            if i in lei[0]: # 是雷
                tpn=9  # tpn设为Block.mine值，详见该class
            else: # 不是雷暂时为空地
                tpn=0  # （0为空，1-8数字，9雷
            # 将设置好的Block放入地面arr（参数意义详见该class
            ground.append(Block(scr,int(i/NUMS[diff]),i%NUMS[diff],diff,tpn,i))
        for j in range(NUMS[diff]**2): # 放数字
            if j==0: # 若是第一格（前面伏笔的部分（因为周围没雷
                continue # 原本因为下方计算需要除，但不能除0，求大神帮改
            if ground[j].mine!=9: # 若不为雷
                if j%NUMS[diff]!=0: # 若该格不在第一横列
                    search(j,1,diff,ground) # 搜该格上方有无雷
                if (j+1)%NUMS[diff]!=0: # 若该格不在最后一横列
                    search(j,2,diff,ground) # 搜该格下方有无雷
                if j>=NUMS[diff]: # 以此类推，顺序↑↓←→↖↙↗↘
                    search(j,3,diff,ground)
                if j<=NUMS[diff]**2-1-NUMS[diff]:
                    search(j,4,diff,ground)
                if (j%NUMS[diff]!=0) and (j>=NUMS[diff]):
                    search(j,5,diff,ground)
                if (j>=NUMS[diff]) and ((j+1)%NUMS[diff]!=0):
                    search(j,6,diff,ground)
                if (j<=NUMS[diff]**2-1-NUMS[diff]) and (j%NUMS[diff]!=0):
                    search(j,7,diff,ground)
                if (j<=NUMS[diff]**2-1-NUMS[diff]) and ((j+1)%NUMS[diff]!=0):
                    search(j,8,diff,ground) # 此函数简单说会查若有雷将数字+1，详见该函数
        run=True # 内循环（小局）是否运行
        notdead=True # 没死
        startedcount=False # 还未开始计时
        counts=0 # 计时变量清零
        winned=False # 没赢呢 （ps：没死不代表赢了哦owo
        while run: # 主循环（内
            if fcx!=0 and fcy!=0 and startedcount==False: # 如果是在确认安全开局循环中
                counts=0 # 计时清零
                startedcount=True # 开始计时
            if fcx!=0 and fcy!=0: # 若在确认开局安全中（没按前fcx,fcy默认0,0）
                ax,ay=int(fcx/BLWD[diff]),int((fcy-50)/BLWD[diff]) # 当作按下与上次相同位置
                if ground[ax*NUMS[diff]+ay].mine!=0: # （ax,ay为按下位置换算格子坐标）
                    run=False # ground[ax*NUMS[diff]+ay]正好为该按下格的Block对象，
                else: # (接上)若该格为非空地，重开  然后若为空格：
                    ground[ax*NUMS[diff]+ay].dig(ground) # 可以安心挖开惹
                    fcx,fcy=0,0 # 设fcx,fcy为0,0，停止安全开局测试
            for event in pygame.event.get(): # 事件侦测
                if event.type==pygame.QUIT: # 退出
                    pygame.quit()
                elif event.type==pygame.KEYDOWN: # 键盘
                    if event.key==pygame.K_q: # 按下q
                        run=False # 停止内外循环
                        outrun=False
                        if not winned: # 若没赢早退，设记录999.99s以便return（无用不可删）
                            rttt=999.99
                    elif event.key==pygame.K_a: # 按下a （正常玩没事别按
                        necularbomb(ground) # 格子全开（将导致失败）（因为雷也开了嘛doge
                elif event.type==COUNT: # 计时
                    if startedcount and notdead==True and winned==False:
                        counts+=1 # 若开始计时，没死，没赢，计时
                elif event.type==pygame.MOUSEBUTTONDOWN and notdead and not winned: # 滑鼠（没死没赢情况下
                    cx,cy=pygame.mouse.get_pos() # cx,cy为滑鼠按下确切坐标
                    ax,ay=int(cx/BLWD[diff]),int((cy-50)/BLWD[diff]) # ax,ay为格子坐标
                    if event.button==1: # 左键
                        if firstclick: # 若第一次按（安全开局用
                            fcx,fcy=cx,cy 
                            if ground[ax*NUMS[diff]+ay].mine!=0: # 同上安全开局措施
                                run=False
                            else:
                                ground[ax*NUMS[diff]+ay].dig(ground)
                            firstclick=False
                        else: # 若为一般局内按下
                            if ground[ax*NUMS[diff]+ay].mine==9 and ground[ax*NUMS[diff]+ay].sts=='':
                                notdead=False # 若该格子没旗子，挖了，是雷，那就死了
                            if ground[ax*NUMS[diff]+ay].sts=='': # 没旗子
                                ground[ax*NUMS[diff]+ay].dig(ground) # 挖了挖了
                    if event.button==3: # 右键
                        ground[ax*NUMS[diff]+ay].flag() # 插旗
            if notdead==False: # 若死了
                necularbomb(ground) # 把格子全开了
            win=True # 下方测试是否胜利
            for ww in ground: # 遍历全图
                if ww.mine==9 and ww.digged: # 若踩雷 没赢（甚至输了
                    win=False 
                elif ww.mine!=9 and not ww.digged: # 若不是雷的却没开，那也没赢
                    win=False
                else:
                    continue
            winned=win # 若该挖的都挖了，那就赢了呗
            scr.fill(0xffffff) # 背景白
            flag=0 # 测插旗数用
            for i in range(0,NUMS[diff]**2): # 遍历全图
                ground[i].drawme() # 画格子
                if ground[i].digged==False and ground[i].sts!='': # 插旗了
                    flag+=1
            # 画状态栏
            drawText(scr,'flag : '+str(FLAG[diff]-flag),int(sx/3),25,int(sx/16),(255,0,0))
            drawText(scr,'time : '+'{:.2f}'.format(counts/100),int(sx/3)*2,25,int(sx/16),(255,0,0))
            if notdead==False: # 死了，画死亡画面
                drawText(scr,'GAME OVER',int(sx/12.5)+int(sx/2.4),int(sx/2.73)+int(sx/6.4),int(sx/6.43),(255,0,0))
                drawText(scr,'--------------------------------------------------------',int(sx/12.5)+int(sx/2.4),int(sx/1.84)+int(sx/10),int(sx/22.5),(255,0,0))
                drawText(scr,"PRESS 'Q' TO TRY AGAIN",int(sx/3.54)+int(sx/5),int(sx/1.71)+int(sx/6.4),int(sx/25),(255,0,0))
                rttt='{:.2f}'.format(counts/100) # 记录用时
            if winned==True: # 赢了，画胜利画面
                drawText(scr,' YOU WIN ',int(sx/12.5)+int(sx/2.4),int(sx/2.73)+int(sx/6.4),int(sx/6.43),(255,0,0))
                drawText(scr,'--------------------------------------------------------',int(sx/12.5)+int(sx/2.4),int(sx/1.84)+int(sx/10),int(sx/22.5),(255,0,0))
                drawText(scr,"PRESS 'Q' TO TRY AGAIN",int(sx/3.54)+int(sx/5),int(sx/1.71)+int(sx/6.4),int(sx/25),(255,0,0))
                rttt='{:.2f}'.format(counts/100) # 记录用时
            pygame.display.update() # 刷新画面 然后 return 是否胜利，难度，用时，当前时间
    return winned,diff,rttt,time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

def search(n,di,diff,ground): # 查雷并加数字
    cgit=False 
    if di==1: # 按参数12345678对应↑↓←→↖↙↗↘查
        if ground[n-1].mine==9: cgit=True
    elif di==2:
        if ground[n+1].mine==9: cgit=True
    elif di==3:
        if ground[n-NUMS[diff]].mine==9: cgit=True
    elif di==4:
        if ground[n+NUMS[diff]].mine==9: cgit=True
    elif di==5:
        if ground[n-NUMS[diff]-1].mine==9: cgit=True
    elif di==6:
        if ground[n-NUMS[diff]+1].mine==9: cgit=True
    elif di==7:
        if ground[n+NUMS[diff]-1].mine==9: cgit=True
    elif di==8:
        if ground[n+NUMS[diff]+1].mine==9: cgit=True
    if cgit: # 是雷，数字加一
        ground[n].cg()

class Block(): # Block对象
    def __init__(self,screen,x,y,diff,mine,gid): # 初始化(参数屏幕，格坐标，难度，数字，id)
        self.screen=screen
        self.x=x
        self.y=y
        self.gid=gid # 这个gid就是该block在ground中的位置
        self.digged=False # 是否挖开
        if self.x % 2 == 0 and self.y % 2 == 0: # xy坐标都是双数
            self.color=0x85f285 # 外面浅绿
            self.insideColor=0xf2dc85 # 里面浅土色
        elif self.x % 2 == 1 and self.y % 2 == 1: # xy都是单数
            self.color=0x85f285 # 同上
            self.insideColor=0xf2dc85
        else: # 其他情况
            self.color=0x57ed57 # 外深绿里深土
            self.insideColor=0xebca48
        self.diff=diff 
        if self.diff==1: self.width=50 # 依难度设格数（ps都方形哦
        if self.diff==2: self.width=30
        if self.diff==3: self.width=25
        self.mine=mine 
        if self.mine==0: self.nc=(0,0,0) # 空地或雷的话字体黑色
        if self.mine>=9: self.nc=(0,0,0)
        self.sts='' # 表层符号（旗子或空）
        self.bmb='*~●' # 雷的图案（我很机智吧 233)
    def cg(self): # search函数中用，周围有雷，数字+1 另外附上字体颜色
        self.mine+=1
        if self.mine==1: self.nc=(0,150,255) # 颜色自己看awa rgb
        if self.mine==2: self.nc=(0,205,102)
        if self.mine==3: self.nc=(255,0,0)
        if self.mine==4: self.nc=(139,101,8)
        if self.mine==5: self.nc=(139,69,19)
        if self.mine==6: self.nc=(0,0,205)
        if self.mine==7: self.nc=(54,54,54)
        if self.mine==8: self.nc=(41,112,112)
    def flag(self): # 改变表层状态（插旗不插旗）
        if self.sts=='/■': # 若为旗子，改为没旗子
            self.sts=''
        else: # 不然就插旗子
            self.sts='/■'
    def dig(self,ground,shut=False): # 挖（若是空格周围也要开（连锁反应也要考虑
        self.digged=True # 挖开了
        if self.mine==0 and shut==False: # 若是空地（shut在necularbomb中为了避免过度连锁而设
            gs=[self.gid-1,self.gid+1,   # 该格八方格的gid
                           self.gid-NUMS[self.diff],
                           self.gid+NUMS[self.diff],
                           self.gid-NUMS[self.diff]-1,
                           self.gid-NUMS[self.diff]+1,
                           self.gid+NUMS[self.diff]-1,
                           self.gid+NUMS[self.diff]+1]
            ck=[] # 要侦测的方向
            if self.gid%NUMS[self.diff]!=0: # 条件略(然鹅这里太长，求大神优化)(我懒了doge)
                ck.append(1)
            if (self.gid+1)%NUMS[self.diff]!=0:
                ck.append(2)
            if self.gid>=NUMS[self.diff]:
                ck.append(3)
            if self.gid<=NUMS[self.diff]**2-1-NUMS[self.diff]:
                ck.append(4)
            if (self.gid%NUMS[self.diff]!=0) and (self.gid>=NUMS[self.diff]):
                ck.append(5)
            if (self.gid>=NUMS[self.diff]) and ((self.gid+1)%NUMS[self.diff]!=0):
                ck.append(6)
            if (self.gid<=NUMS[self.diff]**2-1-NUMS[self.diff]) and (self.gid%NUMS[self.diff]!=0):
                ck.append(7)
            if (self.gid<=NUMS[self.diff]**2-1-NUMS[self.diff]) and ((self.gid+1)%NUMS[self.diff]!=0):
                ck.append(8)
            rgs=[] # 要侦测的方向的格子的Block对象（们
            for p in range(len(gs)): 
                if p+1 in ck: # 略
                    rgs.append(ground[gs[p]])
            try:
                tempnum=0
                for ab in range(len(rgs)):
                    if rgs[ab].digged==False and rgs[ab].mine!=9: # 若还没挖，且不是雷
                        rgs[ab].dig(ground) # 挖了挖了
                        tempnum=ab
            except IndexError: # 防止报错(ground[-1]不符合什么的)(然后接着)
                for ab in range(tempnum+1,len(rgs)):
                    if rgs[ab].digged==False and rgs[ab].mine!=9: # 同上
                        rgs[ab].dig(ground) 
    def drawme(self): # 画自己（？
        if self.digged: # 挖过了，显示里色
            cl=self.insideColor
        else: # 没挖，显示外色
            cl=self.color
        pygame.draw.rect(self.screen,cl,
                     ((self.x*self.width,self.y*self.width+50),
                      (self.width,self.width))) # 画方块
        if self.digged: # 挖了
            if self.mine > 0 and self.mine < 9: # 是数字，画数字
                drawText(self.screen,str(self.mine),self.x*self.width+self.width/2,self.y*self.width+50+self.width/2,int(self.width*7/10),self.nc)
            elif self.mine==9: # 是雷，画雷
                drawText(self.screen,self.bmb,self.x*self.width+self.width/2,self.y*self.width+50+self.width/2,int(self.width*2/5))
        elif self.sts!='': # 没挖，插旗了，画旗子
            drawText(self.screen,self.sts,self.x*self.width+self.width/2,self.y*self.width+50+self.width/2,int(self.width*2/5),(255,0,0))
        
def necularbomb(gr): # 开全格（函数名为核弹233
    for b in gr:
        b.dig(gr,shut=True)
        
# 画字体函数
g_textHeight=0 # 为了减少fontObj调用次数，防止卡顿，在更改字体大小时才重新赋值
fontObj_=0     # 大幅减少卡顿，但是expert后期依旧小卡，求大佬优化
def drawText(self,text,posx,posy,textHeight,fontColor=(0,0,0),backgroudColor=None):
    global g_textHeight,fontObj_  
    if g_textHeight !=textHeight:
        g_textHeight=textHeight
        fontObj_ = pygame.font.Font('game.ttf',textHeight)
    fontObj=fontObj_
    textSurfaceObj = fontObj.render(text,True,fontColor,backgroudColor)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (posx, posy)
    self.blit(textSurfaceObj, textRectObj)

def main1(): # 真·主循环
    while True:
        difficulty=sp() # 难度&开始画面
        wi,di,re,ti=main(difficulty) # 局内信息与游戏画面
        if wi: # 若胜利
            status.writeStatus(di,re,ti) # 写入数据库
            
if __name__=='__main__':
    main1()