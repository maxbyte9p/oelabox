# oela-koji tools

Right now the tools directory doesn't hold anything other than Oela Importer and a script to install its dependencies.

The vagrant virtual machines also do not share the Oela Box root directory yet. There's a bug with that where it gets a little quirky. Using NFS for synced folders also doesn't quite work. I have tried to skirt around this with the vagrant-sshfs plugin, but that seems to make the virtual machines unstable for some reason. I've had to reset the VMs countless times during the development of Oela Importer for Oela Box. (The VMs just stopped working again while writing this. I think no more vagrant-sshfs from now on.)

Anyway, if you want to run Oela Importer on the koji server it needs to be copied over. I recommend using the vagrant-scp plugin for this as I've had a good experience with it before. The deps.sh script also needs to be copied over and ran to install the required dependencies.

To run Oela Importer after following the above steps (don't forget to ssh into the koji server):
```
echo "ThisIsNotMyPassword1!" | kinit oelakoji

python3.11 oelaimporter.py -u oelakoji -s openela-main -d dist-oela8 -b el8
```

To use regex mode:
```
python3.11 oelaimporter.py -u oelakoji -s openela-main -d dist-oela8 -b "^el-8.8$|^el8$" -r
```

To import only a specified slice of repositories.
```
python3.11 oelaimporter.py -u oelakoji -s openela-main -d dist-oela8 -b "el8" -c "5:10"
```
