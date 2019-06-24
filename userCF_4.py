# -*- coding=utf-8 -*-

import math

from texttable import Texttable


#
#   使用 |A&B|/sqrt(|A || B |)计算余弦距离
#   不考虑评分
#
#
#

def calcCosDistSpe(user1,user2):#认为分数为1
    avg_x=0.0
    avg_y=0.0
    for key in user1:
        avg_x+=key[1]
    avg_x=avg_x/len(user1)

    for key in user2:
        avg_y+=key[1]
    avg_y=avg_y/len(user2)

    u1_u2=0.0
    for key1 in user1:
        for key2 in user2:
            if key1[1] > avg_x and key2[1]>avg_y and key1[0]==key2[0]:
                u1_u2+=1
    u1u2=len(user1)*len(user2)*1.0
    sx_sy=u1_u2/math.sqrt(u1u2)
    return sx_sy

#
#   计算余弦距离:考虑评分
#
#
def calcCosDist(user1,user2):
    sum_x=0.0
    sum_y=0.0
    sum_xy=0.0
    for key1 in user1:
        for key2 in user2:
            if key1[0]==key2[0] :
                sum_xy+=key1[1]*key2[1]
                sum_y+=key2[1]*key2[1]
                sum_x+=key1[1]*key1[1]

    if sum_xy == 0.0 :
        return 0
    sx_sy=math.sqrt(sum_x*sum_y) 
    return sum_xy/sx_sy


#
#
#   相似余弦距离：
#
#
#
def calcSimlaryCosDist(user1,user2):
    sum_x=0.0
    sum_y=0.0
    sum_xy=0.0
    avg_x=0.0
    avg_y=0.0
    for key in user1:
        avg_x+=key[1]
    avg_x=avg_x/len(user1)

    for key in user2:
        avg_y+=key[1]
    avg_y=avg_y/len(user2)

    for key1 in user1:
        for key2 in user2:
            if key1[0]==key2[0] :
                sum_xy+=(key1[1]-avg_x)*(key2[1]-avg_y)
                sum_y+=(key2[1]-avg_y)*(key2[1]-avg_y)
                sum_x+=(key1[1]-avg_x)*(key1[1]-avg_x) #减去平均值是什么含义？

    if sum_xy == 0.0 :
        return 0
    sx_sy=math.sqrt(sum_x*sum_y) 
    return sum_xy/sx_sy


#
#   读取文件
#
#
def readFile(file_name):
    contents_lines=[]
    f=open(file_name,"r")
    contents_lines=f.readlines()
    f.close()
    return contents_lines



#
#   解压rating信息，格式：用户id\t硬盘id\t用户rating\t时间
#   输入：数据集合
#   输出:已经解压的排名信息
#
def getRatingInformation(ratings):
    rates=[]
    for line in ratings:
        rate=line.split("\t")
        rates.append([int(rate[0]),int(rate[1]),int(rate[2])])
    return rates


#
#   生成用户评分的数据结构
#   
#   输入:所以数据 [[2,1,5],[2,4,2]...]
#   输出:1.用户打分字典 2.兴趣字典
#   使用字典，key是用户id，value是用户对兴趣的评价，
#   rate_dic[2]=[(1,5),(4,2)].... 表示用户2对兴趣1的评分是5，对兴趣4的评分是2
##    2.兴趣字典：test_item_to_user[兴趣id]=[用户id1,用户id2...]
def createUserRankDic(rates):
    user_rate_dic={}
    item_to_user={}
    for i in rates:
        user_rank=(i[1],i[2])
        if i[0] in user_rate_dic:
            user_rate_dic[i[0]].append(user_rank)
        else:
            user_rate_dic[i[0]]=[user_rank]

        if i[1] in item_to_user:
            item_to_user[i[1]].append(i[0])
        else:
            item_to_user[i[1]]=[i[0]]
    return user_rate_dic,item_to_user


#
#   计算与指定用户最相近的邻居
#   输入:指定用户ID，所有用户数据，所有物品数据
#   输出:与指定用户最相邻的邻居列表
#      1.用户字典：test_dic[用户id]=[(兴趣id,兴趣评分)...]
#      2.兴趣字典：test_item_to_user[兴趣id]=[用户id1,用户id2...]
def calcNearestNeighbor(userid,users_dic,item_dic):
    neighbors=[]
    #neighbors.append(userid)
    for item in users_dic[userid]:
        for neighbor in item_dic[item[0]]:
            if neighbor != userid and neighbor not in neighbors: 
                neighbors.append(neighbor)

    neighbors_dist=[]
    for neighbor in neighbors:
        dist=calcCosDist(users_dic[userid],users_dic[neighbor])  #calcSimlaryCosDist(?) calcCosDist calcCosDistSpe
        neighbors_dist.append([dist,neighbor])
    neighbors_dist.sort(reverse=True)
    #print neighbors_dist
    return  neighbors_dist

def getHobbyList(file_name):
    hobbies_contents=readFile(file_name)
    hobbies_info={}
    for hobby in hobbies_contents:
        hobby_info=hobby.split("|")
        hobbies_info[int(hobby_info[0])]=hobby_info[1]
    return hobbies_info



#主程序
#输入 ： 测试数据集合
if __name__ == '__main__':

    hobbies=getHobbyList("C:\\Users\\Administrator\\AppData\\Local\Programs\\Python\\Python37\\Scripts\MV\\test.item")
    #读取文件数据
    test_contents=readFile("C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python37\\Scripts\\MV\\test.data")

    #文件数据格式化成二维数组 List[[用户id,兴趣id,兴趣评分]...] 
    test_rates=getRatingInformation(test_contents)

    #格式化成字典数据 
    #    1.用户字典：test_dic[用户id]=[(兴趣id,兴趣评分)...]
    #    2.兴趣字典：test_item_to_user[兴趣id]=[用户id1,用户id2...]
    test_dic,test_item_to_user=createUserRankDic(test_rates)
    rows=[]
    rows.append([u"neighbor1",u"neighbor2", u"neighbor3",u"neighbor4"])
    all_neighbors_dis=[]
    #for userid in test_dic:
    for userid in test_dic:
        neighbors=calcNearestNeighbor(userid,test_dic,test_item_to_user)[:39]
        #if userid not in all_neighbors_dis:
        #all_neighbors_dis.append([neighbors_dis[0],userid,neighbors_id[0]])
        for neighbor in neighbors:
            all_neighbors_dis.append([neighbor[0],userid,neighbor[1]])
        #全排序 all_neighbors_dis={[dis,usrid,neighbor],....}

        #格式化成字典数据
        #user_rate_dic[用户id]=[(距离，用户，邻居id)...]
        user_rate_dic={}
        for i in all_neighbors_dis:
            user_rank=(i[0],i[1],i[2])
            if i[1] in user_rate_dic:
                user_rate_dic[i[1]].append(user_rank)
            else:
                user_rate_dic[i[1]]=[user_rank]
        
    all_neighbors_dis.sort(reverse=True)
    #print("user_rate_dic[3]:",user_rate_dic[3])
    #print("user_rate_dic[10]:",user_rate_dic[10])
    #print("user_rate_dic[11]:",user_rate_dic[11])
    #print("user_rate_dic[28]:",user_rate_dic[28])
    #print("user_rate_dic[31]:",user_rate_dic[31])
    #print("user_rate_dic[32]:",user_rate_dic[32])
    killneighbors=[]
    #贪心法取最大nearest_neighbors_dis([距离,用户,邻居],...)
    #先从数组中去掉neighbors_id1和neighbors_id2
    a=len(all_neighbors_dis)
    for m in range(a):
        nearest_neighbors_dis=all_neighbors_dis.pop(0)

        #取用户和邻居添加到数组中
        neighbors_id1=nearest_neighbors_dis[1]
        neighbors_id2=nearest_neighbors_dis[2]
        if neighbors_id1 in killneighbors or neighbors_id2 in killneighbors:
            continue
        killneighbors.append(neighbors_id1)
        killneighbors.append(neighbors_id2)
        for item in user_rate_dic[neighbors_id2]:
            if item[2] not in killneighbors: 
                killneighbors.append(item[2])
                #且加到宿舍，第三个
                break
        for item2 in user_rate_dic[item[2]]:
            #找第三个的邻居
            if item2[2] not in killneighbors:
                killneighbors.append(item2[2])
                #todo 加到宿舍，第四个
                break
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(['t','t','t','t']) # automatic
        table.set_cols_align(["l", "l", "l", "l"])

        #print ("id1:",neighbors_id1)
        #print ("id2:",neighbors_id2)
        rows.append([neighbors_id1,neighbors_id2,item[2],item2[2]])
    table.add_rows(rows)
        #取下一个贪心最大值
    
    print (table.draw())
    #all_neighbors_dis.sort(reverse=True)
    #user_2=[ i[1] for i in all_neighbors_dis]
    #user_3=[ i[2] for i in all_neighbors_dis]
    #print (all_neighbors_dis)
   # print (user_2[0])
    #user_2_2=calcNearestNeighbor(user_2[0],test_dic,test_item_to_user)[:2]
    #user_2_2_id=[ i[1] for i in user_2_2]
   # user_2_2_dis=[ i[0] for i in user_2_2]
    #print (user_2_2)
   # print (user_3[0])
   # user_3_2=calcNearestNeighbor(user_3[0],test_dic,test_item_to_user)[:2]
   # user_3_2_id=[ i[1] for i in user_3_2]
   # user_3_2_dis=[ i[0] for i in user_3_2]
   # print (user_3_2)


"""
    neighbors_id=[ i[1] for i in neighbors]
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t',  # text 
                          't',  # float (decimal)
                          't']) # automatic
    table.set_cols_align(["l", "l", "l"])
    rows=[]
    rows.append([u"hobby name",u"hobby id", u"from userid"])
    for hobby_id in recommend_list[:4]:
        from_user=[]
        for user_id in items_hobby[hobby_id]:
            if user_id in neighbors_id:
                from_user.append(user_id)
        rows.append([hobbies[hobby_id][0],hobby_id,from_user])
    table.add_rows(rows)
    print (table.draw())
"""