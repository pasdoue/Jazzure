import subprocess
import threading
import uuid
from pathlib import Path
from typing import Union, Optional

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
            It manages a persistent powershell session to be able to import modules and use them later ;) (also saving context between runs)
        """
        self.client: Optional[DockerClient] = None
        self.image: Optional[Image] = None
        self.container: Optional[Container] = None
        self._docker_runtime_name = f"{self.DOCKER_IMAGE_NAME}-runtime"
        # Persistent PowerShell process. Allow to chains commands without losing imported modules or context
        self._powershell_process = None

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
        self._start_persistent_powershell()

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
                command=["sleep", "infinity"],
                name=self._docker_runtime_name,
                detach=True,
                remove=False,
            )
            logger.success(f"Container started: {container.id}")
            return container
        except docker.errors.APIError as e:
            logger.error(f"Unable to start PowerShell container:\n{e}")
            raise

    def _start_persistent_powershell(self) -> None:
        """
            Start one persistent PowerShell process inside the container.
            This process remains alive for the entire lifetime of the PowerShellContainer object.
        """
        if self.container is None:
            raise RuntimeError("Docker container has not been created")

        self.container.reload()
        if self.container.status != "running":
            raise RuntimeError(f"Container is not running: {self.container.status}")

        logger.info("Starting persistent PowerShell process")
        self._powershell_process = subprocess.Popen(
            [ "docker", "exec", "-i", self.container.id, "pwsh", "-NoLogo", "-NoProfile", "-Command", "-" ],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0
        )
        if self._powershell_process.stdin is None:
            raise RuntimeError("Unable to open PowerShell stdin")
        if self._powershell_process.stdout is None:
            raise RuntimeError("Unable to open PowerShell stdout")
        logger.success("Persistent PowerShell session started")

    def run(self, command: str, env_vars: Optional[dict] = None, timeout: float = 60.0) -> str:
        """
            Execute a PowerShell command inside the running container.
        """
        if not command or not command.strip():
            raise ValueError("PowerShell command cannot be empty")

        process = self._powershell_process
        if process is None:
            raise RuntimeError("PowerShell session is not running")
        if process.poll() is not None:
            raise RuntimeError("PowerShell process has terminated")

        marker = (f"__JAZZURE_COMMAND_END_{uuid.uuid4().hex}__")

        logger.debug(f"Executing PowerShell command:\n{command}")
        # Optional environment variables
        env_commands = ""
        if env_vars:
            for key, value in env_vars.items():
                value = str(value).replace("'", "''")
                env_commands += (f"$env:{key} = '{value}'\n")

        payload = (
                env_commands
                + command
                + "\n"
                + f"Write-Output '{marker}'"
                + "\n"
        )
        try:
            process.stdin.write(payload.encode("utf-8"))
            process.stdin.flush()
        except (BrokenPipeError, OSError) as e:
            raise RuntimeError("Lost connection to PowerShell process") from e

        # Read output until marker
        output = bytearray()
        def read_output() -> None:
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                output.extend(line)
                if marker.encode("utf-8") in line:
                    break

        reader = threading.Thread(target=read_output, daemon=True)
        reader.start()
        reader.join(timeout)
        if reader.is_alive():
            logger.error(f"PowerShell command timed out after {timeout} seconds")
        decoded = output.decode("utf-8", errors="replace",)
        # Remove marker
        marker_position = decoded.find(marker)
        if marker_position != -1:
            decoded = decoded[:marker_position]
        return decoded

    def stop(self) -> None:
        """
            Remove powershell persistent connector & ttop container
        """
        # Stop persistent PowerShell process
        if self._powershell_process is not None:
            logger.info("Stopping persistent PowerShell process")
            try:
                self._powershell_process.stdin.close()
            except Exception:
                pass
            try:
                self._powershell_process.terminate()
                self._powershell_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._powershell_process.kill()
                self._powershell_process.wait()
            except Exception:
                pass
            self._powershell_process = None

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

    def __enter__(self):
        return self


if __name__ == "__main__":

    pwsh_container = PowerShellContainer()

    try:
        print(pwsh_container.run("Get-Date"))
        #print(pwsh_container.run("Get-InstalledModule Az"))
        print(pwsh_container.run("Import-Module -Name AADInternals"))
        #print(pwsh_container.run("Import-Module -Name AADInternals-Endpoints"))
        print(pwsh_container.run("Get-InstalledModule Microsoft.Entra"))
        print(pwsh_container.run("Get-InstalledModule Microsoft.Graph"))

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
