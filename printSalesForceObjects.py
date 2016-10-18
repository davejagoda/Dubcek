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

def walkAccounts(salesforce, sfid):
    result = []
    allaccounts = salesforce.query_all('select Id, Name from Account')
    for record in allaccounts['records']:
        if sfid:
            tuple = (record['Id'], record['Name'])
        else:
            tuple = (record['Name'])
        result.append(tuple)
    return(result)

def walkContacts(salesforce, sfid):
    result = []
    allcontacts = salesforce.query_all('select Id, Name, Email from Contact')
    for record in allcontacts['records']:
        if record['Email'] is None:
            email = 'NO EMAIL'
        else:
            email = record['Email']
        if sfid:
            tuple = (record['Id'], record['Name'], email)
        else:
            tuple = (record['Name'], email)
        result.append(tuple)
    return(result)

def print_nicely(result):
    broken_bar = unichr(0x00a6)
    for row in result:
        if (str == type(row) or unicode == type(row)):
            print(row)
        else:
            print(broken_bar.join(row))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--production', action='store_true', help='use production SalesForce instance')
    parser.add_argument('--sfid', action='store_true', help='display SalesForce ID')
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
        result = walkAccounts(salesforce, args.sfid)
    if args.contact:
        result = walkContacts(salesforce, args.sfid)
    print(len(result))
    print_nicely(result)
