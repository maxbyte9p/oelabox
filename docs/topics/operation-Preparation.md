<!--
SPDX-FileCopyrightText: 2024 Maxine Hayes <maxinehayes90@gmail.com>
SPDX-License-Identifier: CC-BY-SA-4.0
-->
# Preparation

## Recommended Hardware Specs
Recommended hardware specs are based on my workstation specs.

The recommended specs are as follows:
- An 8 core 16 thread CPU (Ryzen 5800x)
- 16 GB of DDR4 memory
- Atleast 200 GB of storage space

I recommend a CPU like the Ryzen 5800x specifically due to it being a great processor with enough cores which can be dedicated to the Oela Box virtual machines. It is important to ensure we have enough cores in order to get the best performance out of Oela Box. This processor also gives us enough wiggle room to dedicate more cores if we choose to do so.

I recommend at least 16 GB of memory due to the fact Oela Box eats a lot of memory. It often uses up to 10 GB of memory on my workstation. It has been difficult to run Oela Box alongside other applications. I had many times where I would run entirely out of both memory and swap causing my system to freeze.

I recommend at least 200 GB of storage space as that gives us wiggle room for the Koji server. Package builds in Koji can use up a lot of disk space and it's best for us to have more than we need rather than not enough. As of right now the Koji server defined in the Vagrant file is hard coded to create a 70 GB disk. This is good for testing, but I recommend upping it to much more than that.

Lastly, I recommend running Oela Box on a dedicated machine, so you don't run into any similar memory related issues mentioned before.

## Recommended Virtual Machine Specs
Recommended virtual machine specs are based on my QA testing virtual machine.

The recommended specs are as follows:
- 8 cores dedicated
- 10 GB dedicated memory
- 200 GB dedicated storage space

I recommend dedicating 8 cores in order to ensure the Oela Box virtual machines which will be nested can also have dedicated cores.

I recommend 10 GB of dedicated memory as that is the absolute bare minimum for running Oela Box inside of a virtual machine running Rocky 9.3 Minimal.

I recommend 200 GB of dedicated storage space for the same reason as before in Recommended Hardware Specs.

## OS Compatibility
A Rocky Linux 9.3 or Oracle Linux 9.3 install is recommended.

Oela Box has been thoroughly tested on Rocky Linux 9.3 minimal and Oracle Linux 9.3 minimal. All parts of Oela Box are ensured to work on Rocky Linux 9.3 and Oracle Linux 9.3.

Oela Box is likely to work on other Enterprise Linux distributions with minimal modification, but this is not guaranteed and has not been thoroughly tested. However I still want to support the entire Enterprise Linux ecosystem.

## Automated Setup
Setup of Oela Box is automated using a shell script called "setup.sh" and an Ansible playbook called "setup.yml".

The "setup.sh" shell script bootstraps a Rocky Linux 9.3 install to be able to run the "setup.yml" Ansible playbook. Once the system is capable of running the playbook the script then runs the playbook for us.

The "setup.yml" playbook installs all the required dependencies and configures the system for Oela Box.

To run the "setup.sh" script:
```
sudo sh setup.sh
```

Setup is estimated to take about 10 - 20 minutes.
