# noticeCreator
Generates NOTICE file part for libraries and licenses from project dependency.

## Usage

For generate NOTICE file run this command:
> python main.py notice -m maven.deps -n package-lock.json

For generate `maven.deps` file use the following command:
> mvn dependency:list | grep -Poh "\\S+:(system|provided|compile)" | sort | uniq > maven.deps

The tool try to find dependency in clearlydefined service and save the result in local folder.
For local cache folder `.noticeCreator` is used inside user directory.

Not all dependencies are presented in clearlydefined.
Some of the presented have a non valid specified License.
In that case, you could manually overwrite the library license by the following command:
> python main.py overwrite maven/mavencentral/aopalliance/aopalliance/1.0 MIT

For libraries from npmjs you could use special `overwrite_npmjs` command.
The command will read License from npmjs resource and store it for future use.
Example:
> python main.py overwrite_npmjs npm:npmjs:-:color-name:1.1.3
