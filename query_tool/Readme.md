# Query Tool

This tool contains a Python script to query migration libraries based on our C/C++ library migrations knowledge base. 

The targeted libraries and related information are categorized into direct and iterative targets, and the results are output to file `Targeted_Libraries.txt`.

## Requirements

- Python 3.x
- pandas
- networkx

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Dl0qWmJ4/C-CPPLibraryMigration.git
    cd C-CPPLibraryMigration/query_tool
    ```

2. Install the required Python packages:

    ```sh
    pip install pandas networkx
    ```

## Usage
Run the tool with the required arguments. Below is its usage:

```sh
python query_tool.py --rem_lib <library_to_remove> [--reason <migration_reason>] [--pmt <project_management tool>]
```

The script will generate an output file:
- `Targeted_Libraries.txt`: Contains the direct targeted libraries along with migration rules and commit information, and iterative targeted libraries along with migration rules.

### Optional Arguments

1. `--reason`: The reason for the library migration. This is an optional argument. When specifying the `--reason` argument, you can use one of the following reason types:

	deprecation, bug or issue, feature, usability, performance, activity, popularity, size, integration, simplification

    For example:

    ```sh
    python query_tool.py --rem_lib gtest --reason performance
    ```

2. `--pmt`: The project management tool. This is also an optional argument. You can use one of the following types:

	conan, deb, meson, xmake, vcpkg, gitsubmod

    For example:

    ```sh
    python query_tool.py --rem_lib gtest --pmt conan
    ```