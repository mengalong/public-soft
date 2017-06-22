import eventlet

from datetime import datetime


def do_something(param):
    time_now = datetime.now()
    print "%s-%s" % (time_now, param)
    eventlet.sleep(1)
    return [param]


if __name__ == "__main__":
    pool = eventlet.GreenPool(10)
    instances = [i for i in xrange(1, 100)]
    result_batch = []
    for result in pool.imap(do_something, instances):
        result_batch.extend(result)

