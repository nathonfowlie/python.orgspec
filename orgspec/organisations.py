"""Organisation specifications.

Environments will be automagically loaded into the organisation via
naming convention (ie: there should be a module under 
`orgspec.environments` that exactly matches the organisations short name).
"""
from orgspec.common import Organisation

org1: Organisation = Organisation(name="Org 1", short_name="org1")

org2: Organisation = Organisation(name="Org 2", short_name="org2")
