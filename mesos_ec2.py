import argparse
import logging
from autoscale import MesosReporter, MesosDecider, AwsAsgScaler
from time import sleep

_LOG_FORMAT_ = '%(filename)s|%(name)s|%(asctime)s.%(msecs)d|%(levelname)s|%(message)s'
_LOG_DATE_FORMAT_ = '%Y-%m-%dT%H:%M:%S'


def log(name, not_logged_libraries=None):
    logging.basicConfig(
        format=_LOG_FORMAT_,
        datefmt=_LOG_DATE_FORMAT_,
        level=getattr(logging, args.log_level.upper())
    )
    if not_logged_libraries:
        for library in not_logged_libraries:
            logging.getLogger(library).setLevel(logging.WARN)

    return logging.getLogger(name)


def main():
    while True:
        reporter = MesosReporter(args.mesos_url)
        decider = MesosDecider(thresholds)
        scaler = AwsAsgScaler(args.region, args.asg)

        delta = decider.should_scale(reporter)
        if delta:
            logger.info('Scaling {asg} in {region} by {delta}'.format(asg=args.asg, region=args.region, delta=delta))
            scaler.scale(delta)
        else:
            logger.info('No change needed for {asg} in {region}'.format(asg=args.asg, region=args.region))
        sleep(300)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-log', '--log-level', default="warn", help='Log level (debug, [default] info, warn, error)')
    parser.add_argument('-url', '--mesos-url', help='Mesos cluster URL', required=True)
    parser.add_argument('-c', '--cpus', help='Comma-delimited CPU thresholds (lower,upper)')
    parser.add_argument('-d', '--disk', help='Comma-delimited disk thresholds (lower,upper)')
    parser.add_argument('-m', '--mem', help='Comma-delimited memory thresholds (lower,upper)')
    parser.add_argument('-r', '--region', help='AWS region', required=True)
    parser.add_argument('-asg', '--asg', help='AWS auto scaling group name', required=True)

    args = parser.parse_args()

    logger = log('Autoscaling', not_logged_libraries=['boto', 'boto3'])

    thresholds = {}
    if args.cpus:
        lower, upper = args.cpus.split(',')
        thresholds['cpus'] = dict(lower=int(lower), upper=int(upper))
    if args.disk:
        lower, upper = args.disk.split(',')
        thresholds['disk'] = dict(lower=int(lower), upper=int(upper))
    if args.mem:
        lower, upper = args.mem.split(',')
        thresholds['mem'] = dict(lower=int(lower), upper=int(upper))

    main()
