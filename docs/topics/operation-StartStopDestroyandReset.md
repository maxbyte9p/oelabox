<!--
SPDX-FileCopyrightText: 2024 Maxine Hayes <maxinehayes90@gmail.com>
SPDX-License-Identifier: CC-BY-SA-4.0
-->
# Start, Stop, Destroy, and Reset

## Start
Starting Oela Box is pretty simple. Provisioning is estimated to take about 30 minutes.

```
vagrant up
```

## Stop
```
vagrant halt
```

## Destroy
```
vagrant destroy -f
```

## Reset
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

This is weird and I know it's weird, but trust me. I discovered this quirk from rapidly resetting Oela Box during development. It caused a lot of headache. Once I actually timed it. I found vagrant destroy, wait 10 minutes, and vagrant up to be the most predictable way to reset Oela Box.
