import deepcut
import requests
from bs4 import BeautifulSoup
import re
import regex
import numpy as np
import codecs
import time
from pymongo import MongoClient
import os
import glop


# function get news from website thairath only
def get_news(URL):
    data = requests.get(URL)
    soup = BeautifulSoup(data.text, 'html.parser')
    header = soup.find_all("h1")
    date_news = soup.find_all("div", {"class": "css-1cxbv8p evs3ejl7"})
    content = soup.find_all("p")

    text = ''
    # for i in header:
    #   text += i.text
    # for z in date_news:
    #   text += z.text
    for j in content:
        text += j.text

    return text


def word_tokenize(text):
    data = deepcut.tokenize(text, custom_dict='/dictionary/custom_dict.txt')
    return data


def tag_object(read_text):
    #     read_file = codecs.open('aof1.txt','r','utf8')
    #     read_text = read_file.read()

    # tad_date_and_time
    regex_time = r"(([0-1][\d]|[2][0-4])\s?(:|.)([0-5][\d])\s?(นาฬิกา|น\.|น)|(ช่วง|ตอน)(เช้า|ค่ำ|เย็น|ดึก|บ่าย|สาย|กลางดึก))"
    matches_time = regex.sub(regex_time, r'<time>\1</time>', read_text)
    read_text = matches_time
    regex_date = (
        r"(([1-9]|[0-2][\d]|[3][0-1])\s?(/|-)?(ม\.ค\.|มกราคม|มกรา|ก\.พ\.|กุมภาพันธ์|กุมภา|มี\.ค\.|มีนาคม|มีนา|เม\.ย\.|"
        "เมษายน|เมษา|พ\.ค\.|พฤษภาคม|พฤษภา|มิ\.ย\.|มิถุนายน|มิถุนา|ก\.ค\.|กรกฎาคม|กรกฎา|ส\.ค\.|สิงหาคม|สิงหา|ก\.ย\.|"
        "กันยายน|กันยา|ต\.ค\.|ตุลาคม|ตุลา|พ\.ย\.|พฤศจิกายน|พฤศจิกา|ธ\.ค\.|ธันวาคม|ธันวาคม)\s?(/|-)?(พ.ศ.|ค.ศ.|พศ|คศ)?\s?"
        "(\d\d\d\d|\d\d)?|([1-9]|[0-2][\d]|[3][0-1])\s?(/|-|.)([0][\d]|[1][0-2])\s?(/|-|.)(\d\d\d\d|\d\d))")
    matches_date = regex.sub(regex_date, r'<date>\1</date>', read_text)
    read_text = matches_date

    # read_dictionary
    read_file_p = codecs.open('dictionary/จังหวัด.txt', 'r', 'utf8')
    read_p = read_file_p.read()
    read_p_list = read_p.split('\n')
    list_str_p = '|'.join(read_p_list[:len(read_p_list) - 1])
    list_str_p += '|' + read_p_list[len(read_p_list) - 1]

    read_file_c = codecs.open('dictionary/ประเทศ.txt', 'r', 'utf8')
    read_c = read_file_c.read()
    read_c_list = read_c.split('\n')
    list_str_c = '|'.join(read_c_list[:len(read_c_list) - 1])
    list_str_c += '|' + read_c_list[len(read_c_list) - 1]

    read_file_t = codecs.open('dictionary/ตำบล.txt', 'r', 'utf8')
    read_t = read_file_t.read()
    read_t_list = read_t.split('\n')
    list_str_t = '|'.join(read_t_list[:len(read_t_list) - 1])
    list_str_t += '|' + read_t_list[len(read_t_list) - 1]

    read_file_a = codecs.open('dictionary/อำเภอ.txt', 'r', 'utf8')
    read_a = read_file_a.read()
    read_a_list = read_a.split('\n')
    list_str_a = '|'.join(read_a_list[:len(read_a_list) - 1])
    list_str_a += '|' + read_a_list[len(read_a_list) - 1]

    read_file_area = codecs.open('dictionary/เขต.txt', 'r', 'utf8')
    read_area = read_file_area.read()
    read_area_list = read_area.split('\n')
    list_str_area = '|'.join(read_area_list[:len(read_area_list) - 1])
    list_str_area += '|' + read_area_list[len(read_area_list) - 1]

    read_file_d = codecs.open('dictionary/แขวง.txt', 'r', 'utf8')
    read_d = read_file_d.read()
    read_d_list = read_d.split('\n')
    list_str_d = '|'.join(read_d_list[:len(read_d_list) - 1])
    list_str_d += '|' + read_d_list[len(read_d_list) - 1]

    read_file_r = codecs.open('dictionary/ถนน.txt', 'r', 'utf8')
    read_r = read_file_r.read()
    read_r_list = read_r.split('\n')
    list_str_r = '|'.join(read_r_list[:len(read_r_list) - 1])
    list_str_r += '|' + read_r_list[len(read_r_list) - 1]

    read_file_ri = codecs.open('dictionary/แม่น้ำ.txt', 'r', 'utf8')
    read_ri = read_file_ri.read()
    read_ri_list = read_ri.split('\n')
    list_str_ri = '|'.join(read_ri_list[:len(read_ri_list) - 1])
    list_str_ri += '|' + read_ri_list[len(read_ri_list) - 1]

    read_file_m = codecs.open('dictionary/ห้าง.txt', 'r', 'utf8')
    read_m = read_file_m.read()
    read_m_list = read_m.split('\n')
    list_str_m = '|'.join(read_m_list[:len(read_m_list) - 1])
    list_str_m += '|' + read_m_list[len(read_m_list) - 1]

    read_file_h = codecs.open('dictionary/โรงบาล1.txt', 'r', 'utf8')
    read_h = read_file_h.read()
    read_h_list = read_h.split('\n')
    list_str_h = '|'.join(read_h_list[:len(read_h_list) - 1])
    list_str_h += '|' + read_h_list[len(read_h_list) - 1]

    read_file_uni = codecs.open('dictionary/มหาลัย.txt', 'r', 'utf8')
    read_uni = read_file_uni.read()
    read_uni_list = read_uni.split('\n')
    list_str_uni = '|'.join(read_uni_list[:len(read_uni_list) - 1])
    list_str_uni += '|' + read_uni_list[len(read_uni_list) - 1]

    # tag location
    regex_province2 = (r"(((?<!ผว)จ\.|จังหวัด|จว.)\s?(" + list_str_p + "){e<=1}|(กรุงเทพ))")

    regex_province = (r"<province_fail>((จ\.|จังหวัด|จว.)\s?(" + list_str_p + ")|(กรุงเทพ))</province_fail>")

    regex_country2 = (r"((ประเทศ)\s?(" + list_str_c + "){e<=1})")

    regex_country = (r"<country_fail>((ประเทศ)\s?(" + list_str_c + "))</country_fail>")

    regex_area2 = (r"((เขต)\s?(" + list_str_area + "){e<=1})")

    regex_area = (r"<area_fail>((เขต)\s?(" + list_str_area + "))</area_fail>")

    regex_district2 = (r"((แขวง)\s?(" + list_str_d + "){e<=1})")

    regex_district = (r"<district_fail>((แขวง)\s?(" + list_str_d + "))</district_fail>")

    regex_road2 = (r"((ถ\.|ถนน|ทาง)\s?(" + list_str_r + "){e<=1})")

    regex_road = (r"<road_fail>((ถ\.|ถนน|ทาง)\s?(" + list_str_r + "))</road_fail>")

    regex_amphoe2 = (r"(((?<!นาย)อำเภอ|อ\.)\s?(" + list_str_a + "){e<=1})")

    regex_amphoe = (r"<amphoe_fail>(((?<!นาย)อำเภอ|อ\.)\s?(" + list_str_a + "))</amphoe_fail>")

    regex_river2 = (r"((แม่น้ำ)(" + list_str_ri + "){e<=1})")

    regex_river = (r"<river_fail>((แม่น้ำ)(" + list_str_ri + "))</river_fail>")

    regex_tambon2 = (r"((ตำบล|\sต\.)\s?(" + list_str_t + "){e<=1})")

    regex_tambon = (r"<tambon_fail>(\s?(ตำบล|ต\.)\s?(" + list_str_t + ")\s?)</tambon_fail>")

    regex_all = (
        r"((?!ซอยดังกล่าว|ซอยหอ|ซอยหรือ|ซอยมี|ซอยถัด|สน.ที่|ซอยริมถนน|ซอยข้าง|ซอยเข้า|ซอยเปลี่ยว|ซอยที่เกิดเหตุ|ซอยตัน|ซอยหลบ|ซอยแคบ|ซอยด้วย|ซอยไม่มีชื่อ|ซอยข้างบ้าน|สน.ออก)(ซอย|\sซ\.|(?<!ท|\.)สภ\.|สน\.)(\d\d?|[ก-๙]{2,}(?=ชัก|ไป|สอบ|ได้|จะ|ดำเนิน|มายัง|ต่อไป|จับกุม|เพื่อ|กล่าว|ดำเนิน|และ|รับเเจ้ง|ได้รับ|รับตัว)"
        "|(?!ตาย|เพื่อ|ได้|ของ|ใกล้|แล้ว|ให้)[ก-๙]{2,}\s?(\d?\d?))|(?!ย่านถนน|ย่านชุมชน|ย่านซอย)(ย่าน)([ก-๙]{2,}(?=ตาย|หาเงิน|เพื่อ)|[ก-๙]{2,})(\s?\d?\d?)|(บ้านเลขที่|ห้องเลขที่|บ้านเช่าเลขที่)\s?(\d\d?\d?)"
        "(/)?(\d?\d?\d?)|((หมู่|หมู่ที่|\sม\.)\s?(\d\d?))|((ที่|ใน|คา)(?<!พนักงาน)โรงแรม|โรงเรียน|โรงรับจำนำ)(?!ทั้ง|แห่งนี้|แต่|กับ|เพราะ|เป็น|ที่|ส่วน|สั่ง|แห่งเดียว|จะได้|เดียว|ได้สั่ง|ก็โดน|ใน|มี|ต่างหาก|ก็เห็น|ใกล้|ตนได้|และ|ว่า|ที่เกิดเหตุ)([ก-๙]{2,}(?=ชื่อ|ใน|ริม)|(?!จริง|ชื่อ|ดังกล่าว)[ก-๙]{2,})|"
        "(?!ที่คอนโดมิเดียมแห่งนี้)(บริเวณ|ภายใน|ที่|ใน|คา)(คอนโด|แมนชั่น|อะพาร์ตเมนต์|หน้าผับ|ผับ|ห้องเช่า|ห้องแถว)|"
        "(?!ที่ร้านอาหารดังกล่าว|ที่ร้านขายแต่)(บริเวณ|ภายใน|ที่|ใน|คา)(หน้าร้าน|ร้าน)(กาแฟ[ก-๙]{2,}|ข้าว[ก-๙]{2,}|อาหาร[ก-๙]{2,}(?=ใน|ชื่อ|ย่าน)|อาหาร[ก-๙]{2,}|"
        "ซ่อม[ก-๙]{2,}(?=ดังกล่าว)|ซ่อม[ก-๙]{2,}|ขาย[ก-๙]{2,}(?=ชื่อ|และ|ที่อยู่)|ขาย[ก-๙]{2,}|ทำ[ก-๙]{2,}|เสริม[ก-๙]{2,}|ร้านน้ำ[ก-๙]{2,}|สะดวกซื้อ|เซเว่นอีเลฟเว่น|เซเว่น|กาแฟ|อาหาร|คาราโอเกะ"
        "|เฟอร์นิเจอร์|เคเอฟซี|พิซซ่า|ทอง)|(ที่|ใน|คา)(บ้านพัก|บ้านหลังหนึ่ง|บ้านแห่งหนึ่ง|บ้านเช่า))")

    regex_mall = (r"((ห้างสรรพสินค้า|ห้าง)(?!ดัง)(" + list_str_m + "))")
    regex_mall2 = (r"((?!ห้างฉัตร)(ห้างสรรพสินค้า|ห้าง)((?!ร้าน|ดัง|เปิด|และ|ค้า|ได้|ซึ่ง)[ก-๙]{2,}))")

    regex_hos = (r"((โรงพยาบาล|ร\.พ\.|รพ\.)(?!ได้|ตำบล|สต)(" + list_str_h + "))")
    regex_hos2 = (
        r"((โรงพยาบาล|ร\.พ\.|รพ\.)(?!เสียก่อน|เป็น|เอง|ทันที|หลาย|โทร|ได้|เพื่อ|ว่า|ให้การ|ตำบล|สต|แล้ว|ใน|ใส่|ขณะ|เดิน|ได้แล้ว|เขาก็|ใกล้|ก่อนหน้า|ดังกล่าว)([ก-๙]{2,}(?=หาสาเหตุ|อาการ|ทันที|โดย|อีก|เพื่อ|ในเวลา)|[ก-๙]{2,}))")

    regex_university = (r"((มหาวิทยาลัย|มหาลัย)(" + list_str_uni + "))")
    regex_university2 = (
        r"((มหาวิทยาลัย|มหาลัย)(?!แล้ว|หลาย|ได้|เพื่อ|ตำบล|ชื่อดัง|ดังกล่าว|ที่เคย|ต้นสังกัด|ไม่)([ก-๙]{2,}))")

    matches_province2 = regex.sub(regex_province2, r'<province_fail>\1</province_fail>', read_text)
    read_text = matches_province2
    matches_province = regex.sub(regex_province, r'<province>\1</province>', read_text)
    read_text = matches_province
    matches_country2 = regex.sub(regex_country2, r'<country_fail>\1</country_fail>', read_text)
    read_text = matches_country2
    matches_country = regex.sub(regex_country, r'<country>\1</country>', read_text)
    read_text = matches_country
    matches_area2 = regex.sub(regex_area2, r'<area_fail>\1</area_fail>', read_text)
    read_text = matches_area2
    matches_area = regex.sub(regex_area, r'<area>\1</area>', read_text)
    read_text = matches_area
    matches_district2 = regex.sub(regex_district2, r'<district_fail>\1</district_fail>', read_text)
    read_text = matches_district2
    matches_district = regex.sub(regex_district, r'<district>\1</district>', read_text)
    read_text = matches_district
    matches_road2 = regex.sub(regex_road2, r'<road_fail>\1</road_fail>', read_text)
    read_text = matches_road2
    matches_road = regex.sub(regex_road, r'<road>\1</road>', read_text)
    read_text = matches_road
    matches_tambon2 = regex.sub(regex_tambon2, r'<tambon_fail>\1</tambon_fail>', read_text)
    read_text = matches_tambon2
    matches_tambon = regex.sub(regex_tambon, r'<tambon>\1</tambon>', read_text)
    read_text = matches_tambon
    matches_amphoe2 = regex.sub(regex_amphoe2, r'<amphoe_fail>\1</amphoe_fail>', read_text)
    read_text = matches_amphoe2
    matches_amphoe = regex.sub(regex_amphoe, r'<amphoe>\1</amphoe>', read_text)
    read_text = matches_amphoe
    matches_river2 = regex.sub(regex_river2, r'<river_fail>\1</river_fail>', read_text)
    read_text = matches_river2
    matches_river = regex.sub(regex_river, r'<river>\1</river>', read_text)
    read_text = matches_river
    matches_all = regex.sub(regex_all, r'<place>\1</place>', read_text)
    read_text = matches_all
    matches_mall2 = regex.sub(regex_mall2, r'<mall2>\1</mall2>', read_text)
    read_text = matches_mall2
    matches_mall = regex.sub(regex_mall, r'<mall>\1</mall>', read_text)
    read_text = matches_mall
    matches_hos2 = regex.sub(regex_hos2, r'<hospital2>\1</hospital2>', read_text)
    read_text = matches_hos2
    matches_hos = regex.sub(regex_hos, r'<hospital>\1</hospital>', read_text)
    read_text = matches_hos
    matches_university2 = regex.sub(regex_university2, r'<university2>\1</university2>', read_text)
    read_text = matches_university2
    matches_university = regex.sub(regex_university, r'<university>\1</university>', read_text)
    read_text = matches_university
    return read_text


if __name__ == '__main__':
    # connect to database on mongodb atlas cloud
    # database = "mongodb+srv://student:m789789123@cluster0-ds9da.mongodb.net/test?retryWrites=true"
    # client = MongoClient(database, connectTimeout=200)
    # check status to connect
    # print(client.status)
    # show list data base
    # print(client.list_database_names())
    # use database client
    # datanews = client.datanews
    # print(datanews.list_collection_names())

    URL = input("Enter URL:")
    news = get_news(URL)

    print(tag_object(news))
