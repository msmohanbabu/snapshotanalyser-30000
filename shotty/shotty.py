import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances =[]

    if project:
         filters = [{'Name':'tag:Project', 'Values':[project]}]
         instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def cli():
    """Shotty manages snapshots"""

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list')
@click.option('--project', default=None,
help="Only Volumes for project (tag Project:<name>)")

def list_snapshots(project):
    "List EC2 Volumes"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print (", ".join((
                s.id,
                v.id,
                i.id,
                s.state,
                s.progress,
                s.start_time.strftime("%c")
                )))
    return

@cli.group('volumes')
def volumes():
    """Command for volumes"""

@volumes.command('list')
@click.option('--project', default=None,
help="Only Volumes for project (tag Project:<name>)")

def list_volumes(project):
    "List EC2 Volumes"

    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
             print(", ".join((
             v.id,
             i.id,
             v.state,
             str(v.size) + "GiB",
             v.encrypted and "Encrypted" or "Not Encrypted")))




@cli.group('instances')
def instances():
    """Commands for instances"""

@instances.command('snapshot',
      help="create snapshots for all volumes")
@click.option('--project', default=None,
help="Only Instances for project (tag Project:<name>)")
def create_snapshots(project):
    "Create snapshots"
@instances.command("list")

@click.option('--project', default=None,
help="Only Instances for project (tag Project:<name>)")

def list_instances(project):
    "List EC2 instances"
    instances = filter_instances(project)

    for i in instances:
        tags = {t['Key']:t['Value'] for t in i.tags or []}
        print(', '.join((
                i.id,
                i.instance_type,
                i.placement['AvailabilityZone'],
                i.state['Name'],
                i.public_dns_name,
                tags.get('Project', '<no project>'))))
    return

@instances.command('stop')
@click.option('--project', default=None,
help='Only Instances for project')
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)

    for i in instances:
         print ("Stopping {0}...".format(i.id))
         i.stop()

    return

@instances.command('start')
@click.option('--project', default=None,
help='Only Instances for project')
def start_instances(project):
    "Start EC2 instances"

    instances = filter_instances(project)

    for i in instances:
         print ("Starting {0}...".format(i.id))
         i.start()

    return

if __name__ == '__main__':
    cli()
