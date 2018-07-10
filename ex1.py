#!/usr/bin/env python
import pyeapi
import six
from pprint import pprint

def main():
    eapi_conn = pyeapi.connect_to("pynet-sw4")
    
    interfaces = eapi_conn.enable("show interfaces")
    interfaces = interfaces[0]['result']
    interfaces = interfaces['interfaces']
    
    #pprint(interfaces)
    
    intf_stats = {}
    for interface, int_values in interfaces.items():
        int_counters = int_values.get('interfaceCounters', {})
        #int_counters = int_values['interfaceCounters']
        #.get will return {} if 'interfaceCounters' does not exist
        
        intf_stats[interface] = (int_counters.get('inOctets'), int_counters.get('outOctets'))
        #.get will return None if '[in|out]Octets' does not exist
        
    #pprint(intf_stats)
    
    print("\n{:20} {:<20} {:<20}".format("Interface:", "inOctets", "outOctets"))
    for intf, octets in sorted(intf_stats.items()):
        print("{:20} {:<20} {:<20}".format(intf, six.text_type(octets[0]),
                                           six.text_type(octets[1])))
    print()
    
if __name__ == '__main__':
    main()