import sys
sys.dont_write_bytecode = True
import psd_tools
import cv2
import numpy as np
import pathlib
import re

def layer2img(layer):
    img = layer.topil() # pilにとりあえず変換
    if img is None: #レイヤーに何もない時
        return img, False
    # print(img)
    dst = np.array(img, dtype = np.uint8) # グレースケールならこれでよい
    # print(dst)
    if dst.shape[2] == 3: # RGBの場合
        dst = cv2.cvtColor(dst, cv2.COLOR_RGB2BGR)
    elif dst.shape[2] == 4: # RGBAの場合
        dst = cv2.cvtColor(dst, cv2.COLOR_RGBA2BGRA)
    return dst, True

exts = [".jpg", ".png", ".jpeg", ".bmp", ".webp", ".JPG", ".PNG", ".JPEG", ".BMP", ".WEBP", '.psd', '.PSD']
srcDirPath = pathlib.Path(sys.argv[1])
src_paths = sorted([p for p in srcDirPath.iterdir() if p.suffix in exts])

dst_dir = pathlib.Path('dst_layers')
if(not dst_dir.exists()): dst_dir.mkdir() #フォルダがない時に作る

for i in range(len(src_paths)): # ルートのアイテムをループ
    # i =  375#ファイル名
    psd = psd_tools.PSDImage.open(f'{src_paths[i]}')
    # print(i, psd[i])
    for x in range(len(psd)):
        if psd[x].is_group(): # ルートがフォルダの場合
            for j in range(len(psd[x])): # フォルダ内はループ
                print(x, j, psd[x][j])           
                img,flag = layer2img(psd[x][j])
                if flag: #
                    # print(img, flag)
                    # ファイル名に使えないものは置換
                    file_name = psd[x][j].name
                    file_name = re.sub(r'[\\|/|:|?|.|"|<|>|\|]', '_', file_name)
                    cv2.imwrite(f"dst_layers/{src_paths[i].stem}_{x:03}_{j:02}_{file_name}.png", img)
        else: # フォルダじゃなければレイヤー
            img,flag  = layer2img(psd[x])
            if flag:               
                # print(img)
                file_name = psd[x].name
                file_name = re.sub(r'[\\|/|:|?|.|"|<|>|\|]', '_', file_name)
                cv2.imwrite(f"dst_layers/{src_paths[i].stem}_{x:03}_{file_name}.png", img)
    # break #処理を終了