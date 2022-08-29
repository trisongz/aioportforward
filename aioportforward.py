"""
Kubernetes Port-Forward Go-Edition For Python
"""

__version__ = "0.0.1"

import os
import time
import asyncio
import contextlib

from pathlib import Path
from typing import Optional, Generator, AsyncGenerator

import _portforward


class PortforwardError(Exception):
    """Will be raised when something went wrong while the port-forward process."""



# ===== Validators =====

def _validate_str(arg_name, arg):
    if arg is None or not isinstance(arg, str):
        raise ValueError(f"{arg_name}={arg} is not a valid str")

    if len(arg) == 0: raise ValueError(f"{arg_name} cannot be an empty str")

    if "/" in arg: raise ValueError(f"{arg_name} contains illegal character '/'")


def _validate_port(arg_name, arg):
    in_range = arg and 0 < arg < 65536
    if arg is None or not isinstance(arg, int) or not in_range:
        raise ValueError(f"{arg_name}={arg} is not a valid port")


def _config_path(config_path_arg) -> str:
    if config_path_arg and not isinstance(config_path_arg, str):
        raise ValueError(f"config_path: {config_path_arg} is not a valid str")

    elif config_path_arg and os.path.exists(config_path_arg):
        return config_path_arg
    
    elif os.getenv('KUBECONFIG') and os.path.exists(os.getenv('KUBECONFIG')):
        return os.getenv('KUBECONFIG')

    return str(Path.home() / ".kube" / "config")



@contextlib.contextmanager
def forward(
    namespace: str,
    pod: str,
    port: int,
    to_port: Optional[int] = None,
    config_path: Optional[str] = None,
    startup_interval: float = 0.25,
    verbose: bool = False,
) -> Generator[None, None, None]:
    """
    Connects to a Pod and tunnels traffic from a local port to this pod.
    It uses the kubectl kube config from the home dir if no path is provided.

    Caution: Go and the port-forwarding needs some ms to be ready. ``waiting``
    can be used to wait until the port-forward is ready.

    (Best consumed as context manager.)

    Example:
        >>> import aioportforward
        >>> with aioportforward.forward("test", "web", 9000, 80):
        >>>     # Do work

    :param namespace: Target namespace
    :param pod: Name of target Pod
    :param port: Local port
    :param to_port: Port inside the pod. Default to port if empty.
    :param startup_interval: Delay in seconds
    :param verbose: Print output from portforward
    :param config_path: Path for loading kube config
    :return: None
    """

    _validate_str("namespace", namespace)
    _validate_str("pod", pod)
    _validate_port("port", port)
    # allow for default null port
    to_port = to_port if to_port is not None else port
    _validate_port("to_port", to_port)

    config_path = _config_path(config_path)

    try:
        _portforward.forward(namespace, pod, port, to_port, config_path, verbose)
        # Go and the port-forwarding needs some ms to be ready
        time.sleep(startup_interval)
        yield None

    except RuntimeError as err:
        # Suppress extension exception
        raise PortforwardError(err) from None

    finally:
        _portforward.stop(namespace, pod)


@contextlib.asynccontextmanager
async def async_forward(
    namespace: str,
    pod: str,
    port: int,
    to_port: int = None,
    config_path: Optional[str] = None,
    startup_interval: float = 0.25,
    verbose: bool = False,
) -> AsyncGenerator[None, None]:
    _validate_str("namespace", namespace)
    _validate_str("pod", pod)

    _validate_port("port", port)
    # allow for default null port
    to_port = to_port if to_port is not None else port
    _validate_port("to_port", to_port)
    config_path = _config_path(config_path)

    try:
        _portforward.forward(namespace, pod, port, to_port, config_path, verbose)
        #await _portforward.async_forward(namespace, pod, from_port, to_port, config_path, verbose)
        # Go and the port-forwarding needs some ms to be ready
        await asyncio.sleep(startup_interval)
        yield None

    except RuntimeError as err:
        # Suppress extension exception
        raise PortforwardError(err) from None

    finally:
        _portforward.stop(namespace, pod)

# ToDo.
# Create an independent class that can handle
# multiple persistent port-forwarding
#class PortManager:
