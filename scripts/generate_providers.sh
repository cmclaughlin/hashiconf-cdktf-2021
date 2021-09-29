#! /bin/bash

num_providers=$(cat cdktf.json | jq '.terraformProviders | length')
if (( $num_providers > 0 ));
then
    cdktf get
fi
