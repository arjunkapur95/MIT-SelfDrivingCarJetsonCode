from sweeppy import Sweep

with Sweep('/dev/ttyUSB1') as sweep:
    sweep.start_scanning()

    for scan in sweep.get_scans():
        print('{}\n'.format(scan))
