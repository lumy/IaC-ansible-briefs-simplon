#!/usr/bin/python

DOCUMENTATION = """
---
module: world.py
short_description: Hello World from custom ansible module. Write into a file Hello world
options:
  name:
    required: true
    description:
      - World name to say hello to.
  sentence:
    description:
      - additional sentence to say.
  pathfile:
    description:
      - pathfile to hello file
"""


from ansible.module_utils.basic import AnsibleModule

def write_hello(context, pathfile, content):
  try:
    with open(pathfile, "w") as f:
      f.write(content)
  except IOError as e:
    module, result = context
    result['msg'] = "Error during Hello World"
    result['message'] = e.message
    module.fail_json(**result)


def read_hello(context, pathfile):
 try:
    with open(pathfile, "r") as f:
      return f.read()
 except FileNotFoundError as e:
   return ""

def main():
  module_args = dict(
    name=dict(type='str', required=True),
    sentence=dict(type='str', required=False, default=None),
    pathfile=dict(type='str', required=False, default="/tmp/hello.txt")
  )

  result = dict(
    changed=False
  )

  module = AnsibleModule(
    argument_spec=module_args,
  )

  name = module.params['name']
  sentence = module.params['sentence']
  pathfile = module.params['pathfile']

  msg = "Hello World {} !\n".format(name)
  if sentence:
    msg += "{}\n".format(sentence)

  content = read_hello((module, result), pathfile)

  if content != msg:
    write_hello((module, result), pathfile, msg)
    result["changed"] = True
    result["diff"] = [{
      'before':content,
      'after':msg
    }]

  module.exit_json(**result)


if __name__ == '__main__':
    main()
