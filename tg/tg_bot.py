import telepot
import sys
import random
import datetime
bot = 0

# send pic
def handle1(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot.sendMessage(chat_id, 'Hello')
    try:
        bot.sendPhoto(chat_id, open(r'D:\hype_tweety_bg2.png', 'rb'))
    except Exception as ex:
        print(ex)

    print('sent')

#send /roll or /time
def handle2(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)

    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,6))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))

#send emoji code
def handle3(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    #m = telepot.namedtuple.Message(**msg)

    if chat_id < 0:
        # group message
        print('Received a %s from %s, by %s' % (content_type, msg['chat']['id'], msg['from']['id']))
    else:
        # private message
        print('Received a %s from %s' % (content_type, msg['chat']['id']))  # m.chat == m.from_

    if content_type == 'text':
        reply = ''

        # For long messages, only return the first 10 characters.
        if len(msg['text']) > 10:
            reply = u'First 10 characters:\n'

        # Length-checking and substring-extraction may work differently
        # depending on Python versions and platforms. See above.

        reply += msg['text'][:10].encode('unicode-escape').decode('ascii')
        bot.sendMessage(chat_id, reply)

def handle(msg):
    flavor = telepot.flavor(msg)

    summary = telepot.glance(msg, flavor=flavor)
    print(flavor, summary)

def main(token):
    global bot
    bot = telepot.Bot(token)
    bot.message_loop(handle, run_forever=True)

TOKEN = '779485434:AAExvneL3PdlbWCXDhgY-MiKLlJUI8gqST0'

main(TOKEN)
