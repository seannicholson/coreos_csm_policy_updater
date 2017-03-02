#coreos_csm_policy_updater

Disclaimer: This script is provided as is. USE AT YOUR OWN RISK.
NOT A SUPPORTED SOLUTION

To configure script add API Key information and CSM Policy ID to cloudpassage.yml File
>key_id: your_api_key_id

>secret_key: your_api_secret_key

>csm_policy_id: your_csm_policy_id


This script queries the CoreOS version endpoints to retrieve the current versions
for each release of CoreOS (Alpha, Beta, Stable)
>https://coreos.com/dist/aws/aws-alpha.json

>https://coreos.com/dist/aws/aws-beta.json

>https://coreos.com/dist/aws/aws-stable.json


In order for this scrip to work, your Halo CSM policy must contain three
file configuration setting checks that have the remediation suggestion set to
Alpha, Beta, or Stable. If this section of the checks is not configured, the
script will not find a match to update the policy.

Checks should be formatted like this example


>object_type: "configuration_file_setting",
active: true,
exportable: true,
suggestion: "Alpha",
config_file_path: "/etc/os-release",
config_file_section: "",
config_item: "VERSION",
desired_value: "1325.1.0",
comment_character: "#",
delimiter: "="
