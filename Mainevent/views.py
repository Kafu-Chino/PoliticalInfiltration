# -*- coding: utf-8 -*-
import json
import time,datetime
from collections import defaultdict
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.db.models import Q
from Mainevent.models import Task,Event_Analyze,Event,Figure


from rest_framework.views import APIView
from rest_framework.schemas import ManualSchema

from Mainevent.models import Hot_post

class Test(APIView):
    """测试页面"""
'''    def get(self, request):
        """获取用户信息"""
        # do something
        return HttpResponse('Hello world')

    def post(self, request):
        """获取用户信息"""
        pass

    def put(self, request):
        """更新用户信息"""
        pass

    def delete(self, request):
        """删除用户信息"""
        pass'''


class Task_create(APIView):
    """添加任务入库
       输入任务名称name、任务内容content和关键词keywords
       若成功输出{"status":201, "msg": "任务成功添加"}
       若失败输出{"status":400, "error": "请输入事件的名称，关键词和内容"}"""
    def get(self,request):
        times = int(time.time())
        dates = datetime.datetime.now().strftime('%Y-%m-%d')  # 获取当前时间戳和日期
        event_id = str(request.GET.get("name")) + str(times)  # 事件名+时间戳作为任务ID
        event_content = request.GET.get("content")
        keywords = request.GET.get("keywords")
        if event_id and keywords and event_content:
            Task.objects.create(t_id=event_id, status=0, text=event_content,keywords_dict=keywords, into_timestamp=times,
                                into_date=dates,task_type=1,into_type=1)
            return JsonResponse({"status":201, "msg": "任务成功添加"},safe=False,json_dumps_params={'ensure_ascii':False})
        else:
            return JsonResponse({"status":400, "error": "请输入事件的名称，关键词和内容"},safe=False,json_dumps_params={'ensure_ascii':False})

class Task_delete(APIView):
#展示的t_id作为id  选中时传入该id
    def get(self,request):
        tid = request.GET.get("id")
        result = Task.objects.filter(t_id=tid)
        if result.exists():
            try:
                Task.objects.filter(t_id=tid).delete() 
                return JsonResponse({"status":201, "msg": "任务已删除"},safe=False,json_dumps_params={'ensure_ascii':False})
            except:
                return JsonResponse({"status":400, "error": "删除失败"},safe=False,json_dumps_params={'ensure_ascii':False})
        else:
            return JsonResponse({"status":400, "error": "任务不存在"},safe=False,json_dumps_params={'ensure_ascii':False})


class Show_task(APIView):
    """展示任务列表
       输出{‘t_id(任务id)’: ,’keywords_dict(任务关键词)’: ,’status(计算状态)’: , ‘into_date(添入日期)’: },{},{}"""
    def get(self, request):
        result = Task.objects.values('t_id','keywords_dict','status','into_date')
        if result.exists():
            return HttpResponse(result)
        else:
            return JsonResponse({"status":400, "error": "无任务"},safe=False)
        json_data = serializers.serialize("json",result)
        results = json.loads(json_data)
        return JsonResponse(results,safe=False)

class Show_event(APIView):
    """展示事件列表
       输出{‘event_name(事件名称)’: ,’keywords_dict(事件关键词)’: ,’content(事件内容)’: , ‘begin_date(开始日期)’:  ,‘end_date(结束日期)’: },{},{}"""
    def get(self, request):
        result = Event.objects.values('event_name','keywords_dict','content','begin_date','end_date')
        if result.exists():
            return HttpResponse(result)
        else:
            return JsonResponse({"status":400, "error": "无事件"},safe=False)



class Show_event_info(APIView):
    """展示事件详情,点击事件传入事件eid
       输出{‘event_name(事件名称)’: ,’keywords_dict(事件关键词)’: ,’content(事件内容)’: , ‘begin_date(开始日期)’:  ,‘end_date(结束日期)’: },{},{}"""
    def get(self, request):
        eid = request.GET.get("eid")
        result = Event.objects.filter(e_id =eid).values('event_name','keywords_dict','content','begin_date','end_date')
        if result.exists():
            return HttpResponse(result)
        else:
            return JsonResponse({"status":400, "error": "无事件详情"},safe=False)



class Event_analy(APIView):
    """事件热度、敏感度、负面指数
       输入事件id:eid
       输出{"hot_index(热度)": ,"sensitive_index(敏感度)": ,"negative_index(负面指数)":}"""
    def get(self, request):
        """获取事件id:eid"""
        event_id = request.GET.get('eid') 
        res_dict= []
        times = time.time()
        result = Event_Analyze.objects.filter(e_id = event_id)
        if result.exists():
            for re in result:
                res_dict.append({"hot_index":re.hot_index,"sensitive_index":re.sensitive_index,"negative_index":re.negative_index})
            return JsonResponse(res_dict,safe=False,json_dumps_params={'ensure_ascii':False})
        else:
            return JsonResponse({"status":400, "error": "事件不存在"},safe=False,json_dumps_params={'ensure_ascii':False})


class representative_info(APIView):
    """输入事件id:eid 
       输出代表微博列表：[{"uid": ,"comment": ,"retweeted": ,"date": ,"text": ,"hazard": },{}...]"""
    def get(self, request):
        event_id = request.GET.get('eid')
        etime = request.GET.get('time')
        res = []
        e = Event.objects.filter(e_id = event_id)
        for item in e:
            info = item.information.all().filter(date=etime).order_by("hazard_index")[:5]
        for i in info:
            lt = time.localtime(i.timestamp)
            itime = time.strftime("%Y-%m-%s %H:%M:%S",lt)
            res.append({"uid":i.uid,"comment":i.comment,"retweeted":i.retweeted,"date":itime,"text":i.text,"hazard":i.hazard_index})
        return JsonResponse(res,safe=False,json_dumps_params={'ensure_ascii':False})


class search_event(APIView):
    """搜索事件 输入事件标题title 输出'event_name','keywords_dict','content','begin_date','end_date'"""
    def get(self, request):
        name = request.GET.get("title")
        result = Event.objects.filter(event_name__contains = name).values('event_name','keywords_dict','content','begin_date','end_date')
        if result.exists():
            return HttpResponse(result)
        else:
            return JsonResponse({"status":400, "error": "该事件不存在"},safe=False)




class figure_info(APIView):
    """人物和信息关联分析"""

    def get(self, request):
        """获取事件eid，返回该事件的相关人物和相关信息,
        数据格式{
                    "figure":[{"f_id": uid, "nick_name": nick_name,"fansnum":fansnum,"friendsnum":friendsnum,"domian":domain,"political":political},{}],
                    "information":[{"text": text1, "hazard_index": hazard_index1},{}]
                }
        """
        res_dict = defaultdict(list)
        eid = request.GET.get('eid')
        res_event = Event.objects.filter(e_id=eid)  #.first().event_set.all()
        for e in res_event:
            res = e.figure.all()
            for f in res:
                res_dict["figure"].append({"f_id": f.f_id, "nick_name": f.nick_name,"fansnum":f.fansnum,"friendsnum":f.friendsnum,"domian":f.domain,"political":f.political})
            #res_dict["figure"].append({"f_id": f.f_id, "nick_name": f.nick_name,"fansnum":f.fansnum,"friendsnum":f.friendsnum,"domian":f.domain,"political":f.political})
        #res_information = Information.objects.filter(e_id=eid)
        #for i in res_information:
            res1 = e.information.all()
            for i in res1:
                res_dict["info"].append({"text": i.text, "hazard_index": i.hazard_index,"keywords":i.keywords_dict,"comment":i.comment,"retweet":i.retweeted})
        if len(res_dict["figure"]) or len(res_dict["info"]):
            return JsonResponse(res_dict,safe=False,json_dumps_params={'ensure_ascii':False})
        else:
            return JsonResponse({"status":400, "error": "无相关人物和信息"},safe=False)


import os
import sys
import re
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'PoliticalInfiltration.settings'
class Sen_info(APIView):
    """展示敏感微博内容涉及到的敏感词
       输入：敏感微博id：id
       输出：{‘sw(敏感词汇)’:{},…, ‘info’:{‘text’(敏感信息内容)：，‘hazard_index(危险指数)’：，‘keywords(关键词)’: , ‘comment(评论数)’：，‘retweet(转发数)’：}}"""
    def get(self,request):
        swords = []
        for b in open(os.path.abspath(os.path.join(ABS_PATH, '../Cron/profile_cal/sensitive_words.txt')), 'r'):
            swords.append(b.strip().split('\t')[0])
        iid = request.GET.get('id')
        result = Information.objects.filter(i_id=iid).values("uid",'text','keywords_dict','comment','retweeted','date','hazard_index')
        res = defaultdict(list)
        #results = json.dumps(result)
        for i in result:
            for word in swords:
            #print(type(word))
                pattern = re.compile(r".*(%s)" % word)
                if pattern.search(i['text']): 
                    res["sw"].append(word)
            res["info"].append(i)
        #json_data = serializers.serialize("json",result)
        #results = json.loads(json_data)
        return JsonResponse(res,safe=False,json_dumps_params={'ensure_ascii':False})



class push_Hotpost(APIView):
    """页面响应,从数据库取热帖展示"""
    def get(self):
        hot_posts = Hot_post.objects.all().values_list()  # 取出所有列，QuerySet类型
        hot_posts = list(hot_posts)  # [(data),(data)]
        # 元组(data):
        # (h_id, uid, root_uid, mid, comment, retweeted, text, keywords_dict, timestamp, date, ip, geo, message_type, root_mid, source, store_timestamp, store_date, similar_event)
        # 例如:
        # ('h_1', 'user_1', 'user_1', 'm_1', 0, 0, '测试热帖库信息', 't1,t2,t3,t4,t5', 1567923180, datetime.date(2019, 9, 8), '127.0.0.1', '北京市', 1, 'm_1', '微博', 1567925639, datetime.date(2019, 9, 8), None)
        hot_post_display = []
        for item in hot_posts:
            a_post = {}
            a_post["h_id"] = item[0]
            a_post["uid"] = item[1]
            a_post["root_uid"] = item[2]
            a_post["mid"] = item[3]
            a_post["comment"] = item[4]
            a_post["retweeted"] = item[5]
            a_post["text"] = item[6]
            a_post["keywords_dict"] = item[7]
            a_post["timestamp"] = item[8]
            a_post["date"] = item[9].strftime('%Y-%m-%d')
            a_post["ip"] = item[10]
            a_post["geo"] = item[11]
            a_post["message_type"] = item[12]
            a_post["root_mid"] = item[13]
            a_post["source"] = item[14]
            a_post["store_timestamp"] = item[15]
            a_post["store_date"] = item[16].strftime('%Y-%m-%d')
            a_post["similar_event"] = item[17]
            hot_post_display.append(a_post)
        results = json.dumps(hot_post_display)
        return JsonResponse(results, safe=False)  # json [{data},{data}]


class Person_show(APIView):
    """用户主表展示"""
    def get(self, request):
        """
        用户展示大表信息
        输入：
        pagenum：当前页码数（以1起始）
        pagelimit：每页显示个数
        输出：
        uid：用户id
        nick_name：人物昵称
        create_at：注册时间
        user_location：注册地点
        fansnum：粉丝数
        friendsnum：关注数
        information_num：发布敏感信息数
        events_name：相关渗透事件
        """
        page_num = int(request.GET.get('pagenum', 1)) - 1
        page_limit = int(request.GET.get('pagelimit', 10))
        persons = Figure.objects.all()[page_num * page_limit : (page_num + 1) * page_limit]
        results = []

        # 批量得到用户相关信息统计
        persons_uid = [p.uid for p in persons]
        informations = Information.objects.filter(uid__in=persons_uid)
        information_count = {uid:0 for uid in persons_uid}
        for i in informations:
            information_count[i.uid] += 1

        # 批量得到用户相关事件统计
        events = Event.objects.filter(figure__uid__in=persons_uid).values_list("event_name", "figure__uid")
        events_name = {uid:[] for uid in persons_uid}
        for e in events:
            event_name, uid = e
            events_name[uid].append(event_name)

        for person in persons:
            dic = {
                "uid":person.uid,
                "nick_name":person.nick_name,
                "create_at":ts2date(int(person.create_at)),
                "user_location":person.user_location,
                "fansnum":person.fansnum,
                "friendsnum":person.friendsnum,
                "information_num":information_count[person.uid],
                "events_name":events_name[person.uid]
            }
            results.append(dic)
        return JsonResponse(results, safe=False)
