from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connection
import os
import csv
from atc.models import *
from fns.models import *

from loadfile.serializers import *



class Command(BaseCommand):
    help = "--clearall-Очистка всех таблиц \n --cleartb[table_name]-Очистка указанной таблицы\n \
        --loadtype-Загрузка типов вызовов\n --loaddirs-Загрузка направлений деятельности\n \
        --loaddist-Загрузка округов\n --loadufns-Загрузка Уфнс\n"

    def add_arguments(self, parser):
        parser.add_argument("--clearall", action="store_true", help="Очистка всех таблиц")
        parser.add_argument("--cleartb", nargs="+", type=str, help="Очистка указанной таблицы")
        parser.add_argument("--loadtype", action="store_true", help="Загрузка типов вызовов")
        parser.add_argument("--loaddirs", action="store_true", help="Загрузка направлений деятельности")
        parser.add_argument("--loaddist", action="store_true", help="Загрузка округов")
        parser.add_argument("--loadufns", action="store_true", help="Загрузка Уфнс")



    def handle(self, *args, **options):
        if options['clearall']:
            print('Внимание!БД будет полностью очищена!')
            os.system('python manage.py flush')
        if options['cleartb']:
            table_name = options['cleartb'][0]
            print(f'Will be delete table with name in DB {table_name}')
            cursor = connection.cursor()
            cursor.execute(f"TRUNCATE TABLE {table_name} CASCADE")
        if options['loadtype']:
            try:
                with open(f'{settings.BASE_DIR}\media\calltype.csv', encoding="utf8", newline='') as csvfile:
                    csv_reader = csv.reader(csvfile,delimiter=';')
                    for dir_id, name in csv_reader:
                        CallType.objects.update_or_create(
                            id = int(dir_id),
                            name = str(name),
                            defaults = None
                        )
            except Exception as error:
                print(f' Произошла ошибка: {error}')
        if options['loaddirs']:
            try:
                with open(f'{settings.BASE_DIR}\media\depsdirs.csv', encoding="utf8", newline='') as csvfile:
                    csv_reader = csv.reader(csvfile,delimiter=';')
                    for deps_name, depdirection_id in csv_reader:
                        DepDirection.objects.update_or_create(
                            deps_name = deps_name,
                            depdirection_id = depdirection_id,
                            defaults=None
                            )
            except Exception as error:
                print(f' Произошла ошибка: {error}')
        if options['loaddist']:
            try:
                with open(f'{settings.BASE_DIR}\media\district.csv', encoding="utf8", newline='') as csvfile:
                    csv_reader = csv.reader(csvfile,delimiter=';')
                    for distr_id, district_name, district_code in csv_reader:
                        if district_code == '':
                           district_code = str(10)
                        if district_code == '099o':      
                           District.objects.update_or_create(
                                id = district_code[0:3],
                                district_name = district_name,
                                district_code = district_code,
                                defaults=None
                            )
                        else:
                            District.objects.update_or_create(
                                id = district_code,
                                district_name = district_name,
                                district_code = district_code,
                                defaults=None
                            )
            except Exception as error:
                print(f' Произошла ошибка: {error}')
        if options['loadufns']:
            try:
                with open(f'{settings.BASE_DIR}\media\lufns.csv', encoding="utf8", newline='') as csvfile:
                    csv_reader = csv.reader(csvfile,delimiter=';')
                    for ufns_id, ufns_code, ufns_name, ufns_time_difference, district_id in csv_reader:
                        Ufns.objects.update_or_create(
                            id = ufns_code,
                            ufns_code = ufns_code,
                            ufns_name = ufns_name,
                            ufns_time_difference = ufns_time_difference,
                            district_id = district_id,
                            defaults=False
                            )                     
            except Exception as error:
                print(f' Произошла ошибка: {error}')