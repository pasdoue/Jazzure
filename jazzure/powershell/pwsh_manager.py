from pathlib import Path
from typing import Union

from R2Log import logger
import docker
from docker.models.containers import Container
from docker.models.images import Image
from docker.client import DockerClient

from jazzure.utils import binary_installed


class PowerShellContainer:

    DOCKER_IMAGE_NAME = "jazzure-powershell"
    DOCKER_TAG = "latest"

    def __init__(self):
        """
            Class to handle the build & run of a docker container which will contains .NET8 and some modules to perform Azure & Entra recon
            List of modules :
            - Az
            - AADInternals
            - AADInternals-Endpoints
            - Microsoft.Entra
            - Microsoft.Graph
        """
        self.client = None
        self.image = None
        self.container = None
        self._docker_runtime_name = f"{self.DOCKER_IMAGE_NAME}-runtime"
        if not binary_installed(binary_name="docker"):
            logger.warning(f"To use powershell feature, please install docker")
            return
        self.client = self._create_docker_client()
        if self.client is None:
            return

        self.image = self.get_docker_image(dokcer_client=self.client, image_name=self.DOCKER_IMAGE_NAME, tag=self.DOCKER_TAG)
        if self.image is None :
            self.image = self.build_container(docker_client=self.client, dockerfile_path=Path(__file__).parent, image_name=self.DOCKER_IMAGE_NAME, tag=self.DOCKER_TAG)
            if self.image is None:
                raise RuntimeError(f"Unable to build docker image")
        self.container = self._create_container()

    @staticmethod
    def _create_docker_client() -> Union[None|DockerClient]:
        """
            Perform connection to docker socket & API
        """
        try:
            client = docker.from_env()
            # Force a connection test.
            client.ping()
            logger.success("Successfully connected to Docker")
            return client
        except docker.errors.DockerException as e:
            if "Permission denied" in str(e):
                logger.error("You dont have permission to perform docker actions with your user")
            else:
                logger.error(f"Unable to connect to Docker:\n{e}")
        return None

    @staticmethod
    def get_docker_image(dokcer_client, image_name: str, tag: str) -> Union[None|Image]:
        try:
            image = dokcer_client.images.get(name=f"{image_name}:{tag}")
            return image
        except docker.errors.ImageNotFound:
            logger.warning("Docker image does not exist")
        return None

    @staticmethod
    def build_container(docker_client, dockerfile_path: Union[str|Path], image_name: str, tag: str) -> Union[None|Image]:
        """
            Handling container build based on Dockerfile
        """
        dockerfile_path = Path(dockerfile_path).resolve() if isinstance(dockerfile_path, str) else dockerfile_path
        if not dockerfile_path.is_dir():
            raise ValueError(f"Docker build context is not a directory : {dockerfile_path}")

        logger.info(f"Launching build of docker container {image_name} with Dockerfile : {dockerfile_path}")
        try:
            # dokcer_client.images.build(path=str(dockerfile_path), tag=f"{image_name}:latest", rm=True)
            resp = docker_client.api.build(path=str(dockerfile_path), tag=f"{image_name}:{tag}", rm=True, decode=True)
            for chunk in resp:
                if "stream" in chunk:
                    print(chunk["stream"], end="", flush=True)
                elif "status" in chunk:
                    print(chunk["status"], flush=True)
                elif "error" in chunk:
                    print(f"\nERROR: {chunk['error']}", flush=True)
                    raise RuntimeError(chunk["error"])

            image = PowerShellContainer.get_docker_image(dokcer_client=docker_client, image_name=image_name, tag=tag)
            if image is not None:
                logger.success(f"Image build successfull !")
                logger.info(f"Image ID: {image.id}")
                logger.info(f"Tags: {image.tags}")
                return image
        except Exception as e:
            logger.error(f"Unable to build container for unknown reason : \n{str(e)}")
        return None

    def _create_container(self) -> Container:
        """
            Create a persistent PowerShell container.
            The container is kept alive so exec_run() can be used multiple times.
        """
        logger.info(f"Creating PowerShell container '{self._docker_runtime_name}'")
        try:
            container = self.client.containers.run(
                image=f"{self.DOCKER_IMAGE_NAME}:{self.DOCKER_TAG}",
                command=[ "pwsh", "-NoLogo", "-NoProfile", "-Command", "while ($true) { Start-Sleep -Seconds 3600 }" ],
                name=self._docker_runtime_name,
                detach=True,
                remove=False,
            )
            logger.success(f"Container started: {container.id}")
            return container
        except docker.errors.APIError as e:
            logger.error(f"Unable to start PowerShell container:\n{e}")
            raise

    def run(self, command: str, env_vars: Union[None|dict] = None) -> str:
        """
            Execute a PowerShell command inside the running container.
        """
        if not command:
            raise ValueError("PowerShell command cannot be empty")

        # Refresh container state from Docker.
        self.container.reload()
        if self.container.status != "running":
            raise RuntimeError(f"PowerShell container is not running (status: {self.container.status})")

        logger.debug(f"Executing PowerShell command:\n{command}")

        try:
            if env_vars is not None:
                result = self.container.exec_run( [ "pwsh", "-NoLogo", "-NoProfile", "-Command", command ], environment=env_vars )
            else:
                result = self.container.exec_run(["pwsh", "-NoLogo", "-NoProfile", "-Command", command])
        except docker.errors.APIError as e:
            raise RuntimeError(f"Unable to execute PowerShell command in container:\n{e}") from e

        output = result.output.decode("utf-8", errors="replace")
        if result.exit_code != 0:
            logger.error(f"PowerShell command failed ({result.exit_code}):\n{output}")
        return output

    def stop(self):
        """
            Stop and remove the PowerShell container.
        """
        if self.container is None:
            return
        try:
            self.container.reload()
            if self.container.status == "running":
                logger.info("Stopping PowerShell container")
                self.container.stop(timeout=5)
            logger.info("Removing PowerShell container")
            self.container.remove()
        except docker.errors.NotFound:
            pass
        except docker.errors.APIError as e:
            logger.warning(f"Unable to stop/remove PowerShell container:\n{e}")
        finally:
            self.container = None

    def __exit__(self, exc_type, exc_value, traceback):
        """
            Force to stop container when exiting code
        """
        self.stop()


if __name__ == "__main__":

    pwsh_container = PowerShellContainer()

    try:
        print(pwsh_container.run("Get-Date"))
        print(pwsh_container.run("Get-Module -ListAvailable Az"))

        # using python vars
        username = "john@example.com"
        command = f'''
        $user = "{username}"
        Write-Output "User: $user"
        '''
        print(pwsh_container.run(command))

        # passing env vars
        print(pwsh_container.run('$env:MY_VALUE', env_vars={"MY_VALUE": "some value from Python"}))

    finally:
        pwsh_container.stop()
