###############################################################################
#
# 
#   디비전송 프로그램입니다.
#   upload_match_result(original_movie_seq, sub_movie_seq, match_detail_list) 함수를 사용하면 됩니다.
#
#
#   match_detail_list는 아래 예시가 있습니다.
#
#   match_detail_list = [
#       {"original_img_seq":-1,"sub_img_path": "./img/sample2.jpg","compare_hash":"sample"},
#       {"original_img_seq":-1,"sub_img_path": "./img/sample3.jpg","compare_hash":"sample"},
#       {"original_img_seq":-1,"sub_img_path": "./img/sample4.jpg","compare_hash":"sample"}
#   ]
#
#
#################################################################################
import requests
import sys
import json

def match_insert(original_movie_seq,sub_movie_seq, search_date):
    body = {"sub_file_seq": sub_movie_seq, "original_movie_seq": original_movie_seq, "search_date":search_date}
    headers={"Content-type" : "application/json"}
    r = requests.post("http://13.209.99.61:8080/detect_hit", data=json.dumps(body), headers = headers)
    r.json()
    print(r.json())
    return r.json()


def upload_sub_img(img_path, seq):
    url = "http://13.209.99.61:8080/sub_img/uploadFile"
    fin = open(img_path, 'rb')
    files = {'file': fin}
    r = requests.post(url, files=files)
    fin.close()
    sub_img_uri = r.json()["fileDownloadUri"];
    #print("sub img link : "+sub_img_uri+"\n")
    body={
            "sub_file_seq" : seq,
            "img_path" : sub_img_uri,
            "img_hash" : "sample",
            "compare_hash" : "sample"
    } 
    headers={"Content-type" : "application/json"}
    r = requests.post("http://13.209.99.61:8080/sub_img", data=json.dumps(body), headers = headers)
    r.json()
    print(r.json())
    return r.json()

def upload_match_detail(match_seq, original_img_seq, sub_img_seq, compare_hash):
    body={
            "detect_hit_seq" : match_seq,
            "sub_img_seq" : sub_img_seq,
            "original_img_seq" : original_img_seq,
            "compare_hash" : compare_hash
    } 
    headers={"Content-type" : "application/json"}
    r = requests.post("http://13.209.99.61:8080/detect_detail", data=json.dumps(body), headers = headers)
    r.json()
    print(r.json())
    return r.json()
    

def upload_match_result(original_movie_seq,sub_movie_seq, match_detail_list):

    match_table_dto = match_insert(original_movie_seq, sub_movie_seq,"2018-11-01T12:00:00")##TODO NOW로
    match_seq = match_table_dto["seq"]
    for eachImg in match_detail_list:
        sub_img_dto = upload_sub_img(eachImg["sub_img_path"],sub_movie_seq)
        upload_match_detail(match_seq, eachImg["original_img_seq"], sub_img_dto["seq"], eachImg["compare_hash"])  
         

#### main Stream Start
if __name__ == ""__main__"":
    match_detail_list = [
        {"original_img_seq":-1,"sub_img_path": "./img/sample2.jpg","compare_hash":"sample"},
        {"original_img_seq":-1,"sub_img_path": "./img/sample3.jpg","compare_hash":"sample"},
        {"original_img_seq":-1,"sub_img_path": "./img/sample4.jpg","compare_hash":"sample"}
    ]

    upload_match_result(1,1,match_detail_list)






