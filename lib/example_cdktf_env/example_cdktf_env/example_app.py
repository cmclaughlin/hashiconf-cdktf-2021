"""
Example App
"""
from cdktf import App


class ExampleApp(App):
    """
    Base class to allow work arounds
    Here you could search/replace strings in the synthesized output, if needed.
    """

    # Example for working around this bug before it was fixed
    # https://github.com/hashicorp/terraform-cdk/issues/282
    # super().synth()

    # outfile_name = 'cdktf.out/cdk.tf.json'
    # with open(outfile_name) as outfile:
    #     output = outfile.read().replace('self_attribute', 'self')

    # with open(outfile_name, 'w') as outfile:
    #     outfile.write(output)

    pass
