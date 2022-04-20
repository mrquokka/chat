import moment from 'moment'

moment.locale('ru')

export default {
  print_date: (unixtime, is_short=false) ->
    moment_date = moment(unixtime * 1000)
    if is_short
      date = moment_date.format('D MMMM')
      current_date = moment().format('D MMMM')
      if date == current_date
        return moment_date.format('h:mm')
      else
        return date
    return moment_date.format('h:mm, D MMMM')

}
