# encoding=utf8
# The ca tool entry

"""The ca tool entry
"""

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import logging
import traceback

from argparse import ArgumentParser

from manager import CertificateManager

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', level = logging.INFO)
logger = logging.getLogger('utility')

def getArguments():
    """Get the arguments
    """
    parser = ArgumentParser(description = 'CA utility')
    parser.add_argument('--base', dest = 'basePath', default = '.', help = 'The base working directory')
    subParsers = parser.add_subparsers(dest = 'action')
    # The init parser
    initParser = subParsers.add_parser('init', help = 'Initialize the database')
    # Vertify certificatae
    verifyParser = subParsers.add_parser('verify', help = 'Verify certificate')
    verifyParser.add_argument('--name', dest = 'name', required = True, help = 'The certificate name')
    # Create root certificate parser
    createRootCertParser = subParsers.add_parser('createRootCert', help = 'Create root certificate')
    createRootCertParser.add_argument('--nopass', dest = 'noPass', default = False, action = 'store_true', help = 'Generate root key without a password (Not recommended), false by default.')
    createRootCertParser.add_argument('--keylen', dest = 'keyLength', default = '4096', choices = [ '2048', '4096' ], help = 'The root key length, 4096 by default')
    # Create server certificate parser
    createServerCertParser = subParsers.add_parser('createServerCert', help = 'Create server cert')
    createServerCertParser.add_argument('--name', dest = 'name', required = True, help = 'The certificate name')
    createServerCertParser.add_argument('--usepass', dest = 'usePass', default = False, action = 'store_true', help = 'Generate key with a password, false by default.')
    createServerCertParser.add_argument('--keylen', dest = 'keyLength', default = '2048', choices = [ '2048', '4096' ], help = 'The key length, 2048 by default')
    createServerCertParser.add_argument('--days', dest = 'days', type = int, default = 3650, help = 'The certificate days parameter')
    # Create client certificate parser
    createClientCertParser = subParsers.add_parser('createClientCert', help = 'Create server cert')
    createClientCertParser.add_argument('--name', dest = 'name', required = True, help = 'The certificate name')
    createClientCertParser.add_argument('--usepass', dest = 'usePass', default = False, action = 'store_true', help = 'Generate key with a password, false by default.')
    createClientCertParser.add_argument('--keylen', dest = 'keyLength', default = '2048', choices = [ '2048', '4096' ], help = 'The key length, 2048 by default')
    createClientCertParser.add_argument('--days', dest = 'days', type = int, default = 3650, help = 'The certificate days parameter')
    # Done
    return parser.parse_args()

def main():
    """The main entry
    """
    args = getArguments()
    try:
        if args.action == 'init':
            # Ask for init
            while True:
                print 'Initialize the path [%s] will cause any files or dirs be removed, continue?[y/n]' % args.basePath,
                text = raw_input()
                if text.lower() == 'n':
                    print 'Will not initialize the path, exit'
                    return 1
                elif text.lower() == 'y':
                    # Initialize
                    manager = CertificateManager(args.basePath)
                    manager.init()
                    return 0
                else:
                    print 'Invalid input'
        elif args.action == 'verify':
            # Verify the certificate
            manager = CertificateManager(args.basePath)
            manager.verifyCertificate(args.name)
            return 0
        elif args.action == 'createRootCert':
            # Create the root cert
            manager = CertificateManager(args.basePath)
            manager.createRootCertificate(args.noPass, int(args.keyLength))
            return 0
        elif args.action == 'createServerCert':
            # Create the server cert
            manager = CertificateManager(args.basePath)
            manager.createServerCertificate(args.name, not args.usePass, args.keyLength, args.days)
            return 0
        elif args.action == 'createClientCert':
            # Create the client cert
            manager = CertificateManager(args.basePath)
            manager.createClientCertificate(args.name, not args.usePass, args.keyLength, args.days)
            return 0
        else:
            logger.error('Unknown argument action [%s]', args.action)
            return 1
    except ValueError as error:
        logger.error(error.message)
        return 1
    except KeyboardInterrupt:
        logger.error('User interrupted')
        return 1
    except:
        logger.exception('Unhandled exception occurred')
        return 1

sys.exit(main())

