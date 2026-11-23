import importlib.util
import platform
import subprocess


def check_nvidia_gpu():
    """Check whether NVIDIA GPU and its tools are available."""
    try:
        result = subprocess.run(
            ["nvidia-smi"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0:
            return result.stdout.strip()

        return "NVIDIA GPU not detected."
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return "nvidia-smi is unavailable."


def check_windows_gpu():
    """Read GPU names using Windows system information."""
    if platform.system() != "Windows":
        return ["Windows GPU detection is unavailable on this OS."]

    try:
        result = subprocess.run(
            [
                r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
                "-NoProfile",
                "-Command",
                "Get-CimInstance Win32_VideoController | "
                "Select-Object -ExpandProperty Name",
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )

        if result.returncode == 0 and result.stdout.strip():
            return [
                name.strip()
                for name in result.stdout.splitlines()
                if name.strip()
            ]

        return ["No GPU information returned."]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ["Could not query Windows GPU information."]


def check_python_libraries():
    """Report availability of optional acceleration libraries."""
    libraries = ["numba", "torch", "cupy", "pyopencl"]

    return {
        library: importlib.util.find_spec(library) is not None
        for library in libraries
    }


def main():
    print("=== GeneWeaver GPU Capability Check ===")
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Python Version: {platform.python_version()}")

    print("\nGPU Devices:")
    for device in check_windows_gpu():
        print(f"- {device}")

    print("\nNVIDIA Check:")
    print(check_nvidia_gpu())

    print("\nPython Acceleration Libraries:")
    libraries = check_python_libraries()

    for library, installed in libraries.items():
        status = "Installed" if installed else "Not installed"
        print(f"- {library}: {status}")

    print("\nGPU acceleration status:")
    if libraries["torch"] or libraries["cupy"] or libraries["pyopencl"]:
        print("A candidate GPU library is installed; backend support needs testing.")
    else:
        print("No GPU acceleration library is currently configured.")

    print("\nFallback: Standard CPU execution is available.")


if __name__ == "__main__":
    main()

