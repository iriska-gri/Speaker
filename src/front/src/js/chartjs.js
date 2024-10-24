function linear_tick_callback(value,index,values,data){
    if (data.modal != true) {
        {                       
          let half = Math.ceil((values.length )/4)                     
         if ([0,half,2*half,values.length - 1].includes(index)) return value.toLocaleString("ru-RU")
                                
        } 
    
      }// Не отображаем остальные метки
      else {
        return value.toLocaleString("ru-RU")
      }
      }
function linear_tick_callback_first_last(value,index,values,data){
if (data.modal != true) {
    {                       
                       
        if ([0,values.length - 1].includes(index)) return   data.labels[index].toLocaleString("ru-RU")          
    } 

    }// Не отображаем остальные метки
    else {
    return data.labels[index].toLocaleString("ru-RU")
    }
    }






export {linear_tick_callback, linear_tick_callback_first_last}
