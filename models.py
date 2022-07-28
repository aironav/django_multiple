from re import sub
from django.db import models

class Plan(models.Model):
    id = models.AutoField(primary_key=True)
    plan_code = models.CharField(max_length=64, null=True)
    plan_name = models.CharField(max_length=64, null=True)
    plan_group = models.CharField(max_length=64, null=True)
    plan_sub_group = models.CharField(max_length=64, null=True)
    plan_category = models.CharField(max_length=64, null=True)
    plan_class = models.CharField(max_length=64, null=True)

    def __str__(self):
        return self.plan_name



class Policy(models.Model):

    plan = models.ForeignKey(Plan, null=False, on_delete= models.CASCADE)
    id = models.AutoField(primary_key=True)
    policy_id = models.CharField(max_length=16, null=False, blank=False)
    name = models.CharField(max_length=50, null=False)
    sex = models.BinaryField(null=False)
    policy_start_date = models.DateTimeField(null=False)
    policy_end_date = models.DateTimeField(null=False)
    dob = models.DateField(null=False)
    annual_benefit_limit = models.IntegerField(null=False)

    def __str__(self):
        return self.name


class Member(models.Model):
    id = models.AutoField(primary_key=True)
    plan = models.ForeignKey(Plan, null=False, on_delete= models.CASCADE)
    policy = models.ForeignKey(Policy, null=False, on_delete= models.CASCADE)
    member_id = models.CharField(max_length=32, null=False, blank=False)
    member_name = models.CharField(max_length=20, null=True) 
    relation = models.CharField(max_length=20, null=True)
    dob = models.DateField(null=False)


    def __str__(self):
        return self.member_name


class ICDAdd(models.Model):
    id = models.AutoField(primary_key=True)
    icd = models.CharField(max_length=16 ,null=False)
    member = models.ForeignKey(Member,null=False,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.icd