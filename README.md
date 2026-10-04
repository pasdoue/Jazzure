## General

This tool is built to facilitate Azure/Entra environment discovery.  
The philosophy of the tool is same as [Jawsome](https://github.com/pasdoue/Jawsome) (developped to brute force IAM permissions in AWS)    
But due to complexity of Microsoft, this project is more complex to answer multiple problems and contains multiple submodules that works together.  

## Installation

### Pypi

Perform git clone for now... I will release first package on Pypi when the tool will be "really" functional 😉  

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

This tool is under heavy construction and documentation will follow.  
Also as there are many things to handle, I decided to split documentation across modules/packages to avoid an unreadable README 🤪  

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

This way of handling Microsoft features like I did for Jawsome was aborted, but left dead code as a reminder  
More details here : [Python SDK details](jazzure/python_sdk/README.md)

#### az CLI

As the SDK is not suitable for performing introspection, I turned to azure CLI parsing.  
Actually script take between 40min to 1h to parse all azure CLI options to generate JSON to be faster next times.
More details here : [Azure CLI details](jazzure/az_cli/README.md)

#### Powershell handler

As a lot of commands & Entra connections are well handled in PowerShell and not in python SDK or even Azure CLI, it was necessary to support PowerShell ecosystem.  
More details over here : [PowerShell details](jazzure/powershell/README.md)  

#### IMDS / Managed Identity

This section is about when you're logged into a VM, so you can interrogate IMDS on `http://169.254.169.254/metadata`.    
More details over here : [IMDS details](jazzure/imds/README.md)



