## Getting Started With CDK for Terraform - HashiConf 2021

This repo contains a couple reusable libraries and example stacks
that highlight cdktf features and patterns. There's a top-level Makefile
with the following features:

### Stack Creation

Here's how to create a new stack.

```
make init NAME=mystack
cd stacks/mystack
make install
```

### Library Creation

We have a template for creating new Python modules in the lib directory.
These provide re-usable compontents for importing into stacks. Here's how to
create one.

```
make library NAME=mylib
```

## Example Modules

### example_cdktf_env

`example_cdktf_env` contains the ExampleStack, which can be used to derived new
classes using inheritance. It automatically configures some common patterns,
such as state management and the AWS provider.

### example_s3

`example_s3` is a trivial example of a reusable Python module that can be
imported into stacks.

## Example Stacks

### cdk-state

cdk-state demonstrates how to setup S3 and DynamoDB for Terraform state
management for use with the `ExampleStack` class.

### example-site

The `example-site` stack is very simple deplyoment of a static website hosted
on S3. The S3 bucket could have easily been created within the stack, but
it demonstrates the use of inheriting the `ExampleStack` class and the reusable
`example_s3` module.
