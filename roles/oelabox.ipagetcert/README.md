CI Badge

# ipa-getcert Ansible Role
This is a modified version of the Rocky Linux ipa-getcert role for Oela Box.

A very basic ipa-getcert role used for certificates issued for internal communication. This assumes the client is enrolled with FreeIPA.

This is loosely based on another project on github with some heavy modifications and adapted for the Rocky Linux infrastructure. In particular, we have made it more modular. This may be used and copied.

**Note**: Note that the certificates should auto-renew when requested via `ipa-getcert`. However. if you turn on the chain, you will have to fix that manually.

## Getting started
Ensure all dependencies are installed and then follow the below process
1. `git clone repo` Get the development repository
2. `pre-commit install` Install the pre-commit hooks
3. Make edits as explained in the customization section
4. `pre-commit` Make sure existing code is good
5. `do development` You know what to do
6. `pre-commit` Make sure the edits are good to go
7. `molecule converge`

## Dependencies
This repo expects 3 things installed on the local machine
1. [pre-commit](https://pre-commit.com/) Methodology to test yaml style
2. [ansible-lint](https://github.com/ansible-community/ansible-lint) lint ansible code for best practices
3. [yamllint](https://github.com/adrienverge/yamllint) Ensures all yaml is well formed

### Customization
If you can come up with a customization to this, go for it!

### Optional
The github actions are configured to automatically run the molecule tests but if you want to load them locally you will also need molecule installed on the development machine

## Advanced
There are numerous other options within the [defaults/main.yml](./defaults/main.yml) that can change other parts of the behavior of the system

## Changelog
The [changelog](./CHANGELOG.md) is stored externally

