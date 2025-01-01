import json
import sys
import time

from pyarchitecture import cpu, disks, gpu

version = "0.0.0-a0"


def commandline() -> None:
    """Starter function to invoke PyArchitecture via CLI commands.

    **Flags**
        - ``--version | -V``: Prints the version.
        - ``--help | -H``: Prints the help section.
        - ``disk``: Prints the disk information in the terminal.
        - ``cpu``: Prints the CPU name in the terminal.
        - ``gpu``: Prints the GPU information in the terminal.
        - ``save``: Saves the chosen information into a JSON file.
        - ``--filename``: Filename to store the information.
    """
    assert (
        sys.argv[0].lower().endswith("pyarchitecture")
    ), "Invalid commandline trigger!!"

    print_ver = "--version" in sys.argv or "-V" in sys.argv
    get_help = "--help" in sys.argv or "-H" in sys.argv
    disk_info = "disk" in sys.argv
    cpu_info = "cpu" in sys.argv
    gpu_info = "gpu" in sys.argv
    all_info = "all" in sys.argv
    save_info = "save" in sys.argv

    filename = None
    custom_filename = "--filename" in sys.argv
    if custom_filename:
        filename_idx = sys.argv.index("--filename") + 1
        try:
            filename = sys.argv[filename_idx]
            assert filename.endswith(".json")
        except IndexError:
            print("ERROR:\n\t--filename argument requires a value")
            sys.exit(1)
        except AssertionError:
            print("ERROR:\n\tfilename must be JSON")
            sys.exit(1)

    options = {
        "--version | -V": "Prints the version.",
        "--help | -H": "Prints the help section.",
        "disk": "Prints the disk information in the terminal.",
        "cpu": "Prints the CPU name in the terminal.",
        "gpu": "Prints the GPU information in the terminal.",
        "save": "Saves the chosen information into a JSON file.",
        "--filename": "Filename to store the information.",
    }
    # weird way to increase spacing to keep all values monotonic
    _longest_key = len(max(options.keys()))
    _pretext = "\n\t* "
    choices = _pretext + _pretext.join(
        f"{k} {'·' * (_longest_key - len(k) + 8)}→ {v}".expandtabs()
        for k, v in options.items()
    )

    if print_ver:
        print(f"PyArchitecture {version}")
        sys.exit(0)

    if disk_info and not save_info:
        for disk in disks.get_all_disks():
            print(disk)
        sys.exit(0)
    if cpu_info and not save_info:
        print(cpu.get_cpu_name())
        sys.exit(0)
    if gpu_info and not save_info:
        print(gpu.get_gpu_names())
        sys.exit(0)

    if save_info:
        filename = filename or f"PyArchitecture_{int(time.time())}.json"
        if all_info:
            data = {
                "Disks": disks.get_all_disks(),
                "CPU": cpu.get_cpu_name(),
                "GPU": gpu.get_gpu_names(),
            }
        else:
            data = {}
            if cpu_info:
                data["CPU"] = cpu.get_cpu_name()
            if gpu_info:
                data["GPU"] = gpu.get_gpu_names()
            if disk_info:
                data["Disks"] = disks.get_all_disks()
        with open(filename, "w") as file:
            json.dump(data, file, indent=2)
        print(f"Architecture information has been stored in {filename!r}")
        sys.exit(0)
    else:
        get_help = True

    if get_help:
        print(
            f"\nUsage: pyarchitecture [arbitrary-command]\n\nOptions (and corresponding behavior):{choices}"
        )
        sys.exit(0)