import time

def logging(type, message):
    m=('['+type+'] ' + message + " on the [" + time.ctime().split()[3] + ']')
    print(m)
    log = open('LOG.txt', "a")
    log.write(m + "\n")
    log.close()