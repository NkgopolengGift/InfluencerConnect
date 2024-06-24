let loc = window.location
let wsStart = 'ws://'

if(loc.protocol === 'https'){
    wsStart = 'wss://'
}
let endpoint = wsStart + loc.host + loc.pathname

var socket = new WebSocket(endpoint)

socket.onopen = async function(e){
    console.log('open', e)
}

socket.onmessage = async function(e){
    console.log('message', e)
}

socket.onerror = async function(e){
    console.log('error', e)
}

socket.onclose = async function(e){
    console.log('close', e)
}

let input_message = $('.input_message')
let message_body = $('.msg_card_body')

function newMessage(message){
    if($.trim(message)===''){
        return false;
    }
}