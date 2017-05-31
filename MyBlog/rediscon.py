import redis
import cPickle
r=redis.Redis(host='127.0.0.1',port=6379)
def testsetbyte():
    list=[1, 2, 3, 4]
    obj=cPickle.dumps(list)
    r.set('list',obj)
    print r.get('list')
    print cPickle.loads(r.get('list'))
    r.flushdb()
if __name__=='__main__':
    testsetbyte()