# Louis Abel <label@rockylinux.org>
# This is a koji plugin to assist in auto signing packages in sigul
# This is going through constant change until it "works"
#
# Based on another plugin, updated and refinements where needed:
#   -> Config file introduced
#   -> Some linting
#
# TODO: Hook into a vault system

import sys
import logging
import subprocess
import os

import koji
from koji.plugin import register_callback, ignore_error
if '/usr/share/koji-hub' not in sys.path:
    sys.path.append("/usr/share/koji-hub")
import kojihub
from kojihub import RootExports

# CONVERT TO CONFIG FILE
CONFIG_FILE = '/etc/koji-hub/plugins/key_signing.conf'
CONFIG = None
if not CONFIG:
    CONFIG = koji.read_config_files([(CONFIG_FILE, True)])

passphrase = CONFIG.get('signing', 'passphrase')
gpg_key_name = CONFIG.get('signing', 'gpg_key_name')
gpg_key_id = CONFIG.get('signing', 'gpg_key_id')
build_target = CONFIG.get('signing', 'build_target').split()
testing_tag = CONFIG.get('signing', 'testing_tag')
send_to_testing = CONFIG.get('signing', 'send_to_testing')
sigul_config = CONFIG.get('signing', 'sigul_config')

@callback('postTag')
def key_signing(cbtype, *args, **kws):
    # Make sure this is a package build and nothing else
    if kws['tag']['name'] not in build_target:
        return

    # The build has to succeed
    if kws['build']['state'] != 1:
        logging.getLogger('koji.plugin.key_signing').error('build state is not finished')
        return

    logging.getLogger('koji.plugin.key_signing').info('buildinfo: %s',str(kws))

    # Find all the RPMs that are part of this build
    kojifunctions = RootExports()
    build_rpms = kojifunctions.listBuildRPMs(kws['build']['id'])
    logging.getLogger('koji.plugin.key_signing').info('rpminfo: %s',str(build_rpms))

    # Sign and write the RPMs
    for rpm_info in build_rpms:
        rpm_name = "%s.%s" % (rpm_info['nvr'],rpm_info['arch'])
        key_signing_rpm(rpm_name)
        kojifunctions.writeSignedRPM(rpm_name,gpg_key_id)

    # If configured, tag for a testing repo
    if send_to_testing:
        kojifunctions.tagBuild(testing_tag,kws['build']['id'])
        logging.getLogger('koji.plugin.key_signing').info(
                'the package %s has been tagged to %s' % (kws['build']['name'],testing_tag))

def run_sigul(command):
    passphrase_to_bytes = '{}\0'.format(passphrase).encode()
    p = os.pipe()
    os.write(p[1], passphrase_to_bytes)
    os.close(p[1])
    send_to_stdin = os.fdopen(p[0], "r")

    child = subprocess.Popen(command, stdin=send_to_stdin,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,shell=True)

    ret = child.wait()
    logging.getLogger('koji.plugin.key_signing').info('sigul returned with code: %s',ret)
    if ret != 0:
        logging.getLogger('koji.plugin.key_signing').error(
                'sigul command failed: %s returned: %s',command,child.communicate())
        sys.exit(1)

def key_signing_rpm(rpm_name):
    # Check to make sure the key works
    command = "sigul -c %s --batch get-public-key %s" % (sigul_config, gpg_key_name)
    run_sigul(command)

    # Run the actual sign command
    command = ("sigul -c %s --batch sign-rpm --koji-only --store-in-koji"
               " --v3-signature %s %s" % (sigul_config, gpg_key_name, rpm_name))
    logging.getLogger('koji.plugin.key_signing').info('running sigul command: %s',command)
    run_sigul(command)

#register_callback('postTag',key_signing)
