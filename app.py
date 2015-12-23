import time

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    return [bytes(t)]
