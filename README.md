# Oela Box

Oela Box is a infrstructure in a box designed for Enterprise Linux development. Oela Box utilizes Vagrant and Ansible for virtual machine provisioning. Oela Box specifically targets OpenELA development and is configured for OpenELA development. Theoretically any Enterprise Linux can be developed using Oela Box.

If you would like to learn more about Oela Box documentation can be found in the "docs" directory. As of right now the documentation is incomplete, but complete enough to help you understand how Oela Box works.

# Getting Started
To Get started with Oela Box I recommend having either a dedicated machine or virtual machine running either Rocky Linux 9.3 Minimal or Oracle Linux 9.3 Minimal.

## Recommended Specs
Recommended specs are based on my workstation specs.
The recommended specs are as follows:
- An 8 core 16 thread CPU (Ryzen 5800x)
- 16 GB of DDR4 memory
- Atleast 200 GB of storage space (For wiggle room, but you can get away with less)

For a virtual machine:
- 8 cores dedicated
- 10 GB dedicated memory
- 200 GB dediated storage space (For wiggle room, but you can get away with less)

## Run The Setup Script
A shell script is provided called "setup.sh". It bootstraps the system to be able to run the Ansible playbook. Once it has completed it will then run the setup.yml Ansible playbook. Setup is estimated to take about 10 - 20 minutes.

```
sudo sh setup.sh
```

## Start Oela Box
Starting Oela Box is pretty simple. Provisioning is estimated to take about 30 minutes.

```
vagrant up
```

## Stop Oela Box

```
vagrant halt
```

## Resetting Oela Box
If you want to reset Oela Box for any reason it's required to handle this carefully. Vagrant gets a little quirky when the vms are destroyed and recreated too quickly.

This will cause Vagrant to become unpredictable and may also result in the provisioning playbooks failing.
```
vagrant destroy -f && vagrant up
```

This will also make vagrant and provisioning unpredictable.
```
vagrant destroy -f && sleep 600 && vagrant up
```

The most predictable way to reset Oela Box is to vagrant destroy, get coffee and vagrant up.
```
vagrant destroy -f
```

Wait 10 minutes

```
vagrant up
```

This is weird and I know it's weird, but trust me. I discovered this quirk from rapidly resetting Oela Box during development. It caused a lot of headache. Once I actually timed it and found vagrant destroy, wait 10 minutes, and vagrant up was the way I had to do it.

## Local Web Interfaces.
The Free IPA and Koji web interfaces can be found at https://ipa.oelabox.local and https://koji.oelabox.local/koji. They're only accessible locally.

## Login To Koji Server and Start A Build

Login through ssh. (I usually use a VNC viewer since it's more stable.)
```
vagrant ssh kojiserver
```

Login to Kerberos as oelakoji. (Password: ThisIsNotMyPassword1!)
```
kinit oelakoji
```

Test Koji authentication. (Should say "Hello, oelakoji!" in a randomly chosen language)
```
koji moshimoshi
```

Add bash package to dist-oela8.
```
koji add-pkg dist-oela8 bash --owner oelakoji
```

Start build of Bash from openela-main SCM.
```
koji build dist-oela8 'git+https://github.com/openela-main/bash#el8'
```

You can now watch the task at https://koji.oelabox.local/koji or on the command line.


