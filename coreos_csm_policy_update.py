#! /usr/local/bin/python

# Author: Sean Nicholson
# Script for querying the CoreOS endpoints for current versions of alpha, beta, & stable releases
# Then takin these value and updating a specific Halo CSM policy for checking CoreOS version compliance


import json, io, requests
import cloudpassage
import yaml


def create_api_session(session):
    config_file_loc = "cloudpassage.yml"
    config_info = cloudpassage.ApiKeyManager(config_file=config_file_loc)
    session = cloudpassage.HaloSession(config_info.key_id, config_info.secret_key)
    return session


def retrieve_coreos_csm(session):
    with open('cloudpassage.yml', 'r') as f:
        config_file = yaml.load(f)
    coreos_policy_id = config_file['defaults']['csm_policy_id']
    csm_policy = cloudpassage.HttpHelper(session)
    coreos_policy = csm_policy.get("/v1/policies/" + coreos_policy_id)
    cores_policy = fixup (coreos_policy, u'desired_value')
    return coreos_policy


def update_coreos_csm_policy(coreos_policy, session):
    if update_policy > 0:
        csm_policy = cloudpassage.ConfigurationPolicy(session)
        data = json.dumps(coreos_policy)
        csm_policy.update(data)
    else:
        return

def fixup(adict, k):
    global update_policy
    update_policy = 0
    coreos_stable_version = get_coreos_new_version("stable")
    coreos_beta_version = get_coreos_new_version("beta")
    coreos_alpha_version = get_coreos_new_version("alpha")
    rules = adict['policy']['rules']
    for rule in rules:
        checks = rule['checks']
        for check in checks:
            if check['suggestion'] == 'Stable':
                if check[k] != coreos_stable_version:
                    check[k] = coreos_stable_version
                    update_policy += 1
            elif check['suggestion'] == 'Beta':
                if check[k] != coreos_beta_version:
                    check[k] = coreos_beta_version
                    update_policy += 1
            elif check['suggestion'] == 'Alpha':
                if check[k] != coreos_alpha_version:
                    check[k] = coreos_alpha_version
                    update_policy += 1
    return adict


def get_coreos_new_version(version):
    reply=[]
    coreos_url = "https://coreos.com/dist/aws/aws-%s.json" % version
    reply = requests.get(coreos_url)
    #print reply.json()['release_info']['version']
    return reply.json()['release_info']['version']


def main():
    api_session = None
    api_session = create_api_session(api_session)
    update_coreos_csm_policy(retrieve_coreos_csm(api_session), api_session)

if __name__ == "__main__":
    main()
