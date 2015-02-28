#!/usr/bin/env python

import os, sys, argparse
import simple_salesforce

def loginToSalesForce(isProduction):
    sandbox = not isProduction
    u = os.getenv('SalesForceUserName')
    p = os.getenv('SalesForcePassWord')
    t = os.getenv('SalesForceToken')
    if u == None:
        print('set the SalesForceUserName environment variable')
        sys.exit(1)
    if p == None:
        print('set the SalesForcePassWord environment variable')
        sys.exit(1)
    if t == None:
        print('set the SalesForceToken environment variable')
        sys.exit(1)
    salesforce = simple_salesforce.Salesforce(
        username = u, password = p, security_token = t, sandbox = sandbox)
    return(salesforce)

def walkAccounts(salesforce):
    allaccounts = salesforce.query_all('select Id, Name from Account')
    for record in allaccounts['records']:
        print(record['Name'].encode('utf8'))

def walkContacts(salesforce):
    allcontacts = salesforce.query_all('select Id, Name, Email from Contact')
    for record in allcontacts['records']:
        try:
            print(record['Name'].encode('utf8') + ':' + record['Email'])
        except:
            print(record['Name'].encode('utf8') + ':')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--production', action='store_true', help='use production SalesForce instance')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--account', action='store_true')
    group.add_argument('--contact', action='store_true')
    args = parser.parse_args()
    if args.production:
        print('using production instance')
    else:
        print('using test instance')
    salesforce = loginToSalesForce(args.production)
    if args.account:
        walkAccounts(salesforce)
    if args.contact:
        walkContacts(salesforce)
