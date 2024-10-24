<template>
    <NumberAnimation 
        :from="1" 
        :to="total" 
        :format="(val) => formatter(val)" 
        :duration=".5" 
        :delay="10" autoplay
        easing="linear">
    </NumberAnimation>
</template>

<script setup>
import moment from "moment";
import NumberAnimation from "vue-number-animation";
import {minSecRusFormatter} from '../../js/formatters.js'
moment.locale("ru");

const props = defineProps({
    total: [String, Number],
    formatF: {
        type: String,
        default: 'Integer',
    },
})

function formatter(value) {
    if (props.formatF == 'Percent') {
        return Number(value).toFixed(2)
    } else if (props.formatF == 'Date') {
        return minSecRusFormatter(value);
    }
    return Number(value.toFixed(0)).toLocaleString('ru-RU')
}

</script>