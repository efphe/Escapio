# Library which provides an escapio
# connectivity library

import xmlrpclib
_escapio_url= 'http://%s:%s@en.beta.eskabio.de/xmlrpc/pna'

def getServer(u, p):
  surl= _escapio_url % (u, p)
  print surl
  s= xmlrpclib.Server(surl)
  return s

class Escapio:
  def __init__(self, user, password, hid, initserver= 1, lang= 'en'):
    self.hotel= hid
    self.user= user
    self.password= password
    self.server= None
    self.lang= lang
    if initserver:
      self.init_server()

  def init_server(self):
    self.server= getServer(self.user, self.password)

  def getRoomTypes(self):
    rtypes= self.server.info.getRoomTypes()
    res= []
    for r in rtypes:
      res.append({'name': r['translations'][self.lang]['name'], 'id': r['id']})
    return res

  def getRooms(self):
    rooms= self.server.pna.getRooms({'hotel_id': self.hotel})
    for r in rooms:
      t= r.pop('translations')
      rname= t[self.lang]['name']
      if not rname:
        for k,v in t.items():
          if v['name']: 
            rname= v['name']
            break
      r['name']= rname
    return rooms

  def setRoom(self, rtype, baseavail, max_adults, max_children, max_babies):
    pass
