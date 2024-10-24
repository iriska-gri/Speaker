<template>
    <div  class="row column col no-scroll "
   
    >
        <div  class="text-center col-auto self-center">       
            <div class="text-subtitle1">
                Принято
            </div>
            <div class="text-h3 text-weight-bold ">
                <div class="flex items-center">
                    <div class="cursor-pointer">
                        <NumberAnimate :formatF="'Percent'" :total="aggmain.accepted_p" />%
                        <ArrowUpdown  :previous="aggprevious.accepted_p" :current="aggmain.accepted_p" :iconsize="'lg'"
                            :tooltip="{
                            label: 'Принято',
                            previous: `${aggprevious.accepted_p.toFixed(2)}%`,
                            diff: `${(aggmain.accepted_p - aggprevious.accepted_p).toFixed(2)}%
                            `}"/>
                    </div>
                </div>
                
            </div>
    </div>
    <div class="col q-gutter-sm ">
        <div class="col row">

            <div class="col-6">
                <div class="text-subtitle1">
                    Поступило звонков
                </div>
                <div class="text-h4 text-weight-bold">
                    <div class="flex items-center">
                        <div class="cursor-pointer">
                            <NumberAnimate :total="aggmain.total" />
                            <ArrowUpdown :greengrow="null" :previous="aggprevious.total" :current="aggmain.total" :iconsize="'md'" 
                                :tooltip="{
                                label: 'Поступило звонков',
                                previous: `${aggprevious.total.toLocaleString('ru-RU')}`,
                                diff: `${(aggmain.total - aggprevious.total).toLocaleString('ru-RU')}`
                                }"/>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-6">
                <div class="row fit">
                    
                    <div class="col column">
                        <div class="text-subtitle1 text-weight-medium col">
                            Пропущено
                        </div>
                        <div class="text-weight-bold text-h5">
                            <div class="flex items-center">
                                <div class="cursor-pointer">
                                    <NumberAnimate :formatF="'Percent'" :total="aggmain.missed_p" />%
                                    <ArrowUpdown :previous="aggprevious.missed_p" :current="aggmain.missed_p" :iconsize="'sm'" :greengrow="false" 
                                        :tooltip="{
                                        label: 'Пропущено',
                                        previous: `${aggprevious.missed_p.toFixed(2)}%`,
                                        diff: `${(aggmain.missed_p - aggprevious.missed_p).toFixed(2)}%`
                                        }"/>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col column">
                        <div class="text-subtitle1 text-weight-medium col">
                            Сброшено
                        </div>
                        <div class="text-weight-bold text-h5">
                            <div class="flex items-center">
                                <div class="cursor-pointer">
                                    <NumberAnimate :formatF="'Percent'" :total="aggmain.dropped_p" />%
                                    <ArrowUpdown :previous="aggprevious.dropped_p" :current="aggmain.dropped_p" :iconsize="'sm'" :greengrow="false" 
                                        :tooltip="{
                                        label: 'Сброшено',
                                        previous: `${aggprevious.dropped_p.toFixed(2)}%`,
                                        diff: `${(aggmain.dropped_p - aggprevious.dropped_p).toFixed(2)}%`
                                        }" />
                                </div>
                            </div>
                        </div>
                    </div>
              
                </div>
            </div>
        </div>
        <div class="col row ">
            <div class="col-6">
                <div class="text-subtitle1">
                    Повторных звонков
                </div>
                <div class="text-h4 text-weight-bold">
                    <NumberAnimate :formatF="'Percent'" :total="aggmain.recall" />%
                </div>
            </div>
            <div class="col-6">
                <div class="text-subtitle1">
                    Средняя длительность звонка
                </div>
                <div class="text-h4 text-weight-bold">
                    <div class="flex items-center">
                        <div class="cursor-pointer">
                            <NumberAnimate :formatF="'Date'" :total="aggmain.avg" />
                            <ArrowUpdown :previous="aggprevious.avg" :current="aggmain.avg" :iconsize="'md'" :greengrow="null" 
                                :tooltip="{
                                label: 'Средняя длительность звонка',
                                previous: `${minSecRusFormatter(aggprevious.avg)}`,
                                diff: `${minSecRusFormatter((aggmain.avg - aggprevious.avg))}`
                                }" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col row q-pt-md">
            <div class="col">
                <div class="text-subtitle1">Сотрудников</div>
                <div class="text-h4 text-weight-bold">
                    <div class="flex items-center">
                        <div class="cursor-pointer">
                            <NumberAnimate :total="aggmain.persons" />
                            <ArrowUpdown :greengrow="null" :previous="aggprevious.persons" :current="aggmain.persons" :iconsize="'md'" 
                                :tooltip="{
                                label: 'Сотрудники, которым поступали звонки',
                                previous: `${aggprevious.persons.toLocaleString('ru-RU')}`,
                                diff: `${(aggmain.persons - aggprevious.persons).toLocaleString('ru-RU')}`
                            }"/>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row col">
                <div class="col">
                    <div class="text-subtitle1 text-weight-medium">Звонков на сотрудника</div>
                        <div class="text-h4 text-weight-bold ">
                        <div class="flex items-center"> ~
                            <div class="cursor-pointer">
                                <NumberAnimate :total="aggmain.perperson.total" />
                                <ArrowUpdown :greengrow="false" :previous="aggprevious.perperson.total" :current="aggmain.perperson.total" :iconsize="'md'" 
                                    :tooltip=" {
                                    label: 'Звонков на сотрудника',
                                    previous: `${Math.round(aggprevious.perperson.total).toLocaleString('ru-RU')}`,
                                    diff: `${Math.round(aggmain.perperson.total - aggprevious.perperson.total).toLocaleString('ru-RU')}`
                                    }" />
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col">
                    <div class="row column">
                        <div class="text-subtitle1 text-weight-medium col">
                            Принятых
                        </div>
                        <div class="text-weight-bold text-h5">
                            <div class="flex items-center">~
                                <div class="cursor-pointer">
                                    <NumberAnimate  :total="aggmain.perperson.accepted" />
                                    <ArrowUpdown :previous="aggprevious.perperson.accepted" :current="aggmain.perperson.accepted" :iconsize="'sm'" 
                                        :tooltip="{
                                        label: 'Принятых',
                                        previous: `${Math.round(aggprevious.perperson.accepted).toLocaleString('ru-RU')}`,
                                        diff: `${Math.round(aggmain.perperson.accepted-aggprevious.perperson.accepted).toLocaleString('ru-RU')}`
                                        }" />
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row column">
                        <div class="text-subtitle1 text-weight-medium col">
                            Пропущенных
                        </div>
                        <div class="text-weight-bold text-h5">
                            <div class="flex items-center">~
                                <div class="cursor-pointer">
                                    <NumberAnimate  :total="aggmain.perperson.missed" />
                                    <ArrowUpdown 
                                        :greengrow="false"
                                        :previous="aggprevious.perperson.missed"
                                        :current="aggmain.perperson.missed" :iconsize="'sm'" 
                                        :tooltip="{
                                        label: 'Пропущенных',
                                        previous: `${Math.round(aggprevious.perperson.missed).toLocaleString('ru-RU')}`,
                                        diff: `${Math.round(aggmain.perperson.missed-aggprevious.perperson.missed).toLocaleString('ru-RU')}`
                                        }" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col row ">
            <div class="col-6">
                <div class="text-subtitle1">Текущая загруженность разговорами</div>
                <div class="text-h4 text-weight-bold flex items-center">
                    <div class="cursor-pointer">
                        <NumberAnimate :formatF="'Percent'" :total="aggmain.loading.now" />%
                        <ArrowUpdown :greengrow="false" :previous="aggprevious.loading.now" :current="aggmain.loading.now" :iconsize="'md'" 
                            :tooltip="{
                            label: 'Текущая загруженность разговорами',
                            previous: `${aggprevious.loading.now.toFixed(2)}%`,
                            diff: `${(aggmain.loading.now - aggprevious.loading.now).toFixed(2)}%`
                            }" />
                    </div>
                </div>
                <div> 
                </div>
                <div>
                    <q-icon name='mdi-information-outline cursor-pointer' size="16px" color="deep-orange">
                        <q-tooltip>
                        <span class="col text-caption">Формула расчета показателя:</span>
                            <div class="row text-center text-caption">
                                <div class="col-auto self-center">
                                    Текущая загруженность =
                                </div>
                                <div class="col q-pt-xs">
                                    <div class="col">
                                        Общая продолжительность разговоров
                                    </div>
                                    <q-separator color="orange" inset/>
                                    <div class="col q-pb-xs">
                                        Сотрудники* x продолжительность рабочего дня
                                    </div>
                                </div>
                                <div class="col-auto self-center">
                                    x 100
                                </div>
                            </div>
                            <span>*абоненты, которым хоть раз поступал вызов в течение 1 дня </span>
                        </q-tooltip>
                    </q-icon>
                    рабочего времени заняли телефонные разговоры
                </div>
            </div>
            <div class="col-6">
                <div class="text-subtitle1">Загруженность при обработке всех звонков</div>
                <div class="text-h4 text-weight-bold flex items-center"><q-icon name='mdi-arrow-right'></q-icon>
                    <div class="cursor-pointer">
                        <NumberAnimate :formatF="'Percent'" :total="aggmain.loading.future" />%
                        <ArrowUpdown :greengrow="false" :previous="aggprevious.loading.future" :current="aggmain.loading.future" :iconsize="'md'" 
                            :tooltip="{
                            label: 'Загруженность при обработке всех звонков',
                            previous: `${aggprevious.loading.future.toFixed(2)}%`,
                            diff: `${(aggmain.loading.future - aggprevious.loading.future).toFixed(2)}%`
                            }"/>
                    </div>
                </div>
                <div> 
                    <q-icon name='mdi-information-outline cursor-pointer' size="16px" color="deep-orange">
                        <q-tooltip>
                        <span class="col text-caption">Формула расчета показателя:</span>
                            <div class="row text-center text-caption">
                                <div class="col-auto self-center">
                                    Загруженность при обработке всех звонков =
                                </div>
                                <div class="col q-pt-xs">
                                    <div class="col">
                                        Средняя длительность разговора х Всего вызовов
                                    </div>
                                    <q-separator color="orange" inset/>
                                    <div class="col q-pb-xs">
                                        Сотрудники* x Продолжительность рабочего дня
                                    </div>
                                </div>
                                <div class="col-auto self-center">
                                    x 100
                                </div>
                            </div>
                            <span>*абоненты, которым хоть раз поступал вызов в течение 1 дня </span>
                        </q-tooltip>
                    </q-icon> 
                    рабочего времени займут телефонные разговоры, если
                    принять все звонки
                </div>
            </div>

        </div>
    </div>
    </div>
</template>
  
<script>
import moment from "moment";
import ArrowUpdown from '../UI/ArrowUpdown.vue'
import { computed } from "vue";
import { minSecRusFormatter } from '../../js/formatters.js'
import NumberAnimate from "../UI/NumberAnimate.vue";

export default {
    components: {
        NumberAnimate,
        ArrowUpdown
    },
    props: {
        maindata: {
            type: Object,
            default: () => {
                return { total: 0, accepted: 0, missed: 0, avg: 0, persons: 0 };
            },

        },
        recall: {
            type: Object,
            default: () => {
                return { total: 0, accepted: 0, missed: 0, avg: 0 };
            },

        },
        previoustopavg: {
            type: Array,
            default: () => []
        }
    },
    setup(props, { emit }) {
        const worktime = 60 * 60 * 8
 
        moment.locale("ru");

        const momenter = (val) => {
            return moment.unix(val, 2).utc().format("m мин ss сек")
        }

        const aggregator = (data) => {
     
            let tabdata = { total: 0, accepted: 0, missed: 0, persons: 0, avg: 0, dropped: 0, callsum: 0, personsday:0 }
            for (let x of data) {
                
                tabdata.total += x.total;
                tabdata.avg += x.avg===null?0:parseFloat(x.avg) * (x.accepted);
                tabdata.missed += x.missed;
                tabdata.accepted += x.accepted;
                tabdata.persons += x.persons
                tabdata.dropped += x.dropped
                tabdata.callsum += x.callsum
                tabdata.personsday+=x.personsday
            }
          
            return datacalcer(tabdata)

        }



        const aggmain = computed({
            get() {

                return aggregator(props.maindata)
            }
        })
        const aggprevious = computed({
            get() {

                return aggregator(props.previoustopavg)
            }
        })

        const recallcount = computed({
            get() {
                let recall = { count: 0, total: 0 }
                props.recall.forEach((e) => {
                    recall.count += e.recall
                    recall.total += e.total
                })
                return 100 * recall.count / recall.total
            }
        })



        const datacalcer = (data) => {
       
            return {
                total: data.total,
                avg: data.avg / data.accepted,
                accepted: data.accepted,
                dropped: data.dropped,
                missed: data.missed,
                accepted_p: data.accepted * 100 / data.total,
                missed_p: data.missed * 100 / data.total,
                dropped_p: data.dropped * 100 / data.total,
                persons: data.persons,
                perperson: {
                    total: data.total / data.persons,
                    accepted: data.accepted / data.persons,
                    missed: data.missed / data.persons
                },
                loading: {
                    now: data.callsum / (data.personsday * worktime) * 100,
                    future: (data.avg / data.accepted) * data.total / (data.personsday * worktime) * 100
                },
                recall: recallcount.value
            }
        }


        return {aggmain, aggprevious, minSecRusFormatter };
    },
};
</script>
  
<style></style>
  