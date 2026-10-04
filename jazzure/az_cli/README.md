# General information

As python SDK is not suitable for Azure environment actions discovery, I decided to parse Azure CLI which is quite well when using CLI (but can trigger headache to parse it 😅)  
The idea is to map every service and functions/actions we can interrogate to perform some upper discovery logic. 

# Technical information

## AZ CLI versions

There are several version of this tool and some older ones can reveal more information.  
So there is a function `azcli.AzCLI.retrieve_online_versions()` that can list every documented versions.  
This is not used yet in the tool but in the future I will try to handle them.  

## AZ CLI crawler

The recon of all `az` has been done in version `2.90.0`.  
The class `azcli.AzureCliCrawler` handles the parsing of `az`. It's quite long as we need to parse recursively all CLI possibilities with the `--help` arg.  
The function `crawl()` is the main entrance of parsing and added some asyncio strategy to avoid long time running, even though it takes about 40min to complete 😅  
A file in JSON format is created and contains every mapping of `az` commands with all information (see bellow a little extract):  
```json
{ "command": "az rest",
      "subgroups": [],
      "commands": [],
      "arguments": [
        {
          "name": "--uri",
          "aliases": [
            "--url",
            "-u"
          ],
          "required": true,
          "special_mode": "",
          "description": "Request URL. If it doesn't start with a host, CLI assumes it as an Azure resource ID and prefixes it with the ARM endpoint of the current cloud shown by `az cloud show --query endpoints.resourceManager`. Common token {subscriptionId} will be replaced with the current subscription ID specified by `az account set`."
        },
        {
          "name": "--body",
          "aliases": [
            "-b"
          ],
          "required": false,
          "special_mode": "",
          "description": "Request body. Use @{file} to load from a file. For quoting issues in different terminals, see https://github.com/Azure/azure- cli/blob/dev/doc/use_cli_effectively.md#quoting-issues."
        }
        ]
}
```

Technical bonus detail :  
- While parsing the output I discovered that ANSI chars were dropped randomly in some help and caused my parsing to fails for no reason...
- As it was quite painful some unit tests have been written to ensure good parsing of `az` inside `tests/test_AZCLI.py`





