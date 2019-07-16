from .base import tgfAPI
from .wapp_bot import WhatsAppBot

class WhatsAppAPI(tgfAPI):
    def __init__(self,token,**args):
        super().__init__(token)
        self.bot = WhatsAppBot(token,args.get('endpoint'))

    def start(self,**args):
        while True:
            self.bot.start_polling(**args)

    def send(self,id_,**args):
        self.bot.send_message(
            chat_id=id_,
            text=args['text'],
            reply_markup =args['markup']
        )

    def update(self,msg,**args):
        # here msg is the type set_message_handler pass
        text =args.get('text')
        markup=args.get('markup')
        self.bot.send_message(
            msg.chat.id,
            text=text,
            reply_markup =markup
        )

    def set_message_handler(self,clb):
        self.bot.set_message_handler(clb)

    def set_callback_handler(self,clb):
        self.bot.set_callback_handler(clb)

    def KeyboardButton(self,**args):
        return (args.get('text'),
                args.get('callback_data')
               )
    def KeyboardMarkup(self,buttons=None,**args):
        return buttons

