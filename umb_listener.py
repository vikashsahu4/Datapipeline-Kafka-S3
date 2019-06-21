import optparse
import thread
import Queue
from proton import Url, SSLDomain
from proton.reactor import Container, Selector
from proton.handlers import MessagingHandler


DEFAULT_CERT = #Location of the certificates
DEFAULT_KEY = #Location of the key
DEFAULT_SELECTOR = None
#DEFAULT_SELECTOR = ['"status" = "success"', '"artifact_type" = "log"']


BUSES = { 
    'dev': [],  
    'qa': [],  
    'prod': []   
}



class UmbListener(MessagingHandler):

    def __init__(self, bus_type='dev', cert=DEFAULT_CERT, key=DEFAULT_KEY, queue=Queue.Queue()):
        super(UmbListener, self).__init__()
        self.urls = BUSES[bus_type]
        self.cert = cert
        self.key = key 
        self.queue = queue

    def on_start(self, event):
        domain = SSLDomain(SSLDomain.MODE_CLIENT)
        domain.set_credentials(self.cert, self.key, None)
        conn = event.container.connect(urls=self.urls, ssl_domain=domain)
        selector = [Selector(DEFAULT_SELECTOR[0]), Selector(DEFAULT_SELECTOR[1])] if DEFAULT_SELECTOR is not None else None
        event.container.create_receiver(conn, source=#Enter the topic name, options=selector)
        print("Subscribed...")

    def on_message(self, event):
        print("ADDRESS: {0}".format(event.message.address))
        print("BODY: {0}".format(event.message.body))
        #print(type(event.message.body))
        print("")
        self.queue.put(event.message.body)
    


def main():
    parser = optparse.OptionParser()
    parser.add_option('-b', '--bus', type='choice', choices=BUSES.keys(), default='dev')
    opts, args = parser.parse_args()
    try:
         queue = Queue.Queue()
         Container(UmbListener(bus_type=opts.bus, queue=queue)).run()
    except KeyboardInterrupt:
         pass

if __name__ == '__main__':
    main()
