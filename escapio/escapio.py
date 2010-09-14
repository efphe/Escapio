# Library which provides escapio connectivity

import xmlrpclib
_escapio_url= 'http://%s:%s@en.beta.eskabio.de/xmlrpc/pna'

ESCAPIO_BOARDS= {
 'nf': 'NO_BOARD',
 'bb': 'BREAKFAST',
 'hb': 'HALF_BOARD',
 'fb': 'FULL_BOARD',
 'ai': 'ALL_INCLUSIVE ',
}

def getServer(u, p):
  surl= _escapio_url % (u, p)
  return xmlrpclib.Server(surl)

class Escapio:
  def __init__(self, user, password, hid, initserver= 1, lang= 'en'):
    self.hotel= hid
    self.user= user
    self.password= password
    self.server= None
    self.lang= lang
    if initserver:
      self.init_server()

  def extractTranslation(self, d):
    t= d.pop('translations')
    n= t.get(self.lang)
    if isinstance(n, dict):
      n= n['name']
    if n:
      d['name']= n
      return
    for k,v in t.items():
      if v['name']:
        d['name']= v['name']
        return d

  def init_server(self):
    self.server= getServer(self.user, self.password)

  def getRoomTypes(self):
    rtypes= self.server.info.getRoomTypes()
    for r in rtypes:
      self.extractTranslation(r)
    return rtypes

  def getRooms(self):
    rooms= self.server.pna.getRooms({'hotel_id': self.hotel})
    for r in rooms:
      self.extractTranslation(r)
    return rooms

  def getRates(self, newrate= None):
    rates= self.server.pna.getRates({'hotel_id': self.hotel})
    if not rates and newrate:
      d= {
          'hotel_id': self.hotel_id,
          'translations': {self.lang: newrate},
          }
      rates= [self.server.pna.setRate(d)]
    for r in rates:
      self.extractTranslation(r)
    return rates

  def setRoom(self, rtype, baseavail, max_adults, max_children, max_babies):
    pass

  def setAllocation(self, d, board= 'nf'):
    """ d is a dictionary like this:
      {
        'date_start': '%Y-%m-%d, 
        'date_end': '%Y-%m-%d,
        'rate_id':
        'room_id': 
        'contingents': 
        'contingents_booked':
        'price':
      }
    """
    newd= {'board': board, 'hotel_id': self.hotel, 'type': 'allocation'}
    d.update(newd)
    print d
    return self.server.pna.setAllocationsByPeriod(d)
