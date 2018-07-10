#!/usr/bin/env python
import pyeapi
import six
import argparse
from pprint import pprint


def check_vlan_exists(eapi_conn, vlan_id):
    vlan_id = str(vlan_id)
    cmd = 'show vlan id {}'.format(vlan_id)
    try:
        response = eapi_conn.enable(cmd)
        check_vlan = response[0]['result']
        check_vlan = check_vlan['vlans']
        return check_vlan[vlan_id]['name']
    except (pyeapi.eapilib.CommandError, KeyError):
        pass
    return False


def configure_vlan(eapi_conn, vlan_id, vlan_name=None):
    cmd1 = 'vlan {}'.format(vlan_id)
    cmd = [cmd1]
    if vlan_name is not None:
        cmd2 = 'name {}'.format(vlan_name)
        cmd.append(cmd2)
    return eapi_conn.config(cmd)


def remove_vlan(eapi_conn, vlan_id):
    cmd = 'no vlan {}'.format(vlan_id)
    eapi_conn.config([cmd])


def main():
    eapi_conn = pyeapi.connect_to("pynet-sw4")

    #Argument parsing
    parser = argparse.ArgumentParser(
        description="Idempotent add/del vlan for Arista switch"
    )
    parser.add_argument("vlan_id", help="VLAN number to create or remove",
                        action="store", type=int)
    parser.add_argument(
        "--name",
        help="Specify VLAN name",
        action="store",
        dest="vlan_name",
        type=str
    )
    parser.add_argument("--remove", help="Remove VLAN ID", action="store_true")
    
    cli_args = parser.parse_args()
    vlan_id = cli_args.vlan_id
    remove = cli_args.remove
    vlan_name = cli_args.vlan_name
    
    #print(vlan_id)
    #print(remove) true/false
    #print(vlan_name) if not there equals None
    
    # Check if vlan exists
    check_vlan = check_vlan_exists(eapi_conn, vlan_id)
    print(check_vlan)

    if remove:
        if vlan_id == 1:
            print('eek, run for the hills')
            exit()
        if check_vlan:
            print("VLAN exists, removing it")
            remove_vlan(eapi_conn, vlan_id)
        else:
            print("VLAN does not exist, nothing to do.")
    else:
        if check_vlan:
            if vlan_name is not None and check_vlan != vlan_name:
                print("VLAN already exists, setting VLAN name")
                configure_vlan(eapi_conn, vlan_id, vlan_name)
            else:
                print("VLAN already existing, nothing do do.")
        else:
            print("Adding VLAN including vlan_name (if present)")
            configure_vlan(eapi_conn, vlan_id, vlan_name)
            

if __name__ == '__main__':
    main()