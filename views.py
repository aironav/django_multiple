from bdb import set_trace
from tabnanny import check
from textwrap import indent
from tkinter import N
from unittest import result
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
import mysql.connector as sql
import json
import jsonpickle

def run_query():
    result_sql = """
                    select sa.code, sa.type, sd.type, smn.memberid, group_concat(sd.code) from stg_claim sc 
                    join stg_activity sa on sc.uniqueid = sa.fkclaimuniqueid 
                    join stg_diagnosis sd on sc.uniqueid = sd.fkclaimuniqueid 
                    join sherlock_memberdetails_new smn on sc.memberid = smn.memberid 
                    group by 1,2,3,4;
                """
                    #  select sherlock_memberdetails_new.memberid, sherlock_memberdetails_new.member_type, 
                    #  sherlock_memberdetails_new.member_name, sherlock_memberdetails_new.birth_dt, sherlock_memberdetails_new.relation,
                    #  sherlock_memberdetails_new.policy_start_date, sherlock_memberdetails_new.policy_end_date, 
                    #  sherlock_memberdetails_new.emirate, stg_diagnosis.claim_no , group_concat(stg_diagnosis.code)
                    #  from sherlock_memberdetails_new join stg_claim on sherlock_memberdetails_new.memberid = stg_claim.memberid 
                    #  join stg_diagnosis on stg_claim.uniqueid = stg_diagnosis.fkclaimuniqueid where ren_no=(select max(ren_no) 
                    #  from sherlock_memberdetails_new) group by 1,2,3,4,5,6,7,8,9;


                    #  select sherlock_memberdetails_new.memberid, sherlock_memberdetails_new.member_type, 
                    #  sherlock_memberdetails_new.member_name, sherlock_memberdetails_new.birth_dt, sherlock_memberdetails_new.relation,
                    #  sherlock_memberdetails_new.policy_start_date, sherlock_memberdetails_new.policy_end_date, 
                    #  sherlock_memberdetails_new.emirate, stg_diagnosis.code, stg_diagnosis.claim_no from 
                    #  sherlock_memberdetails_new join stg_claim on sherlock_memberdetails_new.memberid = stg_claim.memberid 
                    #  join stg_diagnosis on stg_claim.uniqueid = stg_diagnosis.fkclaimuniqueid where ren_no=(select max(ren_no) 
                    #  from sherlock_memberdetails_new);

                    # select sa.code, sa.type, sd.type, smn.memberid, group_concat(sd.code) from stg_claim sc 
                    # join stg_activity sa on sc.uniqueid = sa.fkclaimuniqueid and sa.type = '3' 
                    # join stg_diagnosis sd on sc.uniqueid = sd.fkclaimuniqueid 
                    # join sherlock_memberdetails_new smn on sc.memberid = smn.memberid 
                    # group by 1,2,3,4;
                 
    result_conn = sql.connect(host="127.0.0.1", database="batch", user="root", password="qwertyuiop")
    result_cursor = result_conn.cursor()
    result_cursor.execute(result_sql)
    result_db = result_cursor.fetchall()
    return result_db

# def run_query_policy():
    result_sql_policy = """
                     select sherlock_memberdetails_new.contract_no, sherlock_memberdetails_new.member_type, 
                     sherlock_memberdetails_new.member_name, sherlock_memberdetails_new.birth_dt, sherlock_memberdetails_new.relation,
                     sherlock_memberdetails_new.policy_start_date, sherlock_memberdetails_new.policy_end_date, 
                     sherlock_memberdetails_new.emirate, stg_diagnosis.claim_no , group_concat(stg_diagnosis.code)
                     from sherlock_memberdetails_new join stg_claim on sherlock_memberdetails_new.memberid = stg_claim.memberid 
                     join stg_diagnosis on stg_claim.uniqueid = stg_diagnosis.fkclaimuniqueid where ren_no=(select max(ren_no) 
                     from sherlock_memberdetails_new) group by 1,2,3,4,5,6,7,8,9;
                """
    result_conn = sql.connect(host="127.0.0.1", database="batch", user="root", password="qwertyuiop")
    result_cursor = result_conn.cursor()
    result_cursor.execute(result_sql_policy)
    result_policy = result_cursor.fetchall()
    return result_policy

def index(request):
    return HttpResponse("Hello world!")
    
def checkIcd(request):
    result_db = run_query()
    policy_member = []
    member_obj = Member.objects.all().values_list('member_id')
    for mem in member_obj:
        policy_member.append(mem[0])
    member_list = []
    icd_list = []
    for i in result_db:
        member_list.append(i[3])
        icd_list.append(i[4])
    matched_member = set(policy_member) & set(member_list)
    print(matched_member)
    if (matched_member):
        json_data = jsonpickle.encode(matched_member)
        return JsonResponse({"mapped member_id":json_data})
    else:
        return JsonResponse({"msg":"not matched"})

def checkmember_exclusions():
    result_db = run_query()
    icd_list = []
    member_list = []
    icd_ids = []
    member_ids = []
    
    icd_obj = MemberExclusion.objects.all().values_list('icd4_code', 'member')
    for icd in icd_obj:
        icd_ids.append(icd[0])
        member_ids.append(icd[1])
    for ids in member_ids:
        member_list.append(Member.objects.filter(id=ids).values_list('member_id')[0][0])
    for ids in icd_ids:
        icd_list.append(ICD.objects.filter(id=ids).values_list('icd4_code')[0][0])
    member_data = list(zip(member_list,icd_list))
    map_dict = {}
    for i in result_db:
        map_dict[i[3]] = i[4].split(',')
    unmapped_icd = {}
    mapped_icd = {}
    for key,values in map_dict.items():
        for memb in member_data:
            if str(memb[0]) == str(key):
                member_value = []
                member_value.append(memb[1])
                # print(set(values) - set(member_value))
                unmapped_icd[memb[0]] = set(values) - set(member_value)
                mapped_icd[memb[0]] = set(values).intersection(set(member_value))
    return mapped_icd
    # print(unmapped_icd)
    # if (unmapped_icd):
    #     json_data = jsonpickle.encode(unmapped_icd)
    #     return JsonResponse({"unmapped icd":json_data})
    # else:
    #     mapped_json_data = jsonpickle.encode(mapped_icd)
    #     return JsonResponse({"mapped icd":mapped_json_data})


def checkmember_inclusions(request):
    result_db = run_query()
    icd_list = []
    member_list = []
    icd_ids = []
    member_ids = []
    exc_icd = checkmember_exclusions()
    icd_obj = MemberInclusion.objects.all().values_list('icd4_code', 'member')
    for icd in icd_obj:
        icd_ids.append(icd[0])
        member_ids.append(icd[1])
    for ids in member_ids:
        member_list.append(Member.objects.filter(id=ids).values_list('member_id')[0][0])
    for ids in icd_ids:
        icd_list.append(ICD.objects.filter(id=ids).values_list('icd4_code')[0][0])
    member_data = list(zip(member_list,icd_list))
    map_dict = {}
    for i in result_db:
        map_dict[i[3]] = i[4].split(',')
    unmapped_icd = {}
    mapped_icd = {}
    for key,values in map_dict.items():
        for memb in member_data:
            if str(memb[0]) == str(key):
                member_value = []
                member_value.append(memb[1])
                # print(set(values) - set(member_value))
                unmapped_icd[memb[0]] = set(values) - set(member_value)
                mapped_icd[memb[0]] = set(values).intersection(set(member_value))
    both_dict = {}
    for i in mapped_icd:
        for j in exc_icd:
            if i == j:
                both_dict[i] = 1
            else:
                both_dict[i] = 0

    print(both_dict)
    inex = []
    for key, value in both_dict.items():
        if value == 1:
            inex.append(key)
        else:
            pass
    print(inex)
    return JsonResponse({'icd present in both inclusion and exclusion': json.dumps(inex)})



    #return JsonResponse({'msg':json.dumps(both_dict)})

    # return mapped_icd

    # import pdb
    # pdb.set_trace()
    # print(unmapped_icd)
    # if (unmapped_icd):
    #     json_data = jsonpickle.encode(unmapped_icd)
    #     return JsonResponse({"unmapped icd":json_data})
    # else:
    #     mapped_json_data = jsonpickle.encode(mapped_icd)
    #     return JsonResponse({"mapped icd":mapped_json_data})



    



