# Koji callback sent to Rocky Linux mqtt                                            
#                                                                              
# Adapted from https://gitlab.cern.ch/linuxsupport/rpms/koji-hub-plugins-cern/blob/master/src/mash.py
#                                                                              
# License: GPLv2                                                               
# Authors:                                                                     
#     Alex (dot) Iribarren (at) cern (dot) ch (original script)                
#     Thomas (dot) Oulevey (at) cern (dot) ch (mqtt version)
 
import koji
from koji import PluginError
from koji.context import context
from koji.plugin import callback, ignore_error
import kojihub
import ConfigParser
import logging
import base64, json
import os
 
# mqtt client
import paho.mqtt.client as mqtt
 
CONFIG_FILE = '/etc/koji-hub/plugins/rockymsg.conf'
PLUGIN_NAME = 'koji.plugin.rockymsg'
DEFAULT_ARCHES = 'x86_64'
 
config = None
tagCache = {}
 
def get_config():
    global config
    if config:
        return config
 
    config = ConfigParser.SafeConfigParser()
    config.read(CONFIG_FILE)
 
    if not config.has_section('rockymsg'):
        config.add_section('rockymsg')
    if not config.has_option('rockymsg', 'host'):
        logging.getLogger(PLUGIN_NAME).error('No mqtt host specified in config file!')
        return None
    if not config.has_option('rockymsg', 'port'):
        logging.getLogger(PLUGIN_NAME).error('No mqtt port specified in config file!')
        return None
    if not config.has_option('rockymsg', 'topic'):
        logging.getLogger(PLUGIN_NAME).error('No mqtt topic specified in config file!')
        return None
    if not config.has_option('rockymsg', 'ca_cert'):
        logging.getLogger(PLUGIN_NAME).error('No mqtt cacert specified in config file!')
        return None
    if not config.has_option('rockymsg', 'tls_cert'):
        logging.getLogger(PLUGIN_NAME).error('No mqtt tls_cert specified in config file!')
        return None
    if not config.has_option('rockymsg', 'tls_key'):
        logging.getLogger(PLUGIN_NAME).error('No mqtt tls_key specified in config file!')
        return None
    if not config.has_option('rockymsg', 'tls_insecure'):
        config.set('rockymsg' 'tls_insecure', 'False')
    if not config.has_option('rockymsg', 'tls_version'):
        config.set('rockymsg' 'tls_version', '2')
    if not config.has_option('rockymsg', 'exclude_tags'):
        config.set('rockymsg', 'exclude_tags', '')
 
    return config
 
def mqtt_on_publish(client,userdata,result):
  pass 

def _dispatch_on_topic(payload):
    logger = logging.getLogger(PLUGIN_NAME)
 
    config = get_config()
    if not config:
        raise PluginError('Unable to use the bus, config not found')
 
    if not payload['tag']:
        logger.info('No tag specified')
        return None
 
    exclude_tags = config.get('rockymsg', 'exclude_tags')
    if exclude_tags:
      exclude_tags = [x.strip() for x in exclude_tags.split(',')]
    else:
      exclude_tags = []
 
    if payload['tag'] in exclude_tags:
        logger.info('Tag %s excluded' % payload['tag'])
        return None
 
    mqtt_host          = config.get('rockymsg', 'host')
    mqtt_port          = config.get('rockymsg', 'port')
    mqtt_topic         = config.get('rockymsg', 'topic')
    mqtt_cacert        = config.get('rockymsg', 'ca_cert')
    mqtt_tls_cert      = config.get('rockymsg', 'tls_cert')
    mqtt_tls_key       = config.get('rockymsg', 'tls_key')
    mqtt_tls_insecure  = config.get('rockymsg', 'tls_insecure')
    mqtt_tls_version   = config.get('rockymsg', 'tls_version')
 
    # Connect to the bus
    try:
        client = mqtt.Client()
    except Exception as e:
        logger.error('mqtt client error: %s' % e.message) 
    client.tls_set(ca_certs=mqtt_cacert, certfile=mqtt_tls_cert, keyfile=mqtt_tls_key, tls_version=2)
 
    client.tls_insecure_set('False')
    try:
        client.on_publish = mqtt_on_publish
        client.connect(mqtt_host,mqtt_port)
    except Exception as e:
        logger.error('mqtt connection error: %s' % e.message)
 
    # Publish payload to the bus
    #
    ret = client.publish(mqtt_topic, json.dumps(payload))
 
    # Disconnect from the bus
    client.disconnect()
 
    return ret
 
def _get_build_target(task_id):
    try:
        task = kojihub.Task(task_id)
        info = task.getInfo(request=True)
        request = info['request']
        if info['method'] in ('build', 'maven'):
            # request is (source-url, build-target, map-of-other-options)
            if request[1]:
                return kojihub.get_build_target(request[1])
        elif info['method'] == 'winbuild':
            # request is (vm-name, source-url, build-target, map-of-other-options)
            if request[2]:
                return kojihub.get_build_target(request[2])
    except Exception as e:
        logger.error('Exception: %s', e)
 
    return None
 
 
@callback('postTag', 'postUntag')
#@ignore_error
def rockymsg(cbtype, *args, **kws):
    logger = logging.getLogger(PLUGIN_NAME)
    logger.debug('Called the %s callback, args: %s; kws: %s', cbtype, str(args), str(kws))
 
    tag = kws['tag']['name']
    build_task_id = kws['build']['task_id']
 
    build_target = _get_build_target(build_task_id)
    logger.debug('Build target: %s', build_target)
 
    arches = DEFAULT_ARCHES
    if build_target:
        build_tag = kojihub.get_tag(build_target['build_tag_name'])
        arches = build_tag['arches']
 
    payload = { 'action': cbtype, 'tag': tag, 'arches': arches }
    job = _dispatch_on_topic(payload)
    if job:
        logger.info('Sending payload: %s to mqtt - ret code: %s' % (payload, job))
