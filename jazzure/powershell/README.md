# General information

I was performing some HTB cloud labs and (unfortunately), powershell is kind of needed when performing Microsoft security assessment.  
This module answer this problem by managing a Docker image with .NET8 and some necessary PowerShell modules.  
  
> Side note : inside exegol there is already a powershell console, but running in .NET7 and some features were not available 🥲
That's why I created this python docker manager. Also as it build and spawn a docker, you have to run it on your host (bye bye dind)

# Technical information

Python code that manages docker installation and running commands is here : `jazzure/powershell/pwsh_manager.py`  
The Dockerfile it manages : `jazzure/powershell/Dockerfile`

## Installed modules

At this point the following PowerShell modules are installed : 
- Az
- AADInternals
- AADInternals-Endpoints
- Microsoft.Entra
- Microsoft.Graph

## Powershell session handler

Little tricky thing was not about building and spawning docker but to create a handler that will keep a "context" each time you run powershell command.  
Indeed when you connect to container and launch a pwsh, each call will create a new session, and therefore you will lose your connection session to Entra or Azure... 😰  
So I manage to create a function `PowerShellContainer._start_persistent_powershell()` that will handle that for you.  
Also the container stays alive while your using it, and remove running instance only when you finish 🎉  

### Powershell session handler examples & usages

1. Simple commands

```python
from jazzure.powershell.pwsh_manager import PowerShellContainer
pwsh_container = PowerShellContainer()

try:
    print(pwsh_container.run("Get-Date"))
    print(pwsh_container.run("Import-Module -Name AADInternals"))
    print(pwsh_container.run("Get-AADIntTenantID -Domain domain.com")) #this will work (and does not trigger error) as session is the same as upper Import-Module 😉
finally:
    pwsh_container.stop()
```

2. Long command

```python
from jazzure.powershell.pwsh_manager import PowerShellContainer
pwsh_container = PowerShellContainer()

try:
    # using python vars
    username = "john@example.com"
    command = f'''
            $user = "{username}"
            Write-Output "User: $user"
            '''
    print(pwsh_container.run(command))
finally:
    pwsh_container.stop()
```

3. Handling env vars

```python
from jazzure.powershell.pwsh_manager import PowerShellContainer
pwsh_container = PowerShellContainer()

try:
    # passing env vars
    print(pwsh_container.run('$env:MY_VALUE', env_vars={"MY_VALUE": "some value from Python"}))
finally:
    pwsh_container.stop()
```


