''' step definition module for the stop-instance feature '''
from time import sleep
from lettuce import step, before, world
from src.domain.reaper import Reaper

# constants
INSTANCE_REGION = 'ap-southeast-1'
DEV_INSTANCE_ID = 'i-0204ddc16a3b74ed6'
NO_TAG_INSTANCE_ID = 'i-0410e95c99adb71bb'
REAPER = Reaper('ap-southeast-1')


@before.all
def before_hook():
    ''' set up all instances for testing purposes '''
    test_instances = REAPER.ec2_client.start_instances(
        InstanceIds=[NO_TAG_INSTANCE_ID, DEV_INSTANCE_ID])['StartingInstances']

    for instance in test_instances:
        state = instance['CurrentState']['Name']

        while state != 'running':
            sleep(15)
            instance_copy = REAPER.ec2_client.describe_instances(
                InstanceIds=[instance['InstanceId']])['Reservations'][0]['Instances'][0]
            state = instance_copy['State']['Name']


@step(u'Given an EC2 instance with tag Stack Value is "([^"]*)"')
def given_an_ec2_instance_with_tag_stack_value(step, stack_value):
    ''' given an instance with a stack value tag '''
    filters = REAPER.build_filter_criteria(stack_value)
    reservations = REAPER.ec2_client.describe_instances(Filters=filters)[
        'Reservations']

    world.instance = reservations[0]['Instances'][0]
    tags = REAPER.get_tags(world.instance)

    assert len(reservations[0]['Instances']) == 1
    assert stack_value in tags
    world.stack_value = stack_value


@step(u'Then the EC2 instance should continue running')
def then_the_ec2_instance_should_continue_running(step):
    ''' then the instance should continue running '''
    assert REAPER.is_instance_stopped(world.instance['InstanceId']) is False


@step(u'Then the instance should not be reaped')
def then_the_instance_should_not_be_reaped(step):
    ''' then the instance should not be reaped '''
    assert REAPER.is_instance_stopped(world.instance['InstanceId']) is True


@step(u'When the EC2 instance is Idle')
def when_the_ec2_instance_is_idle(step):
    ''' determine whether the instance is idle '''
    world.is_idle_instance = REAPER.is_instance_idle(world.instance)


@step(u'Then the EC2 instance should be reaped')
def then_the_ec2_instance_should_be_reaped(step):
    ''' reap the instance '''
    assert REAPER.is_instance_stopped(world.instance['InstanceId']) is True

# @step(u'When the average Network Out is "([^"]*)" over the last "([^"]*)"')
# def when_the_average_network_out_is_group1_over_the_last_group2(step, network_out, time_period):
#     world.network_out = network_out


# @step(u'And the average CPU utilisation is "([^"]*)" over the last "([^"]*)"')
# def and_the_average_cpu_utilisation_is_group1_over_the_last_group2(step, cpu_util, time_period):
#     world.idle_instance = is_instance_idle(world.instance['InstanceId'])
