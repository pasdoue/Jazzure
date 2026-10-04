# General info

The interesting way of handling python SDK was to reproduce the previous work of Jawsome and avoid (maybe) tremendous work... Even if I had little hope on subject. 🙃  
Contrary to AWS where there is only boto3 SDK for python, Microsoft changed its strategy and developed an SDK for each service...  
Unfortunately all SDK are not compatible each others due to dependency problem... 💣  
So the idea of using them has been aborted and few code remains and the rest went to trash

Also (as a bonus) when I was testing import of python SDK, some of them are deprecated but not archived, so error like this arrived from time to time : 
```
The complete list of available packages can be found at:
https://aka.ms/azsdk/python/all

Kind of shit you will encounter as error message : 
Starting with v0.37.0, the 'azure-storage' meta-package is deprecated and cannot be installed anymore.
Please install the service specific packages prefixed by `azure` needed for your application.
```

# Technical info

All python SDK are listed over there : https://pypi.org/user/azure-sdk/  
That why I developped the class `pypi_manager.Pypi_Crawler`

