import moment from 'moment'

moment.locale('ru')

export default {
  print_date: (unixtime, is_short=false) ->
    return moment(unixtime * 1000).format('h:mm, D MMMM')

}
