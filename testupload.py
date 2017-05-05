#!/usr/bin/python

from datetime import datetime
from datetime import timedelta
import subprocess
import time
import logging

from wrappers import GPhoto
from wrappers import Identify
from wrappers import Curl

#sudo /usr/local/bin/gphoto2 --capture-image-and-download --filename 'test3.jpg'
#curl --form "fileupload=@test7.jpg" http://192.168.178.197:5000/

MIN_INTER_SHOT_DELAY_SECONDS = timedelta(seconds=30)
UPLOAD_URL = "http://upload-test:5000/"
LOG_NAME = "timelapse.log"

def main():
    print "Timelapse upload test"
    camera = GPhoto(subprocess)
    idy = Identify(subprocess)
    curl = Curl(subprocess)
    
    logging.basicConfig(filename=LOG_NAME,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    logging.info("Starting timelapse")
    logger = logging.getLogger('timelapse')    

    # myLogger.debug(msg)
    # myLogger.info(msg)
    # myLogger.warn(msg)
    # myLogger.error(msg)
    # myLogger.critical(msg)

    current_config = 25 #11
    shot = 0
    prev_acquired = None
    last_acquired = None
    last_started = None

    try:
        while True:
            last_started = datetime.now()
            last_acquired = datetime.now()
            filename = "20170421-024718.jpg"

            curl.fileupload(filename, UPLOAD_URL)

            if last_started and last_acquired and last_acquired - last_started < MIN_INTER_SHOT_DELAY_SECONDS:
                print "Sleeping for %s" % str(MIN_INTER_SHOT_DELAY_SECONDS - (last_acquired - last_started))

                time.sleep((MIN_INTER_SHOT_DELAY_SECONDS - (last_acquired - last_started)).seconds)

            print "Forced sleep"
            time.sleep(MIN_INTER_SHOT_DELAY_SECONDS.seconds)
                
            shot = shot + 1
    except Exception,e:
        print str(e)
        logger.error(e)
        logging.shutdown()


if __name__ == "__main__":
    main()
