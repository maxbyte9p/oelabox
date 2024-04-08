# Tools

Tools in Oela Box are stored under the tools directory corresponding to which virtual machine they are designed to be run on.

For example the path to Oela Importer.
```
tools/oelabox-koji/oelaimporter
```

Tools are automatically installed to their corresponding virtual machines using a similar directory tree. Virtual machines which have tools associated with them have their tools directory stored under the vagrant user's home directory.

For example Oela Importer installed on the Koji Server.
```
/home/vagrant/tools/oelaimporter
```

The ansible playbook which automatically installs Oela Box tools is called 'setup-oelabox-tools.yml'. It is automatically ran after provisioning and can be run again using the following command.
```
vagrant provision --provision-with tools
```

Each tool also has a corresponding 'install.yml' Ansible tasks file. This file is responsible for installing any dependencies required to run a specific tool and it is responsible for installing the tool itself. The 'setup-oelabox-tools.yml' playbook automatically looks for this file when installing tools and imports it during the playbook run. In a way Ansible is being used much like a package manager here.

## Oela Box Koji

### Oela Importer
Oela Importer is a tool designed to import OpenELA RPM sources from the openela-main SCM on GitHub. It is a simple, but powerful tool that makes the process of importing thousands of RPM sources much easier. Oela Importer is also designed to be as general as possible, so it may be modified to accomodate other SCMs.

#### Basic Usage
Oela Importer is fairly easy to use and basic usage of it can be enough to get things going the way one sees fit.

In this example Oela Importer will import all OpenELA RPM sources from the 'el8' branch from the 'openela-main' SCM on GitHub to the 'dist-oela8' dist tag in Koji as the 'oelakoji' user.
```
python3.11 ~/tools/oelaimporter/oelaimporter.py -u oelakoji -s openela-main -d dist-oela8 -b el8
```

We should see an output like the following.
```
===Oela Importer=============================================================================
---Import------------------------------------------------------------------------------------
  Repo: libguestfs                                                                           
  Branch Matches: ['el8']                                                                   
  Import IDs: [30]                            
---Import------------------------------------------------------------------------------------
  Repo: cockpit                                                                              
  Branch Matches: ['el8']                                                                   
  Import IDs: [31]                            
---Import------------------------------------------------------------------------------------
  Repo: abrt                                  
  Branch Matches: ['el8']                                                                    
  Import IDs: [32]                                                                           
...
```

Something import to note is Import IDs correspond to the task IDs in Koji. This is so we can note down the import IDs and check on them later using the Koji cli commands if we choose to.

This command can take hours to finish due to it processing as of writing 3,000 git repositories from 'openela-main'. However it might be fun to gaze at the pretty output of Oela Importer and watch as it takes on the monumental task.

Something else to mention is the fact we're not using a GitHub API token, so we will be denied from sending API requests quite frequently. Without a token we can only send 60 API requests per hour. This is a part of why this command will take next to forever to finish. Just guestimating we are only importing about 40 or so repositories per hour.

Oela Importer has support for using a GitHub API token to speed things up. All we have to do is add the '-t' argument with our API token.
```
python3.11 ~/tools/oelaimporter/oelaimporter.py -t YOUR_TOKEN_HERE -u oelakoji -s openela-main -d dist-oela8 -b el8
```

Using our token we bump up our API request limit to 5,000 requests per hour. This allows us to import a lot more repositories which should make importing much faster.

#### Regex Mode
Oela Importer supports regex for branch matching. Regex Mode is very powerful and allows us to import multiple branches at a time from a repository.

Previously we were importing sources from a specific branch. Now we can import sources from branches which generally match what we want.

In this example we'll be importing the 'el8' and 'el-8.8' branches using a regex pattern. We use the '-r' flag to enable regex mode.
```
python3.11 ~/tools/oelaimporter/oelaimporter.py -u oelakoji -s openela-main -d dist-oela8 -r -b "^el8$|^el-8.8$"
```

We should see an output like the following.
```
===Oela Importer=============================================================================
---Import------------------------------------------------------------------------------------
  Repo: libguestfs                                                                           
  Branch Matches: ['el8', 'el-8.8']    
  Import IDs: [53, 54]                        
---Import------------------------------------------------------------------------------------  Repo: cockpit
  Branch Matches: ['el8']                                                                    
  Import IDs: [55]                                                                           
---Import------------------------------------------------------------------------------------  Repo: abrt
  Branch Matches: ['el8']                                                                   
  Import IDs: [56]
...
```

In the output we can now see that Oela Importer has imported both the 'el8' and the 'el-8.8' branches for libguestfs. 

#### Machine Readable Mode
Oela Importer supports outputting import data in a machine readable format. The data for each import is printed out in JSON format. 

We can enable machine readable mode with the '-m' flag.
```
python3.11 ~/tools/oelaimporter/oelaimporter.py -u oelakoji -s openela-main -d dist-oela8 -b el8 -m
```

We should see an output like the following.
```
{"repo": "libguestfs", "imported": [{"branch_match": "el8", "import_id": 64}]}
{"repo": "cockpit", "imported": [{"branch_match": "el8", "import_id": 65}]}
{"repo": "abrt", "imported": [{"branch_match": "el8", "import_id": 66}]}
```

Machine readable mode allows us to use external scripts or programs to parse the data and do what we want with it.

This allows us to do things like write a logging script in Bash. Make sure to `sudo dnf install -y expect jq` to get the 'unbuffer' and 'jq' commands.
```
unbuffer python3.11 ~/tools/oelaimporter/oelaimporter.py -u oelakoji -s openela-main -d dist-oela8 -b el8 -m -c '10' |
while read json
do
    repo=$(echo $json | jq -r -M '.repo')
    readarray -t bmatches <<<$(echo $json | jq -r -M '.imported[].branch_match')
    readarray -t iids <<<$(echo $json | jq -r -M '.imported[].import_id')
    echo "<$(date)> Imported -- Repo: $repo, Branch Matches: [$(echo ${bmatches[@]} | sed 's/ /, /g')], Import IDs: [$(echo "${iids[@]}" | sed 's/ /, /g')]"
done
```

Run the script.
```
sh example.sh
```

We should see an output like so.
```
<Mon Apr  8 19:38:46 UTC 2024> Imported -- Repo: libguestfs, Branch Matches: [el8], Import IDs: [85]
<Mon Apr  8 19:38:46 UTC 2024> Imported -- Repo: cockpit, Branch Matches: [el8], Import IDs: [86]
<Mon Apr  8 19:38:47 UTC 2024> Imported -- Repo: abrt, Branch Matches: [el8], Import IDs: [87]
...
```

We can also pipe the output of our example script into tee, so we can save the logs to a file and view them at the same time.
```
sh example.sh | tee -a log.txt
```

We should see the same output we got before and the 'log.txt' file should have the same data as well.
```
[vagrant@koji ~]$ cat log.txt 
<Mon Apr  8 19:41:02 UTC 2024> Imported -- Repo: libguestfs, Branch Matches: [el8], Import IDs: [92]
<Mon Apr  8 19:41:02 UTC 2024> Imported -- Repo: cockpit, Branch Matches: [el8], Import IDs: [93]
<Mon Apr  8 19:41:02 UTC 2024> Imported -- Repo: abrt, Branch Matches: [el8], Import IDs: [94]
<Mon Apr  8 19:41:03 UTC 2024> Imported -- Repo: anaconda, Branch Matches: [el8], Import IDs: [95]
<Mon Apr  8 19:41:03 UTC 2024> Imported -- Repo: anaconda-user-help, Branch Matches: [el8], Import IDs: [96]
<Mon Apr  8 19:41:04 UTC 2024> Imported -- Repo: cloud-init, Branch Matches: [el8], Import IDs: [97]
<Mon Apr  8 19:41:04 UTC 2024> Imported -- Repo: crash, Branch Matches: [el8], Import IDs: [98]
<Mon Apr  8 19:41:05 UTC 2024> Imported -- Repo: dhcp, Branch Matches: [el8], Import IDs: [99]
<Mon Apr  8 19:41:05 UTC 2024> Imported -- Repo: dnf, Branch Matches: [el8], Import IDs: [100]
<Mon Apr  8 19:41:06 UTC 2024> Imported -- Repo: firefox, Branch Matches: [el8], Import IDs: [101]
```

#### Chunking
Oela Importer has a feature reffered to as 'chunking'. Chunking is where we specify a ratio or a 'chunk' with the '-c' flag. This tells Oela Importer to only import a 'chunk' of RPM sources from an SCM. In fact chunking was used in the logging script example from earlier to keep things brief.

We can use the chunking feature in various ways. These are just a couple examples.

We can tell Oela Importer to only import 10 repositories.
```
python3.11 ~/tools/oelaimporter/oelaimporter.py -u oelakoji -s openela-main -d dist-oela8 -b el8 -c '10'
```

We should see an output like so.
```
===Oela Importer=============================================================================
---Import------------------------------------------------------------------------------------
  Repo: libguestfs
  Branch Matches: ['el8']
  Import IDs: [129]
---Import------------------------------------------------------------------------------------
  Repo: cockpit
  Branch Matches: ['el8']
  Import IDs: [130]
---Import------------------------------------------------------------------------------------
  Repo: abrt
  Branch Matches: ['el8']
  Import IDs: [131]
---Import------------------------------------------------------------------------------------
  Repo: anaconda
  Branch Matches: ['el8']
  Import IDs: [132]
---Import------------------------------------------------------------------------------------
  Repo: anaconda-user-help
  Branch Matches: ['el8']
  Import IDs: [133]
---Import------------------------------------------------------------------------------------
  Repo: cloud-init
  Branch Matches: ['el8']
  Import IDs: [134]
---Import------------------------------------------------------------------------------------
  Repo: crash
  Branch Matches: ['el8']
  Import IDs: [135]
---Import------------------------------------------------------------------------------------
  Repo: dhcp
  Branch Matches: ['el8']
  Import IDs: [136]
---Import------------------------------------------------------------------------------------
  Repo: dnf
  Branch Matches: ['el8']
  Import IDs: [137]
---Import------------------------------------------------------------------------------------
  Repo: firefox
  Branch Matches: ['el8']
  Import IDs: [138]
```

We can tell Oela Importer to only import repositories starting from index 10 and ending at index 15.
```
python3.11 ~/tools/oelaimporter/oelaimporter.py -u oelakoji -s openela-main -d dist-oela8 -b el8 -c '10:15'
```

We should see an output like so.
```
===Oela Importer=============================================================================
---Import------------------------------------------------------------------------------------
  Repo: fwupd
  Branch Matches: ['el8']
  Import IDs: [121]
---Import------------------------------------------------------------------------------------
  Repo: gcc
  Branch Matches: ['el8']
  Import IDs: [122]
---Import------------------------------------------------------------------------------------
  Repo: gdb
  Branch Matches: ['el8']
  Import IDs: [123]
---Import------------------------------------------------------------------------------------
  Repo: gnome-session
  Branch Matches: ['el8']
  Import IDs: [124]
---Import------------------------------------------------------------------------------------
  Repo: gnome-settings-daemon
  Branch Matches: ['el8']
  Import IDs: [125]
```

Chunking is really useful for doing groups of imports or starting back where we left off in a situation where Oela Importer is interrupted. Chunking also makes it really easy to do testing or develop scripts. In the logging example without chunking it would have kept going and taken forever to test while writing these docs. Granted the script could have been interrupted with ctrl-c, but it's a bit of a hassle to deal with Python's stacktrace. It also allows us to see what our script might do from beginning to end without having to figure out which output came from where during debugging. 
