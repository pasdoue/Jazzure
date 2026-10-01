from unittest import TestCase

from jazzure.az_cli import azcli

class TestAZCLI(TestCase):

    def test_retrieve_online_versions(self):
        actual_versions = ['2.90.0', '2.89.1', '2.89.0', '2.88.0', '2.87.0', '2.86.0', '2.85.0', '2.84.0', '2.83.0', '2.82.0', '2.81.0', '2.80.0', '2.79.0', '2.78.0', '2.77.0', '2.76.0', '2.75.0', '2.74.0', '2.73.0', '2.72.0', '2.71.0', '2.70.0', '2.69.0', '2.68.0', '2.67.0', '2.66.0', '2.65.0', '2.64.0', '2.63.0', '2.62.0', '2.61.0', '2.60.0', '2.59.0', '2.58.0', '2.57.0', '2.56.0', '2.55.0', '2.54.0', '2.53.1', '2.53.0', '2.52.0', '2.51.0', '2.50.0', '2.49.0', '2.48.1', '2.48.0', '2.47.0', '2.46.0', '2.45.0', '2.44.1', '2.44.0', '2.43.0', '2.42.0', '2.41.0', '2.40.0', '2.39.0', '2.38.2', '2.38.1', '2.38.0', '2.37.0', '2.36.0', '2.35.0', '2.34.1', '2.34.0', '2.33.1', '2.33.0', '2.32.0', '2.31.0', '2.30.0', '2.29.2', '2.29.1', '2.29.0', '2.28.1', '2.28.0', '2.27.2', '2.27.1', '2.27.0', '2.26.1', '2.26.0', '2.25.0', '2.24.2', '2.24.1', '2.24.0', '2.23.0', '2.22.1', '2.22.0', '2.21.0', '2.20.0', '2.19.1', '2.19.0', '2.18.0', '2.17.1', '2.17.0', '2.16.0', '2.15.1', '2.15.0', '2.14.2', '2.14.1', '2.14.0', '2.13.0', '2.12.1', '2.12.0', '2.11.1', '2.11.0', '2.10.1', '2.10.0', '2.9.1', '2.9.0', '2.8.0', '2.7.0', '2.6.0', '2.5.1', '2.5.0', '2.4.0', '2.3.1', '2.3.0', '2.2.0', '2.1.0', '2.0.81', '2.0.80', '2.0.79', '2.0.77', '2.0.76', '2.0.75', '2.0.74', '2.0.72', '2.0.71', '2.0.70', '2.0.69', '2.0.68', '2.0.67', '2.0.66', '2.0.65', '2.0.64', '2.0.63', '2.0.60', '2.0.59', '2.0.58', '2.0.57', '2.0.56', '2.0.55', '2.0.54', '2.0.53', '2.0.52', '2.0.51', '2.0.50', '2.0.49', '2.0.48', '2.0.47', '2.0.46', '2.0.45', '2.0.44', '2.0.43', '2.0.42', '2.0.39', '2.0.38', '2.0.33', '2.0.32', '2.0.31', '2.0.30', '2.0.29', '2.0.28', '2.0.27', '2.0.26', '2.0.25', '2.0.23', '2.0.22', '2.0.21', '2.0.20', '2.0.19', '2.0.18', '2.0.17', '2.0.16', '2.0.15', '2.0.14', '2.0.13', '2.0.12', '2.0.6', '2.0.2', '2.0.0']

        online_version = azcli.AzCLI.retrieve_online_versions()
        self.assertTrue(set(actual_versions).issubset(set(online_version)))

class TestAzureCliCrawler(TestCase):

    def setUp(self) -> None:
        self.az_help = """
Group
    az

Subgroups:
    account
    acr
    ad
    advisor
    aks
    ams
    apim
    appconfig
    appservice
    aro
    backup
    batch
    batchai
    bicep
    billing
    bot
    cache
    capacity
    cloud
    cognitiveservices
    compute-fleet
    compute-recommender
    config
    connection
    consumption
    container
    containerapp
    cosmosdb
    data-boundary
    databoxedge
    deployment
    deployment-scripts
    disk
    disk-access
    disk-encryption-set
    dls
    dms
    eventgrid
    eventhubs
    extension
    feature
    functionapp
    group
    hdinsight
    identity
    image
    iot
    keyvault
    lab
    lock
    logicapp
    managed-cassandra
    managedapp
    managedservices
    maps
    mariadb
    monitor
    mysql
    netappfiles
    network
    policy
    postgres
    ppg
    private-link
    provider
    redis
    relay
    resource
    resourcemanagement
    restore-point
    role
    search
    security
    servicebus
    sf
    sig
    signalr
    snapshot
    sql
    sshkey
    stack
    stack-whatif
    staticwebapp
    storage
    synapse
    tag
    term
    ts
    vm
    vmss
    webapp

Commands:
    configure
    feedback
    find                : Entry point for `az find`.
    interactive
    login               : Log in to access Azure subscriptions.
    logout              : Log out to remove access to Azure subscriptions.
    rest
    self-test
    survey
    upgrade
    version

"""
        self.az_keyvault_help = """
Group
    az keyvault : Manage KeyVault keys, secrets, and certificates.

Subgroups:
    backup                      : Manage full HSM backup.
    certificate                 : Manage certificates.
    ekm-connection    [Preview] : Manage External Key Manager (EKM) connection for a
                                  Managed HSM.
    key                         : Manage keys.
    network-rule                : Manage network ACLs for vault or managed hsm.
    private-endpoint-connection : Manage vault/HSM private endpoint connections.
    private-link-resource       : Manage vault/HSM private link resources.
    region                      : Manage MHSM multi-regions.
    restore                     : Manage full HSM restore.
    role                        : Manage user roles for access control.
    secret                      : Manage secrets.
    security-domain             : Manage security domain operations.
    setting                     : Manage MHSM settings.

Commands:
    check-name                  : Check that the given name is valid and is not already in use.
    create                      : Create a Vault or HSM.
    delete                      : Delete a Vault or HSM.
    delete-policy               : Delete security policy settings for a Key Vault.
    list                        : List Vaults and/or HSMs.
    list-deleted                : Get information about the deleted Vaults or HSMs in a
                                  subscription.
    purge                       : Permanently delete the specified Vault or HSM. Aka Purges the
                                  deleted Vault or HSM.
    recover                     : Recover a Vault or HSM.
    set-policy                  : Update security policy settings for a Key Vault.
    show                        : Show details of a Vault or HSM.
    show-deleted                : Show details of a deleted Vault or HSM.
    update                      : Update the properties of a Vault.
    update-hsm                  : Update the properties of a HSM.
    wait                        : Place the CLI in a waiting state until a condition of the Vault is
                                  met.
    wait-hsm                    : Place the CLI in a waiting state until a condition of the HSM is
                                  met.

"""
        self.az_keyvault_key_help = """
Group
    az keyvault key : Manage keys.

Subgroups:
    rotation-policy               : Manage key's rotation policy.

Commands:
    backup                        : Request that a backup of the specified key be downloaded to the
                                    client.
    create                        : Create a new key, stores it, then returns key parameters and
                                    attributes to the client.
    decrypt             [Preview] : Decrypt a single block of encrypted data.
    delete                        : Delete a key of any type from storage in Vault or HSM.
    download                      : Download the public part of a stored key.
    encrypt             [Preview] : Encrypt an arbitrary sequence of bytes using an
                                    encryption key that is stored in a Vault or HSM.
    get-attestation               : Get a key's attestation blob.
    get-policy-template [Preview] : Return policy template as JSON encoded policy
                                    definition.
    import                        : Import a private key.
    list                          : List keys in the specified Vault or HSM.
    list-deleted                  : List the deleted keys in the specified Vault or HSM.
    list-versions                 : List the identifiers and properties of a key's versions.
    purge                         : Permanently delete the specified key.
    random                        : Get the requested number of random bytes from a managed HSM.
    recover                       : Recover the deleted key to its latest version.
    restore                       : Restore a backed up key to a Vault or HSM.
    rotate                        : Rotate the key based on the key policy by generating a new
                                    version of the key.
    set-attributes                : The update key operation changes specified attributes of a
                                    stored key and can be applied to any key type and key version
                                    stored in Vault or HSM.
    show                          : Get a key's attributes and, if it's an asymmetric key, its
                                    public material.
    show-deleted                  : Get the public part of a deleted key.
    sign                          : Create a signature from a digest using a key that is stored in a
                                    Vault or HSM.
    verify                        : Verify a signature using the key that is stored in a Vault or
                                    HSM.

"""
        self.az_keyvault_key_create_help = """
Command
    az keyvault key create : Create a new key, stores it, then returns key parameters and attributes
    to the client.
        The create key operation can be used to create any key type in Vault or HSM. If the named
        key already exists, Vault or HSM creates a new version of the key. It requires the
        keys/create permission.

Arguments
    --curve                                        : Elliptic curve name. For valid values, see:
                                                     https://learn.microsoft.com/rest/api/keyvault/k
                                                     eys/create-key/create-key#jsonwebkeycurvename.
                                                     Allowed values: P-256, P-256K, P-384, P-521.
    --default-cvm-policy                           : Use default policy under which the key can be
                                                     exported for CVM disk encryption.
    --default-data-disk-policy --default-dd-policy : Use default policy under which the key can be
                                                     exported for data disk encryption.
    --disabled                                     : Create key in disabled state.  Allowed values:
                                                     false, true.
    --expires                                      : Expiration UTC datetime  (Y-m-d'T'H:M:S'Z').
    --exportable                                   : Whether the private key can be exported. To
                                                     create key with release policy, "exportable"
                                                     must be true and caller must have "export"
                                                     permission.  Allowed values: false, true.
    --immutable                                    : Mark a release policy as immutable. An
                                                     immutable release policy cannot be changed or
                                                     updated after being marked immutable. Release
                                                     policies are mutable by default.  Allowed
                                                     values: false, true.
    --kty                                          : The type of key to create. For valid values,
                                                     see: https://learn.microsoft.com/rest/api/keyva
                                                     ult/keys/create-key/create-key#jsonwebkeytype.
                                                     Allowed values: EC, EC-HSM, RSA, RSA-HSM, oct,
                                                     oct-HSM.
    --not-before                                   : Key not usable before the provided UTC datetime
                                                     (Y-m-d'T'H:M:S'Z').
    --ops                                          : Space-separated list of permitted JSON web key
                                                     operations.  Allowed values: decrypt, encrypt,
                                                     export, import, sign, unwrapKey, verify,
                                                     wrapKey.
    --policy                                       : The policy rules under which the key can be
                                                     exported. Policy definition as JSON, or a path
                                                     to a file containing JSON policy definition.
    --protection -p                                : Specifies the type of key protection.  Allowed
                                                     values: hsm, software.
    --size                                         : The key size in bits. For example: 2048, 3072,
                                                     or 4096 for RSA. 128, 192, or 256 for oct.
    --tags                                         : Space-separated tags: key[=value] [key[=value]
                                                     ...]. Use '' to clear existing tags.

External Key Arguments
    --external-key-id                    [Preview] : Create an external Managed HSM key
                                                     backed by an External Key Manager (EKM) key id.
        Argument '--external-key-id' is in preview and under development. Reference and support
        levels: https://aka.ms/CLI_refstatus

Global Policy Arguments
    --acquire-policy-token                         : Acquiring an Azure Policy token automatically
                                                     for this resource operation.
    --change-reference                             : The related change reference ID for this
                                                     resource operation.

Id Arguments
    --hsm-name                                     : Name of the HSM. (--hsm-name and --vault-name
                                                     are mutually exclusive, please specify just one
                                                     of them).
    --id                                           : Id of the key. If specified all other 'Id'
                                                     arguments should be omitted.
    --name -n                                      : Name of the key. Required if --id is not
                                                     specified.
    --vault-name                                   : Name of the Vault.

Global Arguments
    --debug                                        : Increase logging verbosity to show all debug
                                                     logs.
    --help -h                                      : Show this help message and exit.
    --only-show-errors                             : Only show errors, suppressing warnings.
    --output -o                                    : Output format.  Allowed values: json, jsonc,
                                                     none, table, tsv, yaml, yamlc.  Default: json.
    --query                                        : JMESPath query string. See http://jmespath.org/
                                                     for more information and examples.
    --subscription                                 : Name or ID of subscription. You can configure
                                                     the default subscription using `az account set
                                                     -s NAME_OR_ID`.
    --verbose                                      : Increase logging verbosity. Use --debug for
                                                     full debug logs.

Examples
    Create a key in a specified Key Vault with a given name. (autogenerated)
        az keyvault key create --vault-name envault -n enkey


"""
        self.az_account_clear_help = """
Command
    az account clear : Clear all subscriptions from the CLI's local cache.
        To clear the current subscription, use 'az logout'.

Arguments

Global Policy Arguments
    --acquire-policy-token : Acquiring an Azure Policy token automatically for this resource
                             operation.
    --change-reference     : The related change reference ID for this resource operation.

Global Arguments
    --debug                : Increase logging verbosity to show all debug logs.
    --help -h              : Show this help message and exit.
    --only-show-errors     : Only show errors, suppressing warnings.
    --output -o            : Output format.  Allowed values: json, jsonc, none, table, tsv, yaml,
                             yamlc.  Default: json.
    --query                : JMESPath query string. See http://jmespath.org/ for more information
                             and examples.
    --verbose              : Increase logging verbosity. Use --debug for full debug logs.
"""
        self.as_redis_create_help = """
Command
    az redis create : Create new Redis Cache instance.

Arguments
    --location -l                     [Required] : Location. Values from: `az account list-
                                                   locations`. You can configure the default
                                                   location using `az configure --defaults
                                                   location=<location>`.
    --name -n                         [Required] : Name of the Redis cache.
    --resource-group -g               [Required] : Name of resource group. You can configure the
                                                   default group using `az configure --defaults
                                                   group=<name>`.
    --sku                             [Required] : Type of Redis cache.  Allowed values: Basic,
                                                   Premium, Standard.
    --vm-size                         [Required] : Size of Redis cache to deploy. Basic and Standard
                                                   Cache sizes start with C. Premium Cache sizes
                                                   start with P.  Allowed values: c0, c1, c2, c3,
                                                   c4, c5, c6, p1, p2, p3, p4, p5.
    --disable-access-keys                        : Authentication to Redis through access keys is
                                                   disabled when set as true.  Allowed values:
                                                   false, true.
    --enable-non-ssl-port                        : If specified, then the non-ssl redis server port
                                                   (6379) will be enabled.
    --mi-system-assigned                         : Flag to specify system assigned identity.
    --mi-user-assigned                           : One or more space separated resource IDs of user
                                                   assigned identities.
    --minimum-tls-version                        : Specifies the TLS version required by clients to
                                                   connect to cache.  Allowed values: 1.0, 1.1, 1.2.
    --redis-configuration                        : A json file used to set redis-configuration
                                                   settings. You may encounter parse errors if the
                                                   json file is invalid.
        Usage: --redis-configuration @"{config_file.json}"

        An example json file for configuring max-memory policies
        [
          {
            "maxmemory-policy": "allkeys-lru"
          }
        ]

        An example json file for enabling the RDB back up data persistence is
        [
          {
            "rdb-storage-connection-string": "DefaultEndpointsProtocol=https;AccountName=mystorageac
        count;AccountKey=myAccountKey;EndpointSuffix=core.windows.net",
            "rdb-backup-enabled": "true",
            "rdb-backup-frequency": "15",
            "rdb-backup-max-snapshot-count": "1"
          }
        ]

        An example json file for enabling the AOF back up data persistence is
        [
          {
            "aof-backup-enabled": "true",
            "aof-storage-connection-string-0": "DefaultEndpointsProtocol=https;AccountName=mystorage
        account;AccountKey=myAccountKey;EndpointSuffix=core.windows.net",
            "aof-storage-connection-string-1": "DefaultEndpointsProtocol=https;AccountName=mystorage
        account;AccountKey=myAccountKey;EndpointSuffix=core.windows.net"
          }
        ]

        The content for a json file for configuring Microsoft Entra Authentication is
        {
        "aad-enabled": "true",
        }.
    --redis-version                              : Redis version. This should be in the form
                                                   'major[.minor]' (only 'major' is required) or the
                                                   value 'latest' which refers to the latest stable
                                                   Redis version that is available. Supported
                                                   versions: 4.0, 6.0 (latest). Default value is
                                                   'latest'.
    --replicas-per-master                        : The number of replicas to be created per master.
    --shard-count                                : The number of shards to be created on a Premium
                                                   Cluster Cache.
    --static-ip                                  : Specify a static ip if required for the VNET. If
                                                   you do not specify a static IP then an IP address
                                                   is chosen automatically.
    --subnet-id                                  : The full resource ID of a subnet in a virtual
                                                   network to deploy the redis cache in. Example
                                                   format /subscriptions/{subid}/resourceGroups/{res
                                                   ourceGroupName}/providers/Microsoft.{Network|Clas
                                                   sicNetwork}/virtualNetworks/vnet1/subnets/subnet1
                                                   .
    --tags                                       : Space-separated tags: key[=value] [key[=value]
                                                   ...]. Use '' to clear existing tags.
    --tenant-settings                            : Space-separated tenant settings in key[=value]
                                                   format.
    --update-channel                             : Specifies the update channel for the monthly
                                                   Redis updates your Redis Cache will receive.
                                                   Caches using "Preview" update channel get latest
                                                   Redis updates at least 4 weeks ahead of "Stable"
                                                   channel caches. Default value is "Stable".
                                                   Allowed values: Preview, Stable.
    --zonal-allocation --zonal-allocation-policy : Specifies how availability zones are allocated to
                                                   the Redis cache. "Automatic" enables zone
                                                   redundancy and Azure will automatically select
                                                   zones based on regional availability and
                                                   capacity. "UserDefined" will select availability
                                                   zones passed in by you using the "zones"
                                                   parameter. "NoZones" will produce a non-zonal
                                                   cache. If "zonal-allocation-policy" is not
                                                   passed, it will be set to "UserDefined" when
                                                   zones are passed in, otherwise, it will be set to
                                                   "Automatic in regions where zones are supported
                                                   and "NoZones" in regions where zones are not
                                                   supported.  Allowed values: Automatic, NoZones,
                                                   UserDefined.
    --zones -z                                   : Space-separated list of availability zones into
                                                   which to provision the resource.

Global Policy Arguments
    --acquire-policy-token                       : Acquiring an Azure Policy token automatically for
                                                   this resource operation.
    --change-reference                           : The related change reference ID for this resource
                                                   operation.

Global Arguments
    --debug                                      : Increase logging verbosity to show all debug
                                                   logs.
    --help -h                                    : Show this help message and exit.
    --only-show-errors                           : Only show errors, suppressing warnings.
    --output -o                                  : Output format.  Allowed values: json, jsonc,
                                                   none, table, tsv, yaml, yamlc.  Default: json.
    --query                                      : JMESPath query string. See http://jmespath.org/
                                                   for more information and examples.
    --subscription                               : Name or ID of subscription. You can configure the
                                                   default subscription using `az account set -s
                                                   NAME_OR_ID`.
    --verbose                                    : Increase logging verbosity. Use --debug for full
                                                   debug logs.

Examples
    Create new Redis Cache instance. (autogenerated)
        az redis create --location westus2 --name MyRedisCache --resource-group MyResourceGroup
        --sku Basic --vm-size c0

    Configure the multiple zones for new Premium Azure Cache for Redis
        az redis create --location westus2 --name MyRedisCache --resource-group MyResourceGroup
        --sku Premium --vm-size p1 --zones 1 2

    Deploying a Premium Azure Cache for Redis with zones automatically allocated
        az redis create --location westus2 --name MyRedisCache --resource-group MyResourceGroup
        --sku Premium --vm-size p1 --zonal-allocation-policy Automatic

    Configure the memory policies for the cache.
        az redis create --resource-group resourceGroupName --name cacheName --location westus2 --sku
        Standard --vm-size c0 --redis-configuration @"config_max-memory.json"

    Configure and enable the RDB back up data persistence for new Premium Azure Cache for Redis.
        az redis create --location westus2 --name MyRedisCache --resource-group MyResourceGroup
        --sku Premium --vm-size p1 --redis-configuration @"config_rdb.json"

    Configure and enable the AOF back up data persistence for new Premium Azure Cache for Redis
        az redis create --location westus2 --name MyRedisCache --resource-group MyResourceGroup
        --sku Premium --vm-size p1 --redis-configuration @"config_aof.json"

    Create a Premium Azure Cache for Redis with clustering enabled
        az redis create --location westus2 --name MyRedisCache --resource-group MyResourceGroup
        --sku Premium --vm-size p1 --shard-count 2

    Deploying a Premium Azure Cache for Redis inside an existing Azure Virtual Network
        az redis create --location westus2 --name MyRedisCache --resource-group MyResourceGroup
        --sku Premium --vm-size p1 --subnet-id "/subscriptions/{subid}/resourceGroups/{resourceGroup
        Name}/providers/Microsoft.{Network|ClassicNetwork}/virtualNetworks/vnet1/subnets/subnet1"

    Deploying a Premium Azure Cache for Redis with Microsoft Entra Authentication configured and
    access keys disabled
        az redis create --location westus2 --name MyRedisCache --resource-group MyResourceGroup
        --sku Premium --vm-size p1 --disable-access-keys true --redis-configuration @"config_enable-
        aad.json"
"""
        self.az_storage_account_migration = """
Group
    az storage account migration : Manage Storage Account Migration.

Commands:
    show  [Preview] : Get the status of the ongoing migration for the specified storage account.
    start           : Account Migration request can be triggered for a storage account to change its
            redundancy level. The migration updates the non-zonal redundant storage account to a
            zonal redundant account or vice-versa in order to have better reliability and
            availability. Zone-redundant storage (ZRS) replicates your storage account synchronously
            across three Azure availability zones in the primary region.
"""

    def test_get_sections(self):
        az_help_sections = az_keyvault_help_sections = az_keyvault_key_help_sections = ["Group", "Subgroups", "Commands"]

        # az help
        sections = azcli.AzureCliCrawler.get_sections(lines=self.az_help)
        self.assertListEqual(az_help_sections, list(sections.keys()))
        # az keyvault help
        sections = azcli.AzureCliCrawler.get_sections(lines=self.az_keyvault_help)
        self.assertListEqual(az_keyvault_help_sections, list(sections.keys()))
        # az keyvault key help
        sections = azcli.AzureCliCrawler.get_sections(lines=self.az_keyvault_key_help)
        self.assertListEqual(az_keyvault_key_help_sections, list(sections.keys()))
        # az keyvault key create help
        sections = azcli.AzureCliCrawler.get_sections(lines=self.az_keyvault_key_create_help)
        self.assertListEqual(["Command", "Arguments", "External Key Arguments", "Global Policy Arguments", "Id Arguments", "Global Arguments", "Examples"], list(sections.keys()))
        # az account clear
        sections = azcli.AzureCliCrawler.get_sections(lines=self.az_account_clear_help)
        self.assertListEqual(["Command", "Arguments", "Global Policy Arguments", "Global Arguments"], list(sections.keys()))
        # az redis create
        sections = azcli.AzureCliCrawler.get_sections(lines=self.as_redis_create_help)
        self.assertListEqual(["Command", "Arguments", "Global Policy Arguments", "Global Arguments", "Examples"], list(sections.keys()))
        self.assertTrue("--zones -z" in sections.get("Arguments"))

    def test_parse_commands(self):
        # az help
        args_section = azcli.AzureCliCrawler.get_sections(lines=self.az_help)
        args = azcli.AzureCliCrawler.parse_commands(content=args_section.get("Commands", []))
        self.assertListEqual(args, ["configure", "feedback", "find", "interactive", "login", "logout", "rest", "self-test", "survey", "upgrade", "version"])

        # az storage account migration help
        args_section = azcli.AzureCliCrawler.get_sections(lines=self.az_storage_account_migration)
        args = azcli.AzureCliCrawler.parse_commands(content=args_section.get("Commands", []))
        self.assertListEqual(args, ["show", "start"])


    def test_parse_args(self):
        # az keyvault key create help
        args_section = azcli.AzureCliCrawler.get_sections(lines=self.az_keyvault_key_create_help)
        args = azcli.AzureCliCrawler.parse_arguments(content=args_section.get("Arguments", []))
        self.assertListEqual([x.get("name") for x in args], [ "--curve", "--default-cvm-policy", "--default-data-disk-policy", "--disabled", "--expires", "--exportable", "--immutable", "--kty", "--not-before", "--ops", "--policy", "--protection", "--size", "--tags" ])

        args = azcli.AzureCliCrawler.parse_arguments(content=args_section.get("External Key Arguments", []))
        self.assertListEqual([x.get("name") for x in args], ["--external-key-id"])

        args = azcli.AzureCliCrawler.parse_arguments(content=args_section.get("Global Policy Arguments", []))
        self.assertListEqual([x.get("name") for x in args], ["--acquire-policy-token", "--change-reference"])

        args = azcli.AzureCliCrawler.parse_arguments(content=args_section.get("Id Arguments", []))
        self.assertListEqual([x.get("name") for x in args], ["--hsm-name", "--id", "--name", "--vault-name"])

        args = azcli.AzureCliCrawler.parse_arguments(content=args_section.get("Global Arguments", []))
        self.assertListEqual([x.get("name") for x in args], ["--debug", "--help", "--only-show-errors", "--output", "--query", "--subscription", "--verbose" ])

        # az account clear
        args_section = azcli.AzureCliCrawler.get_sections(lines=self.az_account_clear_help)
        args = azcli.AzureCliCrawler.parse_arguments(content=args_section.get("Arguments", []))
        self.assertListEqual([x.get("name") for x in args], [])

        args = azcli.AzureCliCrawler.parse_arguments(content=args_section.get("Global Policy Arguments", []))
        self.assertListEqual([x.get("name") for x in args], ["--acquire-policy-token", "--change-reference"])

        # az redis create
        args_section = azcli.AzureCliCrawler.get_sections(lines=self.as_redis_create_help)
        args = azcli.AzureCliCrawler.parse_arguments(content=args_section.get("Arguments", []))

        self.assertListEqual([x.get("name") for x in args], ["--location", "--name", "--resource-group", "--sku", "--vm-size", "--disable-access-keys", "--enable-non-ssl-port",
                                                           "--mi-system-assigned", "--mi-user-assigned", "--minimum-tls-version", "--redis-configuration", "--redis-version", "--replicas-per-master", "--shard-count", "--static-ip", "--subnet-id", "--tags", "--tenant-settings", "--update-channel", "--zonal-allocation", "--zones"])



