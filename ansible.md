
# IaC: Infrastucture as Code

You are going to use _Ansible_ to install and configure are server. And ensure that it is always the same state.

> Sadly this tools can not be used on windows. So you'll need to use wsl2 or a virtual Machine on
> your computer

## Introduction

Welcome to the world of *IaC*.

This will make your life easier, as a DevOps or AdminSys you'll have to
create servers and configure them. Most of the configuration will be the same on your server (ex:
authorized ssh only from specific IP, firewall configuration, users configuration).

_Ansible_ is a tool that connect to a server and: run commands, create/modify files/folder, almost
everything can be done (if not everything).


It is written in _python_ and use _yaml_ to explain server configuration.
Here is an example of _yaml_
```yaml
---
- this
- is_a
- list
- dict:
  key: value
  name: toto
```

It is not the only tools to do that, you may have heard of `Chef`, `Puppet`, `Salt`, but these 3 need
a master server to work so you're not gonna use them *today*.

## Philosophy

![Ansible Overview](./Ansible_ov.jpg)

[You should always start reading the basic-concept of new language/framework](https://docs.ansible.com/ansible-core/latest/user_guide/basic_concepts.html#basic-concepts)

[Then it is always a good idea to look at the questions in the FAQ](https://docs.ansible.com/ansible-core/devel/reference_appendices/faq.html)

These are the basic concepts, read about Control node, Managed nodes, Inventory, Tasks and
Playbooks.

Are you in the fog ? It's normal. When you're done reading, we will discuss and understand these new
concepts all together.

## Installation

_Ansible_ use many configuration files in yaml to describe one (or more) server.
from your local machine it will ssh to the remote one and execute your ansible code.
Ansible will try his best to bring your server in the desired state whatever server it is
(unix/linux/windows...).

https://docs.ansible.com/ansible-core/latest/installation_guide/intro_installation.html#installing-ansible-with-pip

_Ansible_ can be used to run playbook or run any ad-hoc remote command.
```bash
  $ ansible all -a "/sbin/reboot" # this will reboot all your nodes.
  $ ansible all -m ansible.builtin.yum -a "name=nginx state=present" # this will install nginx  on all node (that use yum package manager)
  $ ansible-playbook playbook.yml # run all tasks in playbook.yml
  $ ansible-lint play.yml # verify validity of file play.yml
  $ cat /etc/ansible/hosts
  <IP_OR_DOMAIN_NAME>     ansible_ssh_private_key_file=<PATH_TO_SSH_KEY> ansible_ssh_user=<AZURE_USER>
```

_IaC_ Often comes with there package manager.
for _ansible_ it is [ansible-galaxy](https://galaxy.ansible.com/) which is a Collections of free roles/collections
```bash
$ ansible-galaxy --help
$ ansible-galaxy list
$ ansible-galaxy install infopen.fail2ban
```

### Useful Links

  - [introduction to inventory](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#intro-inventory)
  - [Connections methods and configuration](https://docs.ansible.com/ansible/latest/user_guide/connection_details.html)
  - [Jinja2 to template Playbook](https://docs.ansible.com/ansible/latest/user_guide/playbooks_templating.html)
  - [Builtin ansible](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html#modules)
  - [Collections part of ansible](https://docs.ansible.com/ansible/latest/collections/index.html#list-of-collections)
  - [Ansible and Windows Server](https://docs.ansible.com/ansible/latest/collections/ansible/windows/index.html#plugins-in-ansible-windows)
  - [Targeting Nodes](https://docs.ansible.com/ansible/latest/user_guide/intro_patterns.html#intro-patterns)

# Briefs

Create a Linux virtual machine on azure.

## Install Ansible

[Installation Guide](https://docs.ansible.com/ansible-core/devel/installation_guide/intro_installation.html#installing-ansible-with-pip)

```bash
$ python3 -m pip install paramiko ansible
$ ansible --version
ansible 2.10.8
[...]
```

## Create your Inventory

Create your *inventory* with the Azure VM ip.

If you can ping your inventory you can go next step.
```bash
$ ansible all -m ping
www.lumy.me | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
```

## Create a first playbook

Your first playbook will consist on installing and configure what is common to all your server (your personnal user, your aliases, your shell.)

You will have to install:

  - bash
  - python-apt
  - sudo

Then you will have to:

  - create your own user:
    - setup his ssh-key
    - create a file .alias in his home with alias found in `configs/bashrc/alias`
    - found a way to load .alias in .bashrc
  - make your user able to use the sudo command.

Now that you should be able to ssh to your VM and configure them with a default configuration,
you are going to start another playbook.

## Before the second playbook

Let's create another VM. This one will have a domain name.
Go into dns configuration of your vm and set a DNS name. it should look like this:

> {domainname}.{region}.cloudapp.azure.com

In your inventory add this new VM distinct both of them it should look something like that:
```bash
$ cat /etc/ansible/hosts
[proxy]
{dommainname}.{region}.cloudapp.azure.com     ansible_ssh_private_key_file={PATH_TO_SSH_KEY}
[webapp]
{IP_FIRST_VM}  ansible_ssh_private_key_file={PATH_TO_SSH_KEY}
```
Now use Ansible galaxy and install one playbook that will interact with let'sencrypt.
You are free to choose any. (there is alot, called `certbot` or `letsencrypt`)

## Second Playbook

 - This playbook should only target proxy
 - It should install a WebServer:
   - configure a virtualhost to listen on port 80 and respond to letsencrypt or redirect to port 443
   - configure a virtualhost to listen on port 443 and Proxy to the first VM (port 80).
 - request certificate from letsencrypt
 - install fail2ban

## Third Playbook

Now it is time to deploy a website.

### Create a blog

Use [pelican](https://blog.getpelican.com/) to create a simple blog, change the template and create an article.

### Deploy your blog with the playbook

Write the third playbook:
  - This playbook should only target webapp.
  - It should install python.
  - It should install the python package pelican.
  - copy your article.
  - generate your site.
  - install nginx.
  - make your blog available on port 80.


## A playbook to control them all

Isn't a little boring to run each playbook on his side.

Let's write a playbook that include the other.

Now you can run this playbook and configure all our server !

# You are not done yet !

You should look at how to includes variables into playbook or how to read them from another file,
Remember the first playbook to create your user.
Make it generics so that you could easily create any new user in few lines of _yaml_.

_Ansible_ is a world like every IaC.

First You can have a look at _Galaxy_ It contains alot alot of package. You should *ALWAYS* check before use any of
them in a industry environment

 - Then to go deeper You can start searching for `Roles` in _ansible_, It is a *fondamental* key of _ansible_.
 - Dynamique inventory [based on azure api for example](https://github.com/ansible-collections/community.general/blob/main/scripts/inventory/azure_rm.py)
 - _Ansible Vault_ which is mandatory for Real production enviroment.
 - Lookups which can be very usefull
 - Interactive input: prompts
 - [TroubleShooting One Task](https://docs.ansible.com/ansible/latest/user_guide/playbooks_startnstep.html)
 - [Debugging Task](https://docs.ansible.com/ansible/latest/user_guide/playbooks_debugger.html)
 - [Windows Guide](https://docs.ansible.com/ansible/latest/user_guide/windows.html)

And we are far from having understand/learn about _Ansible_.
Only one thing to do: Use it ! find a way to make your life easier with it.
Prepare playbook for your future briefs on azure, or to manage your personnal server.

You think ansible is too much Yaml file and not enough Code ? I agree, you should check `salt`
for more python, but it still use too many yaml.

You want some challenges ? It is time to learn about `chef`
(or `puppet` but it is a little older and the community is dropping slowly).
