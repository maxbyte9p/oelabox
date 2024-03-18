CI Badge

# Kojihub Role
This role installs kojihub and kojiweb. Note that it does NOT install the database. The database must be installed from a different role or playbook method. This role also assumes you are using a Kerberos infrastructure, such as FreeIPA.

FAS is not yet implemented.

Ansible 2.10 users: You will need the community.general collection installed.

## Getting started
Ensure all dependencies are installed and then follow the below process
1. `git clone repo` Get the development repository
2. `pre-commit install` Install the pre-commit hooks
3. Make edits as explained in the customization section
4. `pre-commit` Make sure existing code is good
5. `do development` Dont ask me :D
6. `pre-commit` Make sure the edits are good to go
7. `molecule converge`

## Dependencies
This repo expects 3 things installed on the local machine
1. [pre-commit](https://pre-commit.com/) Methodology to test yaml style
2. [ansible-lint](https://github.com/ansible-community/ansible-lint) lint ansible code for best practices
3. [yamllint](https://github.com/adrienverge/yamllint) Ensures all yaml is well formed

### Customization
There are a few files that are required to be updated when using this template
1. [molecule/requirements.yml](molecule/requirements.yml) - Update with any required  roles or collections
2. [molecule/default/converge.yml](molecule/default/converge.yml) - update with new role name
3. [molecule/default/molecule.yml](molecule/default/molecule.yml) - update with desired distributions and extra playbooks
4. [github](github) - Rename to `.github` and push, this will set up yamllint, ansible-lint and a CI check job for the `main` branch
   1. NOTE: If you are using a SAML token this may fail. You can created the files within the Github web app

### Optional
The github actions are configured to automatically run the molecule tests but if you want to load them locally you will also need molecule installed on the development machine

## Advanced

There are numerous other options within the [defaults/main.yml](./defaults/main.yml) that can change other parts of the behavior of the system

## Changelog
The [changelog](./CHANGELOG.md) is stored externally


