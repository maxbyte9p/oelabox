<!--
SPDX-FileCopyrightText: 2024 Maxine Hayes <maxinehayes90@gmail.com>
SPDX-License-Identifier: CC-BY-SA-4.0
-->
# Koji Server

# Login Through SSH
Logging in through ssh is quite simple. We use Vagrant's ssh plugin to do so.

```
vagrant ssh kojiserver
```

# Login To The oelakoji User With Kerberos
The oelakoji user is the admin user for the Koji instance running on the Koji server. The oelakoji user is used to start package builds, edit dist tags and run all sorts of tasks.

It is also quite simple to login. We use kinit which will prompt us for a password. By default the password is "ThisIsNotMyPassword1!".

```
kinit oelakoji
```

We can also use a one liner in scripts or Ansible playbooks to login. This works because kinit can take input from stdin.
```
echo 'ThisIsNotMyPassword1!' | kinit oelakoji
```

In fact a oneliner like this is used in "init-koji.yml" located in tasks/oelabox-koji. This is the tasks file that the "init-oelabox-koji-ecosystem.yml" playbook uses to initialize the Koji instance running on the Koji server.

```
- name: kinit as koji admin using password
  ansible.builtin.shell: "set -o pipefail && echo \"{{ oelakoji_password }}\" | kinit oelakoji@OELABOX.LOCAL"
  check_mode: false
  changed_when: "1 != 1"
  become: true
  become_user: koji
```

## Test Koji Kerberos Authentication
It is important to always test authentication for the Koji instance. By testing authentication we can catch issues with the Koji instance early which prevents headaches in the future.

Testing authentication is fairly easy.
```
koji moshimoshi
```

The "koji moshimoshi" command should return a message along the lines of "Hello, oelakoji!" in a randomly chosen language. A few examples are provided.

Example 1:
```
g'day, oelakoji!

You are using the hub at https://koji.oelabox.local/kojihub
Authenticated via GSSAPI
```

Example 2:
```
grüezi, oelakoji!

You are using the hub at https://koji.oelabox.local/kojihub
Authenticated via GSSAPI
```

Example 3:
```
dobrý den, oelakoji!

You are using the hub at https://koji.oelabox.local/kojihub
Authenticated via GSSAPI
```

# About Package Building

## Basic Information About Tags
Something to note about Koji tags is that they are very confusing. I've tried to explain a couple of commonly used tags in this section the best I could.

### Dist Tags
Dist tags have a prefix called "dist". These tags are what we primarily add packages to.

### Build Tags
Build tags have a suffix called "build" and typically have a dist prefix. They're primarily for defining internal repos for koji. They also provide DNF package groups called "build" and "srpm-build" for dist tags. Build tags also inherit other tags such as "el8" and "dist-oela8". 

## SCM
An SCM (Source Control Management) system is what Koji calls services like GitLab, Gitea, and GitHub.

The kojid configuration also contains a list of SCMs which users a permitted to build from. For Oela Box only one SCM is permitted. The current SCM permitted is "github.com/openela-main".

When we build a package from an SCM we are simply providing Koji with a URL to a git repository containing the package sources. With this URL Koji knows that it must clone the git repository into the mock chroot.

A SCM URL pointing to sources for a package is constructed like so.

Sections:
```
git+https://    github.com/openela-main/    bash            #el8
^               ^                           ^               ^
Protocol        SCM                         Pkg Repository  Repository Branch
```

Full URL:
```
git+https://github.com/openela-main/bash#el8
```

I hope this helps you understand how an SCM works with Koji. This is another one of those confusing parts of Koji where I'm trying to explain it the best I can.

## Building A Package
In order to build a package in Koji we first need to add it to a dist tag. For this example the bash package will be used and it will be added to the 'dist-oela8' tag. The oelakoji user will also be marked as the owner of this package.

```
koji add-pkg dist-oela8 bash --owner oelakoji
```

Once we have added our package to the appropriate dist tag we can now submit a build job to Koji. We will be building using the 'dist-oela8' tag/build target. Our SCM is 'github.com/openela-main'. The bash package source repository is 'bash' and we will be using the branch 'el8'.

```
koji build dist-oela8 'git+https://github.com/openela-main/bash#el8'
```

Once we have submitted the build job we should initially see an output like so.

```
Created task: 41
Task info: https://koji.oelabox.local/koji/taskinfo?taskID=41
Watching tasks (this may be safely interrupted)...
41 build (dist-oela8, /openela-main/bash:el8): free
```

The 'https://koji.oelabox.local/koji/taskinfo?taskID=41' URL can be used to watch the task on the Koji web interface.

Over time Koji will give us more information about the task and new tasks stemming from the initial task. It will also let us know the current status/results of tasks with a message like like the following.

```
  0 free  1 open  1 done  0 failed
```

Once our package finishes building we should have an output that looks like the following.

```
Created task: 41
Task info: https://koji.oelabox.local/koji/taskinfo?taskID=41
Watching tasks (this may be safely interrupted)...
41 build (dist-oela8, /openela-main/bash:el8): free
41 build (dist-oela8, /openela-main/bash:el8): free -> open (koji.oelabox.local)
  42 buildSRPMFromSCM (/openela-main/bash:el8): open (koji.oelabox.local) -> closed
  0 free  1 open  1 done  0 failed
  43 buildArch (bash-4.4.20-4.el8.src.rpm, i686): free
  44 buildArch (bash-4.4.20-4.el8.src.rpm, x86_64): free
  43 buildArch (bash-4.4.20-4.el8.src.rpm, i686): free -> open (koji.oelabox.local)
  44 buildArch (bash-4.4.20-4.el8.src.rpm, x86_64): free -> open (koji.oelabox.local)
  44 buildArch (bash-4.4.20-4.el8.src.rpm, x86_64): open (koji.oelabox.local) -> closed
  0 free  2 open  2 done  0 failed
  43 buildArch (bash-4.4.20-4.el8.src.rpm, i686): open (koji.oelabox.local) -> closed
  0 free  1 open  3 done  0 failed
  45 tagBuild (noarch): free
  45 tagBuild (noarch): free -> closed
  0 free  1 open  4 done  0 failed
41 build (dist-oela8, /openela-main/bash:el8): open (koji.oelabox.local) -> closed
  0 free  0 open  5 done  0 failed

41 build (dist-oela8, /openela-main/bash:el8) completed successfully 
```

We can now see our completed build listed in koji by either going to the https://koji.oelabox.local/koji web interface or on the command line.

```
koji list-builds --owner oelakoji
```






