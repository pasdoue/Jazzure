## General

This tool is built to facilitate Azure/Entra environment discovery.  
The philosophy of the tool is same as Jaws : https://github.com/pasdoue/JAWS

## Installation

### Pypi

```bash
pipx install jazzure
```
Then just call : ```jazzure -h```

### Local run

```bash
git clone https://github.com/pasdoue/Jazzure.git
python jazzure.py -h
```


## Technical details

### Azure & Entra details

As there are several ways to connect to those environments, here is a "little" summarize : 

| Method                                       | Identity                           |    User interaction        | Used with                       |
| -------------------------------------------- | ---------------------------------- | -------------------------: | ------------------------------- |
| **Interactive / Browser**                    | User                               |                        Yes | `az`, PowerShell, Graph         |
| **Device Code**                              | User                               | Using web browser first    | `az`, Graph PowerShell, MSAL    |
| **Authorization Code + PKCE**                | User                               |                        Yes | Web/Desktop/SPA                 |
| **Access Token existant**                    | User ou App                        |                        No  | `curl`, REST, PowerShell        |
| **Client Secret**                            | Application                        |                        No  | `curl`, MSAL, scripts           |
| **Certificate**                              | Application                        |                        No  | PowerShell, MSAL, automation    |
| **Managed Identity**                         | Azure Resource / Service Principal |                        No  | VM, App Service, Function, etc. |
| **Workload Identity / Federated Credential** | Workload                           |                        No  | CI/CD, Kubernetes, GitHub, etc. |
| **OBO**                                      | User → Application → API           | No after first login       | APIs intermédiaires             |


### Jazzure details

#### Python Microsoft SDK

Contrary to AWS where there is only boto3 SDK for python, Microsoft changed its strategy and developed an SDK for each service...  
Unfortunately all SDK are not compatible each others due to dependency problem...  
So the idea of using them has been aborted and the code I did to test it also went to trash

```
The complete list of available packages can be found at:
https://aka.ms/azsdk/python/all

Kind of shit you will encounter as error message : 
Starting with v0.37.0, the 'azure-storage' meta-package is deprecated and cannot be installed anymore.
Please install the service specific packages prefixed by `azure` needed for your application.
```

#### az CLI

As the SDK is not suitable for performing introspection, I turned to azure CLI parsing.  
Actually script take between 40min to 1h to parse all azure CLI options to generate JSON to be faster next times.


#### IMDS / Managed Identity

When you're logged into a VM, you can interrogate IMDS on `http://169.254.169.254/metadata`.  
The bottleneck is that there are several endpoints to retrieve metadata, and they depend on an `api-version` which are specific dates and updated sometimes.

Bellow the summary, but for curious one's check every endpoint details here : https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service?tabs=linux#endpoint-categories 

| Category root               | Description                                      | Version introduced |
|-----------------------------|--------------------------------------------------|--------------------|
| `/metadata/attested`        | Attested Data                                    | 2018-10-01         |
| `/metadata/identity`        | Managed Identity via IMDS                        | 2018-02-01         |
| `/metadata/instance`        | Instance Metadata                                | 2017-04-02         |
| `/metadata/loadbalancer`    | Retrieve Load Balancer metadata via IMDS         | 2020-10-01         |
| `/metadata/scheduledevents` | Scheduled Events via IMDS                        | 2017-08-01         |
| `/metadata/versions`        | Versions                                         | N/A                |

As IMDS cannot be interrogated from outside the VM, Jazzure has a code `imds/imds.py` which navigate through Microsoft doc and retrieve all api-versions for you.  
Once done, it allows you to craft script to interrogate (by default) latest release version, but you can specify to target them all.

TODO : Harder part is handling /identity





