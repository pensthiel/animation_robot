#!/usr/bin/python3
import uhubctl

uhubctl.utils.UHUBCTL_BINARY = "sudo /HEAD/local/bin/uhubctl"


hubs = uhubctl.discover_hubs()

for hub in hubs:
    print(f"Found hub: {hub}")

    for port in hub.ports:
        print(f"   Found port: {port}")
        
        # You can use the optional argument `cached_results=False` for each of 
        # these 3 methods in order to invalidate the internal cache,
        # which is used for performance reasons
        print(f"      Description: {port.description()}")
        print(f"      Vendor ID: {port.vendor_id()}")
        print(f"      Product ID: {port.product_id()}")