import string
from dataclasses import dataclass

import sys
sys.path.insert(1, 'C:\saiscripts\intercept_branch\Payment Web App Project')

# Now do your import
import private_constants

secret_key = private_constants.secret_key
host=private_constants.host
user=private_constants.user
passwd=private_constants.passwd

@dataclass
class c():
    scrt_key: string
    hst: string
    usr: string
    psswd: string

s = c(secret_key, host, user, passwd)

