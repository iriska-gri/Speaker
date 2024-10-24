import moment from "moment";

function minSecRusFormatter(value){
    return moment.unix(value, 2).utc().format("m мин ss сек")
}
function format_date_to_base(val){
    let d = val.split(".")
    d = d.reverse()
    return d.join("-")
}
export {minSecRusFormatter,format_date_to_base}