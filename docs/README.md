<!--
SPDX-FileCopyrightText: 2024 Maxine Hayes <maxinehayes90@gmail.com>
SPDX-License-Identifier: CC-BY-SA-4.0
-->
# Oela Box

-   About Oela Box
    -   [Purpose of Oela Box](topics/about-PurposeOfOelaBox.md#purpose)
    -   [Expectations of Oela Box](topics/about-ExpectationsOfOelaBox.md#expectations)
    -   [Expectations of The User](topics/about-ExpectationsOfTheUser.md#userexpectations)
        -   [Learning Resources](topics/about-ExpectationsOfTheUser.md#learning)
    -   [Technical Aspects of Oela Box](topics/about-TechnicalAspectsOfOelaBox.md#technical)
        -   [Vagrant](topics/about-TechnicalAspectsOfOelaBox.md#vagrant)
            -   [Virtual Machines](topics/about-TechnicalAspectsOfOelaBox.md#virtualmachines)
                -   [DNS Server](topics/about-TechnicalAspectsOfOelaBox.md#dnsserver)
                -   [IPA Server](topics/about-TechnicalAspectsOfOelaBox.md#ipaserver)
                -   [Koji Server](topics/about-TechnicalAspectsOfOelaBox.md#kojiserver)
                    - [Koji Builder](topics/about-TechnicalAspectsOfOelaBox.md#kojibuilder)
                    - [Koji Hub](topics/about-TechnicalAspectsOfOelaBox.md#kojihub)
                    - [Koji Web](topics/about-TechnicalAspectsOfOelaBox.md#kojiweb)
                    - [Kojira](topics/about-TechnicalAspectsOfOelaBox.md#kojira)
                    - [Koji-gc](topics/about-TechnicalAspectsOfOelaBox.md#kojigc)
                    - [Apache2](topics/about-TechnicalAspectsOfOelaBox.md#apache2)
                    - [IPA Client](topics/about-TechnicalAspectsOfOelaBox.md#ipaclient)
        -   [Ansible](topics/about-TechnicalAspectsOfOelaBox.md#ansible)
            -   [Provisioning Playbooks](topics/about-TechnicalAspectsOfOelaBox.md#provisioningplaybooks)
            -   [Directories Labelled "ansible-xxxx-management"](topics/about-TechnicalAspectsOfOelaBox.md#dirslabelled)
                -   [Inside These Directories](topics/about-TechnicalAspectsOfOelaBox.md#insidedirs)
                    -   [role-oelabox-xxxx.yml](topics/about-TechnicalAspectsOfOelaBox.md#role-oelabox-xxxx.yml)
                    -   [init-oelabox-xxxx.yml](topics/about-TechnicalAspectsOfOelaBox.md#init-oelabox-xxxx.yml)
                        -   [An Example of init-oelabox-xxxx.yml](topics/about-TechnicalAspectsOfOelaBox.md#anexampleinit)
                    -   [import-xxxx.yml](topics/about-TechnicalAspectsOfOelaBox.md#import-xxxx.yml)
                    -   [adhoc-xxxx.yml](topics/about-TechnicalAspectsOfOelaBox.md#adhoc-xxxx.yml)
                        -   [An Example of adhoc-xxxx.yml](topics/about-TechnicalAspectsOfOelaBox.md#anexampleadhoc)
                    -   [Sub-directories](topics/about-TechnicalAspectsOfOelaBox.md#subdirs)
            -   [roles Directory](topics/about-TechnicalAspectsOfOelaBox.md#rolesdir)
                -   [Role Naming Scheme Examples](topics/about-TechnicalAspectsOfOelaBox.md#rolenaming)
                    -   [oelabox.kojid](topics/about-TechnicalAspectsOfOelaBox.md#oelabox.kojid)
                    -   [oelabox.geerlingguy.postgresql](topics/about-TechnicalAspectsOfOelaBox.md#oelabox.geerlingguy.postgresql)
        -   [Bash](topics/about-TechnicalAspectsOfOelaBox.md#bash)
        -   [Python](topics/about-TechnicalAspectsOfOelaBox.md#python)
            -   [Koji Error Example](topics/about-TechnicalAspectsOfOelaBox.md#kojierrorexample)
        -   [Enterprise Linux](topics/about-technicalAspectsOfOelaBox.md#enterpriselinux)

-   Operation of Oela Box
    -   [Preparation](topics/operation-Preparation.md#preparation)
        -   [Recommended Hardware Specs](topics/operation-Preparation.md#hardwarespecs)
        -   [Recommended Virtual Machine Specs](topics/operation-Preparation.md#virtualmachinespecs)
        -   [OS Compatibility](topics/operation-Preparation.md#oscompat)
        -   [Automated Setup](topics/operation-Preparation.md#setup)
    -   [Start, Stop, Destroy, and Reset](topics/operation-StartStopDestroyandReset.md#ssdr)
        -   [Start](topics/operation-StartStopDestroyandReset.md#start)
        -   [Stop](topics/operation-StartStopDestroyandReset.md#stop)
        -   [Destroy](topics/operation-StartStopDestroyandReset.md#destroy)
        -   [Reset](topics/operation-StartStopDestroyandReset.md#reset)
    -   [Koji Server](topics/operation-KojiServer.md#kojiserver)
        -   [Login Through SSH](topics/operation-KojiServer.md#loginssh)
        -   [Login To The oelakoji User With Kerberos](topics/operation-KojiServer.md#loginoelakoji)
            -   [Test Koji Kerberos Authentication](topics/operation-KojiServer.md#testkerbauth)
        -   [About Package Building](topics/operation-KojiServer.md#aboutpkgbuilding)
            -   [Basic Information About Tags](topics/operation-KojiServer.md#basictaginfo)
                -   [Dist Tags](topics/operation-KojiServer.md#disttags)
                -   [Build Tags](topics/operation-KojiServer.md#buildtags)
            -   [SCM](topics/operation-KojiServer.md#scm)
            -   [Building A Package](topics/operation-KojiServer.md#buildingapkg)

-   DNS Server

-   IPA Server

-   Koji Server
