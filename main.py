__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

                   All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
import os, sys

import ujson

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.enum.Enum import Enum

__json__ = os.path.abspath('./files-json.txt')

class Methods(Enum):
    recusive = 1
    nonrecusive = 2
    testing = 4

def main_proc(__command__,method=Methods.recusive):
    __has_json__ = os.path.exists(__json__)
    if (__has_json__):
        files = ujson.loads(_utils.readFileFrom(__json__,mode='r',noCRs=True))
    else:
        from vyperlogix import paramiko
    
        from vyperlogix.crypto import Encryptors
        pwd = Encryptors._decode('D0E5E5EBC0E2B0B0')
    
        host = 'your-host-goes-here'
        port = 22
        user = 'your-username-goes-here'
    
        print 'username=%s, password=%s' % (user,pwd)
    
        sftp = paramiko.ParamikoSFTP(host,int(port),user,password=pwd,use_manual_auth=True,callback=None,auto_close=False,logPath=None)
    
        __remote__ = __command__
        __Local__ = os.path.abspath('./downloads')
    
        __sftp__ = sftp.getSFTPClient
    
        __remotes__ = []
    
        def __sftp_isdir__(directory):
            try:
                result = __sftp__.isdir(directory)
            except:
                result = False
            return result
    
        def sftp_listfiles_from(directory):
            for name in __sftp__.listdir(directory):
                full_path = '/'.join([directory, name])
                if __sftp_isdir__(full_path):
                    for entry in sftp_listfiles_from(full_path):
                        yield entry
                else:
                    yield full_path

        files = [f for f in sftp_listfiles_from(__remote__)]
        sftp.close()

    def store_in_bucket_recursive(bucket={},fp=None):

        def packit(fp):
            toks = [t for t in fp.split('/') if t]
            ret = fp
            for tok in reversed(toks):
                ret = {tok: ret}
            return ret
        
        def merge(d1, d2):
            for k1,v1 in d1.iteritems():
                if not k1 in d2:
                    d2[k1] = v1
                elif isinstance(v1, dict):
                    merge(v1, d2[k1])
            return d2

        if (not fp):
            paths = ['1/2/3','1/2/4','1/2/5']
        else:
            paths = [fp] if (not misc.isList(fp)) else fp
        dicts = [packit(p) for p in paths]
        merged = bucket if (misc.isDict(bucket)) else {}
        for d in dicts:
            merged = merge(merged,d)
        return merged

    def store_in_bucket(__namespace__,keyname,path):
        toks = [t for t in path.split('/') if (len(t) > 0)]

        lines = []
        ops = ['[toks[%s]]' % (i) for i in xrange(0,len(toks))]
        __first_time__ = (not __namespace__.has_key(keyname))
        n = (len(toks)+(1 if (__first_time__) else 0))
        for i in xrange(0,len(toks)+1):
            s = '%s%s' % (keyname,''.join(ops[0:i]))
            t = '%s%s' % (keyname,''.join(ops[0:i-1]))
            if (i == 0):
                lines.append('%s = %s' % (s,'{}'))
            else:
                if (i == (n-1)) and (__first_time__):
                    x = '"%s"'%('/'+('/'.join(toks)))
                else:
                    if (i < n):
                        x = '{} if (not %s.has_key("%s")) else %s' % (t,toks[i-1],s)
                    else:
                        x = '"%s"'%('/'+('/'.join(toks)))
                lines.append('%s = %s' % (s,x))
        if (not __first_time__):
            del lines[0]
        __namespace__['toks'] = toks
        exec('\n'.join(lines)) in __namespace__
        del __namespace__['toks']
        return __namespace__

    __method__ = None
    if (method == Methods.recusive):
        __method__ = store_in_bucket_recursive
    elif (method == Methods.nonrecusive):
        __method__ = store_in_bucket
    elif (method != Methods.testing):
        print >> sys.stderr, 'WARNING: Invalid method used for method parameter.'
        sys.exit(1)
    
    bucket = {}
    if (__method__ == store_in_bucket):
        for f in files:
            bucket = __method__(bucket,'directory',f)
            if (bucket.has_key('__builtins__')):
                del bucket['__builtins__']
    elif (__method__ == store_in_bucket_recursive):
        bucket = __method__(bucket=bucket,fp=files)
    else:
        print >> sys.stderr, 'ERROR: Unknown method.'

    if (method == Methods.testing):
        if (not __has_json__):
            fOut = open(__json__,'w')
            print >> fOut, ujson.dumps(files)
            fOut.flush()
            fOut.close()
    else:
        print ujson.dumps(bucket)
    return files


if (__name__ == '__main__'):
    '''
    python -m cProfile main.py
    '''
    __command_long__ = '/'

    #main_proc(__command_long__,method=Methods.recusive)
    
    main_proc(__command_long__,method=Methods.nonrecusive)

    #main_proc(__command_long__,method=Methods.testing)
    
