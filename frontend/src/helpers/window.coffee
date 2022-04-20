import axios from 'axios'
import {io} from "socket.io-client"

NAMESPACE = '/socket'

state = {
  socket: undefined
}

#
# socket.on('message', (msg) ->
#   console.log('Received message', msg);
# )

export default {
  send_query: (data) ->
    result = await axios.post('/api', data)
    return result.data

  connect: () ->
    if state.socket?
      return true
    else
      socket = io.connect(NAMESPACE)
      return new Promise((resolve) ->
        socket.on('connect', () ->
          state.socket = socket
          resolve(true)
        )
        socket.on('connect_error', () ->
          resolve(false)
        )
      )
  get_chats: () ->
    if state.socket?
      promise = new Promise((resolve, reject ) ->
        state.socket.emit('get_chats', (answer) ->
          resolve(answer)
        )
      )
      return promise
    return

  add_linstener: (event, handler) ->
    if state.socket?
      state.socket.on(event, handler)
    return

  remove_linstener: (event, handler) ->
    if state.socket?
      state.socket.off(event, handler)
    return
}
