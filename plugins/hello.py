from nikola.plugin_categories import Command

class CommandHello(Command):
    """Just test commmand which is hello"""
    name = "hello"
    doc_usage = '[options]'
    doc_purpose = 'say the hello world'

    cmd_options = (
        {
            'name': 'name',
            'short': 'n',
            'long': 'name',
            'type': str,
            'default': 'tonghu',
            'help': 'name for the hello name'
        },
    )

    def _execute(self, options, args):
        "say hello to someone."
        print("hello " + options['name'])
        
