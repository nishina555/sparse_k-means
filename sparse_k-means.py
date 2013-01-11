#coding:utf-8

import sys
import random

#変数
#要素数の数をどれだけの規模でやるか(densesvectorの初期化の数)
width=14000
#n個の点
rows={}
k=int(sys.argv[1])
lastmatches=None
#k個のセントロイド
clusters={}
#k個のセントロイドの2乗を格納するもの
clusters_pow=[(0.0) for i in range(k)]
#点番号とtarget_wordを対応させるためのもの
number_word={}

#関数------------------
#ユークリッド距離の計算
def distance(clusters,clusters_pow,rows):
  dot_product=0.0
  for factor_num,count in rows.items():
    dot_product+=float(rows[int(factor_num)])*clusters[int(factor_num)]
  kyori=1+clusters_pow-2*dot_product
  return kyori
#関数ここまで----------------------

#入力を読み込む
for dot_num,line in enumerate(sys.stdin):
  line=line.strip().split(" ")
  target_word=line[0]
  #点番号とtarget_wordを対応させる辞書
  number_word[dot_num]=target_word
  #点番号のvectorを格納する辞書
  rows[dot_num]={}
  for i in range(1,int(len(line))):
    factor=line[i].strip().split(":")
    factor_num=int(factor[0])
    count=float(factor[1])
    rows[dot_num][factor_num]=count
#点の総数n
n=dot_num+1

#重心の初期化
#ランダムに点を選びそれをクラスタ中心とする
for i in range(k):
  #clustersはdense_vector
  clusters[i]=[0.0]*width 
  random_num=random.randint(0,dot_num)
  print random_num
  for factor_num,count in rows[random_num].items():
    clusters[i][int(factor_num)]+=float(count)
    #クラスタ中心の2乗の計算
    clusters_pow[i]+=pow(float(count),2)
  

#k-meansここから--------------------
for roop in range(0,100):
  #各点が所属するクラスタを格納するbestmatchesの初期化
  bestmatches=[[] for i in range(k)]
  for dot_num in range(n):
    bestmatch=0
    for i in range(k):
      d=distance(clusters[i],clusters_pow[i],rows[dot_num])
      if d<distance(clusters[bestmatch],clusters_pow[bestmatch],rows[dot_num]):
        bestmatch=i
    bestmatches[bestmatch].append(dot_num)
  if bestmatches==lastmatches:
    break
  lastmatches=bestmatches

  #重心の更新
  for i in range(k):
    clusters[i]=[0.0]*width
    clusters_pow[i]=(0.0)
    #そのクラスタにどれだけの点が属しているか
    sum_num=len(bestmatches[i])
    if sum_num==0:
      sum_num=1
    for dot_num in bestmatches[i]:
      for factor_num,count in rows[dot_num].items():
        clusters[i][int(factor_num)]+=float(rows[dot_num][int(factor_num)])
    for dense in range(width):
      clusters[i][dense]/=sum_num
      clusters_pow[i]+=pow(clusters[i][dense],2)
#k-meansここまで------------------------------------

#出力
print "ループ回数",roop
for i in range(k):
  print i,"クラスタ"
  for dot_num in bestmatches[i]:
    print number_word[dot_num],
  print "\n"
