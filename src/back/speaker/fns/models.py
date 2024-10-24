from django.db import models


class District(models.Model):
    district_name = models.CharField(
        max_length=255, blank=False, verbose_name='Название округа')
    district_code = models.CharField(
        max_length=4, null=True, verbose_name='Код округа')

    class Meta:
        verbose_name = "Справочник Округов"
        verbose_name_plural = "Справочник Округов"
        unique_together = [["district_name", "district_code"]]

    def __str__(self):
        return str(self.district_name)


class Ufns(models.Model):
    ufns_code = models.CharField(
        max_length=4, blank=False, verbose_name='Код УФНС')
    ufns_name = models.CharField(
        max_length=255, blank=False, verbose_name='Назвние УФНС')
    ufns_time_difference = models.IntegerField(
        default=0, blank=False, verbose_name='Разница во времени(мск)')
    district = models.ForeignKey(District, related_name="district_ufns", null=True, blank=True, on_delete=models.CASCADE)
    # tz=models.CharField(verbose_name='Имя часового пояся',default='Europe/Moscow')
    class Meta:
        verbose_name = "Справочник УФНС"
        verbose_name_plural = "Справочник УФНС"

    def __str__(self):
        return str(self.ufns_name)


class Tno(models.Model):
    tno_name = models.CharField(
        max_length=255, blank=False, verbose_name='Назвние ТНО')
    tno_code = models.CharField(
        max_length=4, blank=False, verbose_name='Код ТНО')
    ufns = models.ForeignKey(
        Ufns, on_delete=models.CASCADE, blank=False, verbose_name='УФНС')

    class Meta:
        verbose_name = "Справочник ТНО"
        verbose_name_plural = "Справочник ТНО"

    def __str__(self):
        return str(self.tno_name)
        
class DepDirection(models.Model):
    name=models.CharField(max_length=255, blank=False, verbose_name='Название Направления')

    class Meta:
        verbose_name = "Направления деятельности"
        verbose_name_plural = "Направления деятельности"

    def __str__(self):
        return str(self.name)

class Deps(models.Model):
    deps_name = models.CharField(
        max_length=255, blank=False, verbose_name='Название отдела/управления')
    tno = models.ForeignKey(Tno, on_delete=models.CASCADE,
                            blank=False, verbose_name='УФНС')
    depdirection = models.ForeignKey(DepDirection, blank=True,null=True,on_delete=models.CASCADE, verbose_name="Направление")
    class Meta:
        verbose_name = "Справочник отделов"
        verbose_name_plural = "Справочник отделов"
        unique_together = ["deps_name", "tno"]

    def __str__(self):
        return str(self.deps_name)

class Position(models.Model):
    name=models.CharField(
        max_length=255, blank=False, verbose_name='Должность', unique=True)

class Ad(models.Model):
    account_name = models.CharField(max_length=255, unique=True, blank=False)
    sn = models.CharField(max_length=255, blank=True,
                          verbose_name='Фамилия сотрудника')
    given_name = models.CharField(
        max_length=255, blank=True, verbose_name='Имя, Отчество сотрудника')

    telephone_number = models.CharField(
        max_length=255, blank=True, verbose_name='Телефонный номер')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True)
    disabled = models.BooleanField(
        blank=False,default=False, verbose_name='Сотрудник Уволен/Работает')

    department = models.ForeignKey(Deps, on_delete=models.CASCADE,
                                   blank=False, verbose_name='Отдел/Управление')
    pwd_lastset = models.DateTimeField(verbose_name='Дата смены пароля', null=True, blank=True)
    last_logon = models.DateTimeField(verbose_name='Дата входа сотрудника', null=True, blank=True)

    class Meta:
        verbose_name = "Сотрудники"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return str(f'{self.sn} {self.given_name}')
    
    def fullname(self):
        return 
    # def clear_phone(self):
    #     return 


class HolidayExculisions(models.Model):
    holiday_date = models.DateField(null=True, blank=True, verbose_name='дата дня-исключения')

    class Meta:
        verbose_name = "День-исключение"
        verbose_name_plural = "Даты дней-исключений"

    def __str__(self):
        return self.holiday_date.strftime("%d.%m.%Y")