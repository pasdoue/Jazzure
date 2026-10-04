# General information

IMDS (Instance MetaData Service) is a REST API (`http://169.254.169.254/metadata`) that runs inside Azure VM (same mechanism on all cloud providers, at least AWS & GCP).  
Those endpoints cannot be interrogated from outside the VM and prevent (normally) SSRF attacks.   

# Technical information

## Api-version
Contrary to AWS where it's like a simple web server you can navigate on, Microsoft decided to make it harder... 🥵  
The bottleneck is that there are several endpoints to retrieve metadata, and they depend on an `api-version` which are specific dates and updated sometimes. (the magical stuff of Microcro... 😤)

Bellow the summary, but for curious one's check every endpoint details here : https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service?tabs=linux#endpoint-categories 

| Category root               | Description                                      | Version introduced |
|-----------------------------|--------------------------------------------------|--------------------|
| `/metadata/attested`        | Attested Data                                    | 2018-10-01         |
| `/metadata/identity`        | Managed Identity via IMDS                        | 2018-02-01         |
| `/metadata/instance`        | Instance Metadata                                | 2017-04-02         |
| `/metadata/loadbalancer`    | Retrieve Load Balancer metadata via IMDS         | 2020-10-01         |
| `/metadata/scheduledevents` | Scheduled Events via IMDS                        | 2017-08-01         |
| `/metadata/versions`        | Versions                                         | N/A                |

There are function developed inside `imds.py` that will retrieve for each endpoint all available "api-version" (except for `identity` because it's special one... again...)

Little detail about thos endpoints :  

### Attested

Kind of hard to explains, but it verifies that the data is coming from Azure.  
It also can be useful to see as when you uncypher the PKCS17 you can loot some info on current machine (anonymized example bellow): 
```
cat signature | base64 -d | strings | head -n1
@{"licenseType":"Windows_Client","nonce":"20260925-084217","plan":{"name":"","product":"","publisher":""},"sku":"win11-25h2-pro","subscriptionId":"dfee8600-0000-1111-ae65-d00dd0dd0dd0",
"timeStamp":{"createdOn":"09/25/26 02:42:17 -0000","expiresOn":"09/25/26 08:42:17 -0000"},"vmId":"4549e797-1111-0000-2222-2e6a2fa3d6f6"}
```

### Identity

The most tricky one... #TODO (even doc is hard to find as it's splitted on many many pages)

### Instance

Contains a LOT of information about the current instance

### Loadbalancer

It contains information about the loadbalancer (public IP is a hell of interesting one 🫠)  

### Scheduledevents

Can see & also potentially manage some scheduled events on the machine.

### Versions

Return a list of supported API version.  
But honestly, dont rely on it as it will sort out all versions mixed up together...  
For example you will retrieve api-version available for every endpoints but you wont be able to determine if a specific version is available for loadbalancer and for instance  


## Generate templates (TODO)

There is a folder `templates/` that contains jinja files (empty for now). The idea behind is to generate a script in powershell or bash (depending on the VM OS you are running on) to interrogate easily the maximum of IMDS endpoints.  
Templates are good because as versions evolves, I want python to interrogate Microsoft online versions before so we always be up to date. 😉  
Also, as there are some flaws on specific versions, I would like to have the opportunity to BF IMDS endpoints on possibly every api-version.  


