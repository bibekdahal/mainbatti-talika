#!/usr/bin/env python3
import urllib.request

DEFAULT_SERVER = "http://localhost/";
DEFAULT_URL = DEFAULT_SERVER + "routine.php"

def main(filename, url=DEFAULT_URL):
    urllib.request.urlretrieve(url, filename)

if __name__=="__main__":
    main("test_update.xml");
