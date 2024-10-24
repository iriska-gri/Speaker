<template>
 
<q-icon 
  class="q-px-xs cursor-pointer "
  :name="`mdi-arrow-${previous>current?'down':'up'}-bold-circle-outline`"
  :color="colorer()"
  :size="iconsize">
</q-icon>

<q-tooltip anchor="bottom middle" self="top middle">         
  <div>{{tooltip.label}}</div>              
  <div>В прошлом периоде: {{ tooltip.previous }}</div>
  <div>Изменение: {{ tooltip.diff }} </div>
</q-tooltip>



</template>
<script>
import { defineComponent } from 'vue'
export default defineComponent({
    name:'ArrowUpdown',
    props:{
        previous:{
            type:Number,
            default:0
        },
        current:{
            type:Number,
            default:0
        },
        tooltip:{
            type: Object,
            default:()=>{return {label:'', previous:0,diff:0}}
        },
        greengrow:{
            type:Boolean,
            default:true
        },
        iconsize:{
            type: String,
            default:'xs'
        }
    },
  components: {
   

  },
  setup(props) {

    const colorer = ()=>{
        if (props.greengrow===null){
            return "blue"
        }
      let grow = props.current>props.previous
      
      if (props.greengrow==false){

        return grow?'red':'green'
      }
      else if(props.greengrow==true){
       
        return grow?'green':'red'
      }
      return 'red'

    }

return {colorer

}
  }
})
</script>