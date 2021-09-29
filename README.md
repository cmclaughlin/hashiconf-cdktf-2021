## Getting Started With CDK for Terraform - HashiConf 2021

Example project for demos

## Stack Creation

Here's how to create a new stack.

```
make init NAME=mystack
cd stacks/mystack
make install
```

## Library Creation

We have a template for creating new Python modules in the lib directory.
These provide re-usable compontents for importing into stacks. Here's how to
create one.

```
make library NAME=mylib
```
