#encoding: UTF-8
@reaper
Feature: Stop instance when Idle
  In order to reduce idle ec2 usage of dev and test machines
  As a lambda function or administrator
  We will kill idle instances using metadata

  Rules:
    - "Stack" tag must contain "Prod" otherwise it will be "reaped"
    - Instance idle > three hours (Average CPU utilisation is less than 2% and Average NetworkOut is less than 5kb)

      Scenario: Prod stack is "Idle"
    	Given an EC2 instance with tag Stack Value is "Prod"
    	When the EC2 instance is Idle
    	Then the EC2 instance should continue running

      Scenario: Non-Prod stack is "Idle"
    	Given an EC2 instance with tag Stack Value is "Dev"
    	When the EC2 instance is Idle
   	Then the EC2 instance should be reaped
