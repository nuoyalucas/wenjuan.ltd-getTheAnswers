#先导入一大堆标准库和第三方库
import json
import requests
from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk
import re

#发起request并将json转化为dic
def get_json(url):
    pyreg=re.compile("\"questionpage_list\":(.*)\"version\"");
    response=pyreg.findall(requests.get(url).text)[0]
    firstCut=response.lstrip(" ")
    lastCut=firstCut.strip(", ")
    project=json.loads(lastCut)
    return project

#中心部分，解析答案
def get_answer(project):
    information = 0
    answer_data = []
    for x in range(len(project)):
        for y in range(len(project[x]["question_list"])):
            """ 这一段条件判断是检测是否有个人信息需要填写，如果有，information+1 """
            custom_attr = project[x]["question_list"][y]["custom_attr"]
            if("content_type" in custom_attr and custom_attr["content_type"] == "classes") or \
              ("disp_type" in custom_attr and custom_attr["disp_type"] == "name") or \
              ("disp_type" in custom_attr and custom_attr["disp_type"] == "mobile") or \
              ("content_type" in custom_attr and custom_attr["content_type"] == "student_id") or \
              ("disp_type" in custom_attr and custom_attr["disp_type"] == "employee_id") or \
              ("disp_type" in custom_attr and custom_attr["disp_type"] == "sex") or \
              ("content_type" in custom_attr and custom_attr["content_type"] == "department") or \
              ("disp_type" in custom_attr and custom_attr["disp_type"] == "email"):
                information += 1
                continue
            ques_title="第"+str(int(project[x]["question_list"][y]["cid"].replace("Q",""))-information)+"题"
            for z in range(len(project[x]["question_list"][y]["option_list"])):
                answer=project[x]["question_list"][y]["option_list"][z]["custom_attr"]
                if ("correct_answer" in answer and answer["correct_answer"] != None):
                    if (answer["correct_answer"] in project[x]["question_list"][y]["extra_option_id_list"]):
                        for item in range(len(project[x]["question_list"][y]["extra_option_id_list"])):
                            optionList=[chr(i) for i in range(65,65+item)]
                        answer_data.append(ques_title+":"+optionList[project[x]["question_list"][y]["extra_option_id_list"].index(answer["correct_answer"])])
                    else:
                        answer_data.append(ques_title+":"+answer["correct_answer"])

                elif ("is_correct" in answer and answer["is_correct"] == "1"):
                    answer_data.append(ques_title+":"+project[x]["question_list"][y]["option_list"][z]["title"])
                    
                elif ("cloze_option_answer" in answer and answer["cloze_option_answer"] != None):
                    answer_data.append(ques_title+":"+answer["cloze_option_answer"])
    if information > 0:
        print("本场考试须填写个人信息，请自行填写")
    return answer_data

#将答案绘制到画布上
def draw_in_canvas(data):
    root = Tk()
    monty = ttk.LabelFrame(root, text=" 答案 ")  # 创建一个容器，其父容器为win
    monty.grid(column=0, row=0, padx=10, pady=10)
    scr = scrolledtext.ScrolledText(monty,width=100, height=30, wrap=WORD)
    for item in data:
        scr.insert(END,item+"\n")
    scr.grid(column=0, columnspan=3)
    root.mainloop()

#主程序
def main(url):
    project=get_json(url)
    data=get_answer(project)
    draw_in_canvas(data)

if __name__ == "__main__":
    main(input("请输入考试的网址"))

