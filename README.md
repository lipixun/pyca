# pyca

A python implemented certificate authority lib &amp; tools based on openssl

## Features

* Verify certificate
* Generate root CA
* Sign server certificate
* Sign client certificate

## Future features

* Maintain certificate chain
* Generate CRL (Certificate revocation lists)
* Generate OCSP (Online Certificate Status Protocol)

## Simple usage

Before generating / signing anything, you have to init the key / certificate database.

This is done by running command `python -m calib --base [The database path] init`

Please take care that any files or dirs will be removed in the database path. If the `--base` argument is not given, the current working directory will be used.

After initialized the database, you have to generate a root certificate by command `python -m calib --base [The database path] createRootCert`

Please use `python -m calib --help` for more usage info.

