import moment from 'moment'

moment.locale('ru')

export default {
  print_date: (unixtime, is_short=false) ->
    moment_date = moment(unixtime * 1000)
    date = moment_date.format('D MMMM')
    current_date = moment().format('D MMMM')
    if date == current_date
      return moment_date.format('HH:mm')
    else if is_short
      return date
    else
      return moment_date.format('HH:mm, D MMMM')

}
