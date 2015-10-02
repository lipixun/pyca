# encoding=utf8
# The certificate manager

"""The certificate manager
"""

import logging

import os
import os.path
import shutil
import subprocess

import jinja2

class CertificateManager(object):
    """The certificate manager
    """
    DIR_CERTS = 'certs'
    DIR_CRL = 'crl'
    DIR_CSR = 'csr'
    DIR_NEWCERTS = 'newcerts'
    DIR_PRIVATE = 'private'

    DIRS = [ DIR_CERTS, DIR_CRL, DIR_CSR, DIR_NEWCERTS, DIR_PRIVATE ]

    FILE_INDEX = 'index.txt'
    FILE_SERIAL = 'serial'
    FILE_CONFIG = 'openssl.config'

    FILE_CA_CERT = 'ca.cert.pem'
    FILE_CA_KEY = 'ca.key.pem'

    def __init__(self, basePath = None, logger = None):
        """Create a new CertificateManager
        """
        self.basePath = os.path.expanduser(os.path.abspath(basePath)) or os.getcwd()
        self.logger = logger or logging.getLogger('certmgr')
        # Check base path
        if not os.path.isdir(self.basePath):
            raise ValueError('Base path [%s] not found' % self.basePath)

    def init(self):
        """Init the manager
        NOTE:
            This method will remove all files and directories in the base path
        Returns:
            Nothing
        """
        self.logger.info('Start initialize dir [%s]', self.basePath)
        # Clean the directory
        for name in os.listdir(self.basePath):
            path = os.path.join(self.basePath, name)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.unlink(path)
        # Prepare dirs and files
        self.logger.info('Prepare dirs and files')
        for name in self.DIRS:
            os.mkdir(os.path.join(self.basePath, name))
        with open(os.path.join(self.basePath, self.FILE_INDEX), 'wb') as fd:
            pass
        with open(os.path.join(self.basePath, self.FILE_SERIAL), 'wb') as fd:
            print >>fd, 1000
        # Format the config file
        env = jinja2.Environment(
                loader = jinja2.FileSystemLoader(os.path.dirname(os.path.abspath(__file__))),
                trim_blocks = True,
                lstrip_blocks = True
                )
        template = env.get_template('openssl.config.template')
        content = template.render(basePath = self.basePath)
        with open(os.path.join(self.basePath, self.FILE_CONFIG), 'wb') as fd:
            print >>fd, content
        # Done

    def verifyCertificate(self, name):
        """Verify a certificate
        """
        certPath = os.path.join(self.basePath, self.DIR_CERTS, '%s.cert.pem' % name)
        if not os.path.isfile(certPath):
            raise ValueError('Certificate [%s] not found' % certPath)
        if subprocess.call([ 'openssl', 'x509', '-noout', '-text', '-in', certPath ]) != 0:
            raise ValueError('Failed to verify the certificate')

    def createRootCertificate(self, noPass = False, keyLength = 4096):
        """Create a root certificate
        """
        configPath, keyPath, certPath = \
                os.path.join(self.basePath, self.FILE_CONFIG), \
                os.path.join(self.basePath, self.DIR_PRIVATE, self.FILE_CA_KEY), \
                os.path.join(self.basePath, self.DIR_CERTS, self.FILE_CA_CERT)
        if os.path.isfile(keyPath):
            raise ValueError('CA key file exists at [%s]' % keyPath)
        if os.path.isfile(certPath):
            raise ValueError('CA certificate file exists at [%s]' % certPath)
        # Generate the key
        if subprocess.call([ 'openssl', 'genrsa', '-aes256', '-out', keyPath, str(keyLength) ] if not noPass else [ 'openssl', 'genrsa', '-out', keyPath, str(keyLength) ]) != 0:
            raise ValueError('Failed to create root key')
        # Generate the cert
        if subprocess.call([ 'openssl', 'req', '-config', configPath, '-key', keyPath, '-new', '-x509', '-days', '7300', '-sha256', '-extensions', 'v3_ca', '-out', certPath ]) != 0:
            raise ValueError('Failed to create root certifcate')
        # Done

    def createServerCertificate(self, name, noPass = True, keyLength = 2048, days = 375):
        """Create a server certificate
        """
        if not name:
            raise ValueError('Require name')
        configPath, keyPath, csrPath, certPath = \
                os.path.join(self.basePath, self.FILE_CONFIG), \
                os.path.join(self.basePath, self.DIR_PRIVATE, '%s.key.pem' % name), \
                os.path.join(self.basePath, self.DIR_CSR, '%s.csr.pem' % name), \
                os.path.join(self.basePath, self.DIR_CERTS, '%s.cert.pem' % name)
        if os.path.isfile(keyPath):
            raise ValueError('Key file exists at [%s]' % keyPath)
        if os.path.isfile(csrPath):
            raise ValueError('CSR file exists at [%s]' % csrPath)
        if os.path.isfile(certPath):
            raise ValueError('Certificate file exists at [%s]' % certPath)
        # Generate the key
        if subprocess.call([ 'openssl', 'genrsa', '-aes256', '-out', keyPath, str(keyLength) ] if not noPass else [ 'openssl', 'genrsa', '-out', keyPath, str(keyLength) ]) != 0:
            raise ValueError('Failed to create key')
        # Generate the csr
        if subprocess.call([ 'openssl', 'req', '-config', configPath, '-key', keyPath, '-new', '-sha256', '-out', csrPath ]) != 0:
            raise ValueError('Failed to create CSR')
        # Generate the certificate
        if subprocess.call([ 'openssl', 'ca', '-config', configPath, '-extensions', 'server_cert', '-days', str(days), '-notext', '-md', 'sha256', '-in', csrPath, '-out', certPath ]) != 0:
            raise ValueError('Failed to create certificate')
        # Done

    def createClientCertificate(self, name, noPass = True, keyLength = 2048, days = 375):
        """Create a client certificate
        """
        if not name:
            raise ValueError('Require name')
        configPath, keyPath, csrPath, certPath = \
                os.path.join(self.basePath, self.FILE_CONFIG), \
                os.path.join(self.basePath, self.DIR_PRIVATE, '%s.key.pem' % name), \
                os.path.join(self.basePath, self.DIR_CSR, '%s.csr.pem' % name), \
                os.path.join(self.basePath, self.DIR_CERTS, '%s.cert.pem' % name)
        if os.path.isfile(keyPath):
            raise ValueError('Key file exists at [%s]' % keyPath)
        if os.path.isfile(csrPath):
            raise ValueError('CSR file exists at [%s]' % csrPath)
        if os.path.isfile(certPath):
            raise ValueError('Certificate file exists at [%s]' % certPath)
        # Generate the key
        if subprocess.call([ 'openssl', 'genrsa', '-aes256', '-out', keyPath, str(keyLength) ] if not noPass else [ 'openssl', 'genrsa', '-out', keyPath, str(keyLength) ]) != 0:
            raise ValueError('Failed to create key')
        # Generate the csr
        if subprocess.call([ 'openssl', 'req', '-config', configPath, '-key', keyPath, '-new', '-sha256', '-out', csrPath ]) != 0:
            raise ValueError('Failed to create CSR')
        # Generate the certificate
        if subprocess.call([ 'openssl', 'ca', '-config', configPath, '-extensions', 'usr_cert', '-days', str(days), '-notext', '-md', 'sha256', '-in', csrPath, '-out', certPath ]) != 0:
            raise ValueError('Failed to create certificate')
        # Done

