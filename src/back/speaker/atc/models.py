from django.db import models
from fns.models import *


class CallType(models.Model):
    name = models.CharField(
        max_length=255, blank=False, verbose_name='Тип вызова')

    class Meta:
        verbose_name = "Типы вызовов"
        verbose_name_plural = "Типы вызовов"

    def __str__(self):
        return str(self.name)


class CallCauses(models.Model):
    name = models.CharField(
        max_length=255, blank=False, verbose_name='Причины разъеденения')

    class Meta:
        verbose_name = "Причины разъеденений"
        verbose_name_plural = "Причины разъеденений"

    def __str__(self):
        return str(self.name)


class Sources(models.Model):
    name = models.CharField(max_length=255, blank=False)

    class Meta:
        verbose_name = 'Справочник источников'
        verbose_name_plural = 'Справочник источников'

    def __str__(self):
        return str(self.name)



class Calls(models.Model):
    call_type = models.ForeignKey(
        CallType, on_delete=models.DO_NOTHING, blank=False, verbose_name='Звонки')
    time_fixation = models.DateTimeField(blank=False)
    # date_fixation = models.DateField(null=True, db_index=True)
    code_domen_a = models.ForeignKey(Ufns,on_delete= models.DO_NOTHING,
         blank=True, null=True, verbose_name='Код домена А',related_name='ufns_code_a')
  
    number_a = models.CharField(
        max_length=255, blank=False, verbose_name='Номер А', db_index=True)
    code_domen_b = models.ForeignKey(Ufns,on_delete=models.DO_NOTHING,
         blank=False, verbose_name='Код домена Б',related_name='ufns_code_b')
   
    number_b = models.CharField(
        max_length=255, blank=True,null=True, verbose_name='Номер Б')
    subscriber_b = models.ForeignKey(
        Ad, on_delete=models.DO_NOTHING, blank=False, verbose_name='Абонент Б')
    
    
    call_duration = models.IntegerField(default=0, db_index=True)
    causes_disconnect = models.ForeignKey(
        CallCauses, on_delete=models.DO_NOTHING, blank=True,null=True,  verbose_name='Причины разъеденения')
    source = models.ForeignKey(
        Sources, on_delete=models.DO_NOTHING,  blank=True,null=True, verbose_name='Источник')
    outcaller_fullname = models.CharField(default='', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Звонки'
        verbose_name_plural = 'Звонки'
        unique_together = ["subscriber_b", "time_fixation"]
        ordering = ["time_fixation"]
        

    def __str__(self):
        return str(self.time_fixation)













class CallsView(models.Model):
    id = models.CharField(primary_key=True)
    call_type=models.ForeignKey(CallType, on_delete=models.CASCADE)
    date_fixation=models.DateField()
    # hour=models.IntegerField()   
    department = models.ForeignKey(Deps, on_delete=models.CASCADE)
    depdirection = models.ForeignKey(DepDirection, on_delete=models.CASCADE)
    tno = models.ForeignKey(Tno, on_delete=models.CASCADE)
    ufns = models.ForeignKey(Ufns, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    wt = models.BooleanField()
    totalb = models.IntegerField()
    acceptedb = models.IntegerField()
    missedb = models.IntegerField()
    droppedb = models.IntegerField()
    callsumb = models.IntegerField()
    personsdayb=models.IntegerField()
    recallb=models.IntegerField()
    totalmorenineb=models.IntegerField()
    from_ekc = models.BooleanField()
    class Meta:
        managed=False
        db_table='callsview'



class CallsViewClocker(models.Model):
    department = models.ForeignKey(Deps, on_delete=models.CASCADE)
    depdirection = models.ForeignKey(DepDirection, on_delete=models.CASCADE)
    tno = models.ForeignKey(Tno, on_delete=models.CASCADE)
    ufns = models.ForeignKey(Ufns, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    call_type=models.ForeignKey(CallType, on_delete=models.CASCADE)
    date_fixation=models.DateField()
    hour=models.IntegerField()
    accepted = models.IntegerField()
    missed = models.IntegerField()
    dropped = models.IntegerField()
    total = models.IntegerField()
    wt = models.BooleanField()
    from_ekc = models.BooleanField()
    class Meta:
        managed=False
        db_table='callsviewclocker'



class CallsViewPerson(models.Model):
    id = models.CharField(primary_key=True)
    call_type=models.ForeignKey(CallType, on_delete=models.CASCADE)
    date_fixation=models.DateField()
    person = models.CharField()
    subscriber_b=models.ForeignKey(Ad,on_delete=models.CASCADE)
    # hour=models.IntegerField()   
    department = models.ForeignKey(Deps, on_delete=models.CASCADE)
    depdirection = models.ForeignKey(DepDirection, on_delete=models.CASCADE)
    tno = models.ForeignKey(Tno, on_delete=models.CASCADE)
    ufns = models.ForeignKey(Ufns, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    wt = models.BooleanField()
    totalb = models.IntegerField()
    acceptedb = models.IntegerField()
    missedb = models.IntegerField()
    droppedb = models.IntegerField()
    callsumb = models.IntegerField()
    personsdayb=models.IntegerField()
    recallb=models.IntegerField()
    totalmorenineb=models.IntegerField()
    from_ekc = models.BooleanField()
    class Meta:
        managed=False
        db_table='callsViewPerson'
