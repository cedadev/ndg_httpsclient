#!/bin/bash
openssl genrsa -out localhost.key 4096
openssl req -new -out localhost.csr -subj '/O=NDG/OU=Security/CN=localhost' -key localhost.key
