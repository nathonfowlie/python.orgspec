"""Main entrypoint for the demo orgspec utility."""
from orgspec import init_config
from orgspec.organisations import org1, org2

init_config()

print("-" * 80)
print("Organisation 1 Specification")
print("-" * 80)
print(org1)


print("\n")
print("-" * 80)
print("Organisation 2 Specification")
print("-" * 80)
print(org2)
